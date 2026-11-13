# 🤖 RAG-Grounded AI Customer Support Triage Agent

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash--Lite-8E75B2?logo=googlegemini&logoColor=white)
![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-orange)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)

An end-to-end automated customer support triage and response pipeline built with **Python**, **Google Gemini**, **ChromaDB**, and **Streamlit**. 

This application ingests unstructured customer inquiries, deterministically classifies intent and priority into structured JSON, retrieves exact company policy excerpts from a local vector database (RAG), and drafts grounded, hallucination-free email responses via an interactive dashboard.

---

## 🎯 Problem & Solution

* **The Problem:** Support teams spend hours manually sorting incoming tickets, identifying critical production outages, filtering spam, and looking up company policies to write repetitive replies. Furthermore, standard LLM wrappers often hallucinate company rules (like refund windows or escalation steps) when generating drafts.
* **The Solution:** A modular AI pipeline that enforces strict JSON schema classification for instant routing and uses **Retrieval-Augmented Generation (RAG)** to ground every drafted email strictly in verified internal company documentation.

---

## 🏗️ System Architecture

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
