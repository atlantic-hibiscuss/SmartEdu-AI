"""FastAPI backend for the SmartEdu AI project."""

from functools import lru_cache
from pathlib import Path
import os
import sys

from fastapi import FastAPI
from pydantic import BaseModel

ROOT_DIR = Path(__file__).resolve().parents[2]
CACHE_DIR = ROOT_DIR / ".cache" / "huggingface"
PERSIST_DIR = ROOT_DIR / "chroma_db"

# Keep model caches inside the project so Windows permission issues in the
# user profile do not break startup
os.environ.setdefault("HF_HOME", str(CACHE_DIR))
os.environ.setdefault("HUGGINGFACE_HUB_CACHE", str(CACHE_DIR / "hub"))
os.environ.setdefault("TRANSFORMERS_CACHE", str(CACHE_DIR / "transformers"))
os.environ.setdefault(
    "SENTENCE_TRANSFORMERS_HOME",
    str(CACHE_DIR / "sentence_transformers"),
)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT_DIR))

from src.llm_utils import call_llm  # noqa: E402
from langchain_community.embeddings import HuggingFaceEmbeddings  # noqa: E402
from langchain_community.vectorstores import Chroma  # noqa: E402

app = FastAPI(title="SmartEdu AI API - Riyash Subba")

# Simple in theememory conversation history per server session.
_history: str = ""


class ChatRequest(BaseModel):
    message: str
    difficulty: str = "Beginner"


class ChatResponse(BaseModel):
    answer: str


def is_simple_greeting(message: str) -> bool:
    normalized = message.strip().lower()
    return normalized in {"hi", "hello", "hey", "hiya"}


def get_small_talk_reply(message: str) -> str | None:
    normalized = " ".join(message.strip().lower().split())

    if normalized in {"hi", "hello", "hey", "hiya"}:
        return "Hello fellow scholar,"
    if normalized in {
        "can i ask you something",
        "can i ask something",
        "may i ask you something",
        "can i ask a question",
    }:
        return "Hello fellow scholar, of course you can. What would you like to learn today?"
    if normalized in {"how are you", "how are you?"}:
        return "Hello fellow scholar, I am doing well and ready to help you learn."
    return None


@lru_cache(maxsize=1)
def get_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectordb = Chroma(
        persist_directory=str(PERSIST_DIR),
        embedding_function=embeddings,
    )
    return vectordb.as_retriever(search_kwargs={"k": 3})


def retrieve_context(question: str) -> str:
    """Load relevant context while supporting old and new LangChain retrievers."""
    try:
        retriever = get_retriever()
        if hasattr(retriever, "invoke"):
            docs = retriever.invoke(question)
        else:
            docs = retriever.get_relevant_documents(question)
    except Exception as exc:
        return (
            "Reference material could not be loaded right now. "
            f"Continue without it.\n[Retrieval error: {exc}]"
        )

    return "\n".join(doc.page_content for doc in docs)


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    global _history

    # Short greetings do not need retrieval or an LLM call.
    quick_reply = get_small_talk_reply(req.message)
    if quick_reply is not None:
        answer = quick_reply
        _history += f"Student: {req.message}\nTutor: {answer}\n"
        return ChatResponse(answer=answer)

    context = retrieve_context(req.message)
    # Prompt keeps both retrieved notes and the recent chat in view.
    prompt = (
        f"You are a friendly, helpful, and patient tutor. The user prefers a {req.difficulty.lower()} level explanation. "
        "Use the reference material and conversation history to answer the student's question.\n\n"
        f"Reference material:\n{context}\n\n"
        f"Conversation history:\n{_history}"
        f"Student: {req.message}\n"
        "Tutor:"
    )

    answer = call_llm(prompt, max_new_tokens=150)

    _history += f"Student: {req.message}\nTutor: {answer}\n"
    lines = _history.strip().splitlines()
    # Trim old exchanges so one long session does not bloat every future prompt.
    if len(lines) > 8:
        _history = "\n".join(lines[-8:]) + "\n"

    return ChatResponse(answer=answer)


@app.get("/health")
def health():
    return {"status": "ok", "project": "SmartEdu AI", "author": "Riyash Subba"}
