"""
Shared LLM helpers for the SmartEdu AI project.

Primary path:
- Hugging Face router chat-completions API using HF_TOKEN.

Fallback path:
- If the remote model cannot be reached, return a useful answer built from the
  retrieved local context instead of failing silently.
"""

import os
from typing import List

import requests
from dotenv import load_dotenv

load_dotenv()

HF_MODEL = os.getenv("HF_CHAT_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"


def get_token() -> str:
    return os.getenv("HF_TOKEN", "").strip()


def get_headers() -> dict[str, str]:
    token = get_token()
    headers = {"Content-Type": "application/json"}
    # Skip Authorization entirely if the token is missing so the failure message stays clearer.
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _extract_section(prompt: str, start_marker: str, end_marker: str) -> str:
    if start_marker not in prompt:
        return ""

    section = prompt.split(start_marker, 1)[1]
    if end_marker in section:
        section = section.split(end_marker, 1)[0]
    return section.strip()


def _extract_latest_question(prompt: str) -> str:
    start_marker = "Student:"
    end_marker = "\nTutor:"

    # Work backwards so we grab the newest turn in a long prompt.
    start = prompt.rfind(start_marker)
    if start == -1:
        return ""

    start += len(start_marker)
    end = prompt.find(end_marker, start)
    if end == -1:
        end = len(prompt)
    return prompt[start:end].strip()


def _clean_lines(text: str, limit: int = 3) -> List[str]:
    lines = [line.strip(" -\t") for line in text.splitlines()]
    lines = [line for line in lines if line]
    return lines[:limit]


def build_offline_fallback(prompt: str, error_message: str) -> str:
    """Return a useful response even when the remote LLM is unavailable."""
    question = _extract_latest_question(prompt)
    context = _extract_section(
        prompt,
        "Reference material:\n",
        "\n\nConversation history:",
    )

    context_lines = _clean_lines(context)
    if context_lines:
        joined = " ".join(context_lines)
        return (
            "I could not reach the online language model, so here is a "
            "context-based answer from the local knowledge base.\n\n"
            f"Question: {question or 'No question provided.'}\n"
            f"Helpful context: {joined}\n\n"
            "If you want a richer generated explanation, add a valid HF_TOKEN "
            "to the .env file and try again."
        )

    return (
        "I could not reach the online language model, and no matching local "
        "reference material was available.\n\n"
        f"Question: {question or 'No question provided.'}\n"
        f"Technical detail: {error_message}\n\n"
        "Please verify your HF_TOKEN and internet access to "
        "router.huggingface.co."
    )


def _missing_token_message() -> str:
    return (
        "The external Hugging Face API is configured to use the current "
        "router endpoint, but HF_TOKEN is missing.\n\n"
        "Add your Hugging Face token with inference permissions to `.env` as:\n"
        "HF_TOKEN=your_token_here"
    )


def call_llm(prompt: str, max_new_tokens: int = 150) -> str:
    """Call the Hugging Face router API and fall back gracefully if needed."""
    if not get_token():
        return _missing_token_message()

    # This mirrors a normal chat-completions request, just with one user message.
    payload = {
        "model": HF_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_new_tokens,
        "temperature": 0.7,
    }
    try:
        response = requests.post(
            HF_API_URL,
            headers=get_headers(),
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        choices = data.get("choices", [])
        if choices:
            message = choices[0].get("message", {})
            content = message.get("content", "")
            # Some providers can return richer content objects, but plain text is the common case here.
            if isinstance(content, str):
                return content.strip()
        return str(data)
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        if status == 401:
            return (
                "Hugging Face rejected the request with 401 Unauthorized.\n\n"
                "Your HF_TOKEN is missing, invalid, or lacks inference access."
            )
        if status == 402:
            return (
                "Hugging Face reported a billing or quota issue.\n\n"
                "Check your Inference Providers usage and token permissions."
            )
        detail = exc.response.text[:300] if exc.response is not None else str(exc)
        return (
            "The remote model returned an HTTP error.\n\n"
            f"Status: {status}\n"
            f"Details: {detail}"
        )
    except Exception as exc:
        return build_offline_fallback(prompt, str(exc))
