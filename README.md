# RAG-Grounded AI Customer Support Triage Agent

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-3.5%20Flash--Lite-8E75B2?logo=googlegemini&logoColor=white)
![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-orange)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)

An end-to-end automated customer support triage and response pipeline built with **Python**, **Google Gemini**, **ChromaDB**, and **Streamlit**. 

This application ingests unstructured customer inquiries, deterministically classifies intent and priority into structured JSON, retrieves exact company policy excerpts from a local vector database (RAG), and drafts grounded, hallucination-free email responses via an interactive dashboard.

---

## Problem & Solution

* **The Problem:** Support teams spend hours manually sorting incoming tickets, identifying critical production outages, filtering spam, and looking up company policies to write repetitive replies. Furthermore, standard LLM wrappers often hallucinate company rules (like refund windows or escalation steps) when generating drafts.
* **The Solution:** A modular AI pipeline that enforces strict JSON schema classification for instant routing and uses **Retrieval-Augmented Generation (RAG)** to ground every drafted email strictly in verified internal company documentation.

---

## System Architecture

```text
[ Customer Ticket Input (Streamlit UI) ]
                  │
                  ▼
┌───────────────────────────────────┐
│   Gemini Classifier (JSON Mode)   │  ──▶ Category, Priority, Summary
└─────────────────┬─────────────────┘
                  │
      ┌───────────┴──────────────┬─────────────────┐
      ▼                          ▼                 ▼
[ Support / Feature ]        [ Urgent ]         [ Spam ]
      │                          │                 │
      ▼                          ▼                 ▼
Query ChromaDB (RAG)      Escalate Alert     Log & Filter
(`rag_store.py`)
      │
      ▼
Generate Grounded Draft
(`generator.py`)
```

---

## Project Structure

```text
ai-ticket-triage-agent/
├── company_faq.md       # Knowledge base containing official support policies
├── rag_store.py         # ChromaDB vector indexing & semantic retrieval logic
├── generator.py         # Gemini API classification & RAG-grounded draft generation
├── streamlit_app.py     # Interactive local web dashboard
├── requirements.txt     # Project dependencies
├── .gitignore           # Excludes .env, output/, and local chroma_db/ cache
└── README.md            # Project documentation
```

---

## How to Run the Project Locally

### Prerequisites
* **Miniconda or Anaconda** installed on your machine
* A free **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com/)

### Step 1: Clone the Repository
Open your terminal (on Windows, open **Anaconda Prompt** or **PowerShell** with Conda initialized) and run:
```bash
git clone https://github.com/hsk2110/ai-ticket-triage-agent.git
cd ai-ticket-triage-agent
```

### Step 2: Create the Conda Environment & Install Dependencies
```bash
# 1. Create a clean Python 3.11 environment
conda create -n ai-automation python=3.11 -y

# 2. Activate the environment
conda activate ai-automation

# 3. Install required packages
pip install -r requirements.txt
```

### Step 3: Add Your Gemini API Key
1. Create a `.env` file in the root of the project.
2. Add the following line:
```env
GEMINI_API_KEY="your_actual_api_key_here"
```

### Step 4: Initialize the Local Vector Database (Optional)
The app automatically indexes `company_faq.md` on startup, or you can manually build and test the ChromaDB vector store first:
```bash
python rag_store.py
```

### Step 5: Launch the Streamlit Web Dashboard
Start the local web interface:
```bash
streamlit run streamlit_app.py
```
The dashboard will open automatically in your browser at `http://localhost:8501`.