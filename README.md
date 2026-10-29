# CodeFix AI — Intelligent AI Coding Agent

> A full-stack, local-first AI coding assistant tailored for developers and hackathons. Built with **Python**, **Flask**, **LangChain**, **Ollama (`qwen2.5-coder:3b`)**, and **IBM Db2**.

---

## 🚀 Architecture Overview

```
                          ┌─────────────────────────────┐
                          │   Browser Frontend (UI/UX)   │
                          │   Dark Charcoal Dev Theme   │
                          │   Prism.js Syntax Highlight │
                          └──────────────┬──────────────┘
                                         │ JSON / HTTP
                                         ▼
                          ┌─────────────────────────────┐
                          │     Flask Web Application   │
                          │  Input Guardrails & Routing │
                          └──────┬───────────────┬──────┘
                                 │               │
                 Static AST Check│               │ Natural Language Prompts
                                 ▼               ▼
        ┌──────────────────────────────┐   ┌──────────────────────────────┐
        │   Python Static Analyzer     │   │     LangChain AI Agent       │
        │   ast module & syntax parser │   │   Ollama: qwen2.5-coder:3b   │
        └──────────────────────────────┘   └──────────────┬───────────────┘
                                                          │
                                                          ▼
                                           ┌──────────────────────────────┐
                                           │   IBM Db2 Enterprise Cloud   │
                                           │   ibm_db Parameterized SQL   │
                                           └──────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend Framework** | Flask (Python 3.10+) | Application routing, REST API endpoints, validation guardrails |
| **Frontend UI/UX** | HTML5, CSS3, JavaScript | Responsive dark developer workspace, dual-pane editor & preview |
| **AI Framework** | LangChain | Prompt engineering, structured output parsing, agent orchestration |
| **Local Model Runtime** | Ollama (`qwen2.5-coder:3b`) | Free, private, offline-capable code generation & refactoring |
| **Deterministic Analyzer** | Python `ast` module | Pre-execution syntax validation and structural diagnostics |
| **Database** | IBM Db2 (`ibm_db`) | Secure persistent storage for request history & code records |
| **Test Suite** | pytest | Automated route, analyzer, AI agent, and database unit tests |

---

## 📋 Features

1. **Write Code (Feature A):** Generate clean, modular code with functional explanations from natural-language descriptions.
2. **Debug Code (Feature B):** Deterministic Python AST syntax checking combined with AI root-cause diagnosis and correction.
3. **Improve Code (Feature C):** Refactor existing snippets for readability, performance, and maintainability without breaking behavior.
4. **Explain Code (Feature D):** Step-by-step logic breakdown, architectural walkthrough, and algorithmic complexity analysis.
5. **Conversational Follow-ups (Feature E):** Interactive follow-up thread within the session (e.g., "Make it simpler", "Add input validation").
6. **Persistent History (Feature F):** Complete record tracking backed by IBM Db2 with search, filter, and code copy actions.

---

## 💻 Beginner-Friendly Windows 11 Setup Guide

Follow these exact steps in **Windows PowerShell**:

### 1. Prerequisites Check
Ensure Python 3.10+ and Git are installed:
```powershell
python --version
git --version
```

### 2. Clone or Open the Repository
```powershell
cd C:\Users\raiak\OneDrive\Desktop\CodeFix-AI
```

### 3. Create & Activate Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1
```
> *Tip: If PowerShell blocks script execution, run:* `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`

### 4. Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy the template `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
Open `.env` in your text editor (VS Code, Notepad) and review settings:
- `OLLAMA_MODEL=qwen2.5-coder:3b`
- `OLLAMA_BASE_URL=http://localhost:11434`
- `DB2_HOSTNAME`, `DB2_UID`, `DB2_PWD` (Set your IBM Db2 credentials)

### 6. Set Up Ollama Local AI (Free, No API Keys)
1. Download Ollama for Windows from [https://ollama.com/download](https://ollama.com/download).
2. Install and launch Ollama.
3. In a separate PowerShell terminal, pull the required model:
```powershell
ollama pull qwen2.5-coder:3b
```
4. Verify the model is running:
```powershell
ollama list
```

### 7. Run Automated Tests
```powershell
python -m pytest tests/ -v
```

### 8. Start CodeFix AI Application
```powershell
python app.py
```
Open your browser and navigate to:
👉 **`http://localhost:5000`**

---

## 🛡️ Security & Reliability Guardrails

- **Zero Server Code Execution:** Submitted code is never executed via `eval()`, `exec()`, or subshells on the server.
- **AST Static Isolation:** Python syntax checks rely solely on Python's built-in `ast.parse()` without running the code.
- **Input Bounds:** Enforced character caps (`MAX_INPUT_CHARS=10000`) prevent buffer and memory denial of service.
- **Parameterized SQL:** All queries to IBM Db2 use parameterized markers (`?`) to prevent SQL injection vulnerabilities.
- **Credentials Protection:** Database secrets and environment keys are excluded from git via `.gitignore`.
- **Disclaimer:** All generated code is untrusted output from an AI model and must be reviewed before running locally.

---

## 🗺️ Implementation Roadmap

- [x] **Phase 1 — Foundation and UI:** Flask application, developer workspace layout, mode/language selectors, input guardrails, and route testing.
- [ ] **Phase 2 — Static Analysis:** Deterministic Python AST analysis module (`analyzer.py`) and connection to Debug mode.
- [ ] **Phase 3 — Local AI Agent:** LangChain service (`agent_service.py`) integrated with Ollama `qwen2.5-coder:3b`.
- [ ] **Phase 4 — IBM Db2 Integration:** Dedicated database module (`database.py`), parameterized operations, schema initialization.
- [ ] **Phase 5 — Testing & Hackathon Demo:** End-to-end integration tests, judge demonstration scripts, and presentation polish.
