# Generative & Agentic AI Framework for Literature Analysis

An AI-powered multi-agent framework that automates literature research by retrieving research papers, analyzing their content, identifying research trends and gaps, and generating structured research reports.

## Overview

The framework uses **Generative AI and specialized AI agents** to automate key stages of literature analysis. A coordinator agent manages the workflow and delegates tasks such as paper retrieval, analysis, trend identification, citation generation, and report creation.

## Key Features

* 🔎 **Research Paper Retrieval** — Retrieves relevant papers from arXiv based on a research topic.
* 🤖 **Multi-Agent Analysis** — Uses specialized agents for search, paper analysis, trend analysis, citations, and report generation.
* 🧠 **LLM-Based Summarization** — Extracts core problems, methodologies, and findings from research papers.
* 📊 **Trend & Research Gap Analysis** — Identifies dominant research trends, methodological patterns, and open research problems.
* 📚 **Automated Citations** — Generates structured research references.
* 📄 **Report Generation** — Creates downloadable research reports containing literature reviews, methodology, findings, and references.
* 🔬 **Text Analysis** — Includes TF-IDF/cosine-similarity based text-overlap analysis and heuristic AI-text analysis.
* 🌐 **Web Interface** — React-based frontend connected to the Python AI backend.

## Architecture

```text
User Research Topic
        ↓
Coordinator Agent
        ↓
Paper Search Agent → arXiv
        ↓
Analysis Agent
        ↓
Trend & Research Gap Agent
        ↓
Citation / Text Analysis Agents
        ↓
Report Generation Agent
        ↓
React Dashboard + PDF Report
```

## Tech Stack

* **Python**
* **LLMs / Generative AI**
* **Groq API / Llama Models**
* **arXiv API**
* **React.js**
* **Tailwind CSS**
* **REST API**
* **scikit-learn**
* **ReportLab**
* **Matplotlib**

## Project Structure

```text
├── frontend/          # React frontend
├── agents/            # Specialized AI agents
├── coordinator/       # Multi-agent orchestration
├── report/            # PDF report generation
├── requirements.txt
└── README.md
```

## Workflow

1. User enters a research topic.
2. The system refines the topic into search keywords.
3. Relevant research papers are retrieved from arXiv.
4. Paper abstracts are analyzed using an LLM.
5. Trends, research gaps, and future directions are generated.
6. Citations and text-analysis results are produced.
7. A structured research report is generated and presented through the web interface.

## Note

The text-overlap and AI-text analysis components are implemented as **experimental/heuristic analysis tools**, rather than replacements for commercial plagiarism or AI-detection systems.
