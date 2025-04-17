# SmartEdu AI

Welcome to **SmartEdu AI**, my 10-week engineering internship portfolio project. This repository contains the source code, data pipelines, and weekly logs documenting the development of an intelligent, context-aware AI tutor designed to help students with mathematics and programming.

**Author:** Riyash Subba  
**Email:** reeyash124@gmail.com  
**GitHub:** [atlantic-hibiscuss](https://github.com/atlantic-hibiscuss)  

---

## 🌟 Project Overview

SmartEdu AI is a localized Retrieval-Augmented Generation (RAG) Chatbot Tutor. It leverages Small Language Models (SLMs) and vector databases to feed precise contextual data securely and privately, running entirely locally without needing expensive cloud LLM APIs.

### Key Features
- **Context-Aware Responses:** Uses RAG to answer questions based strictly on a provided curriculum.
- **Modern UI:** Built with Gradio featuring a sleek, dark-themed responsive UI, complete with activity logs, customizable filters, and toast notifications.
- **Local Execution:** 100% local processing ensuring data privacy.
- **Advanced Retrieval:** Employs metadata enrichment for precise context filtering.

### Tech Stack
- **Core AI/ML:** Python 3.11+, LangChain, Hugging Face Transformers
- **Vector Database:** ChromaDB, Sentence Transformers (`all-MiniLM-L6-v2`)
- **API & Frontend:** FastAPI, Gradio, Uvicorn
- **DevOps:** Docker, PyTest, GitHub Actions CI/CD

---

## 📁 Repository Structure

This repository acts as a chronological log of my 10-week internship. The `src` directory contains code separated by weekly milestones, while the `logs` folder holds detailed markdown reports of my progress and learnings for each week.

```text
Γö£ΓöÇΓöÇ .github/workflows/       # CI/CD configurations
Γö£ΓöÇΓöÇ docs/                    # High-level architecture and presentation outlines
Γö£ΓöÇΓöÇ logs/                    # Weekly internship logs (weeks 1 - 10)
Γö£ΓöÇΓöÇ src/
Γöé   Γö£ΓöÇΓöÇ week1/             # Python & ML Foundations (OOP, data structures)
Γöé   Γö£ΓöÇΓöÇ week2/             # NLP Basics & Hugging Face pipelines
Γöé   Γö£ΓöÇΓöÇ week3/             # CLI Bot with LangChain Memory
Γöé   Γö£ΓöÇΓöÇ week4/             # Document Ingestion & ChromaDB Setup
Γöé   Γö£ΓöÇΓöÇ week5/             # Conversational RAG CLI
Γöé   Γö£ΓöÇΓöÇ week6/             # Web API (FastAPI) & Frontend GUI (Gradio)
Γöé   Γö£ΓöÇΓöÇ week8/             # Advanced Metadata Filtering
Γöé   Γö£ΓöÇΓöÇ week9/             # Automated Evaluation & Metrics
Γöé   ΓööΓöÇΓöÇ week10/            # Production Configs & Deployment
Γö£ΓöÇΓöÇ Dockerfile               # Containerization
Γö£ΓöÇΓöÇ requirements.txt         # Dependencies
ΓööΓöÇΓöÇ README.md              
```

---

## 🚀 Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.11+ installed. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Running the Core Application
**Step 1: Start the API Server**
The backend is powered by FastAPI.
```bash
uvicorn src.week6.api:app --reload --port 8000
```

**Step 2: Start the Web UI**
In a new terminal (with your venv activated), launch the frontend:
```bash
python src/week6/ui_app.py
```
Visit `http://127.0.0.1:7860` to access the SmartEdu AI dashboard.

### 3. Exploring the Weekly Modules
You can run specific weekly scripts directly. For example, to run the CLI-based RAG chatbot:
```bash
python src/week5/conversational_rag_cli.py
```
To run the automated evaluation pipeline:
```bash
python src/week9/evaluate_rag.py
```

### 4. Docker Deployment
To run the API server via Docker:
```bash
docker build -t atlantichibiscuss/smartedu-ai:latest .
docker run -p 8000:8000 atlantichibiscuss/smartedu-ai:latest
```

---

## 🔮 Future Improvements
- **Multi-modal Support:** Allow users to upload images of math problems.
- **User Authentication:** Save distinct session histories for different users.
- **Dynamic Curriculum:** Enable drag-and-drop document uploads directly from the UI.
