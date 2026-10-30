# CodeFix AI — Intelligent AI Coding Agent

> A full-stack, local-first AI coding assistant tailored for developers and hackathons. Built with **Python**, **Flask**, **LangChain**, **Ollama (`qwen2.5-coder:1.5b`)**, and **IBM Db2**.

---

## 📹 Demo Video & Quick Links

- 🎥 **Demo Video:** [Watch the Full Walkthrough on YouTube / Loom](https://youtu.be/YOUR_DEMO_VIDEO_ID) <!-- Replace with your actual recorded video URL -->
- 💻 **Live Application Workspace:** [http://localhost:5000](http://localhost:5000)
- 🧪 **Automated Test Suite:** `python -m pytest tests/` (36 passing tests)
- 🔍 **System Diagnostic Check:** `python demo_check.py`

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

## 🛠️ Technology Stack & Architectural Roles

| Technology | Layer | Role & Architectural Rationale |
|---|---|---|
| **Python 3.10+** | Core Language | Powers the backend, native abstract syntax tree (`ast`) parsing, compilation inspection, and unit testing. |
| **Flask** | Web Framework | Lightweight, modular WSGI server. Keeps routes thin, enforces input character limits (`MAX_INPUT_CHARS=10000`), handles CSRF safe parameters, and returns structured JSON. |
| **LangChain** | AI Orchestration | Standardizes prompt templates, enforces security guardrails against prompt injection, formats chat message structures, and connects cleanly with local runtimes. |
| **Ollama (`qwen2.5-coder:3b`)** | Local Model Runtime | Provides 100% free, private, offline-capable code generation, debugging, refactoring, and explanation without external paid API keys. |
| **Python `ast` Module** | Deterministic Analyzer | Pre-execution syntax inspection and anti-pattern detection (mutable defaults, division by literal zero, bare excepts) without executing untrusted user code. |
| **IBM Db2 (`ibm_db`)** | Database | Official `ibm_db` driver executes parameterized SQL queries (`?` markers) to store and retrieve coding session history in IBM Cloud Db2. Includes automatic schema creation and a dedicated Setup Mode. |
| **pytest** | Automated Testing | Comprehensive test suite containing 37 tests covering AST parsing, error handling, Flask routes, AI mocks, and database operations. |

---

## 📋 Main Features

1. **Write Code (Feature A):** Generate clean, modular code from natural-language instructions with architecture overviews and limitation notes.
2. **Debug Code (Feature B):** Deterministic Python AST static diagnostics combined with AI root-cause diagnosis and correction.
3. **Improve Code (Feature C):** Refactor existing code for readability, performance, and maintainability while strictly preserving business logic.
4. **Explain Code (Feature D):** Step-by-step structural walkthrough, Big-O time and space complexity analysis, and edge case breakdown.
5. **Conversational Follow-ups (Feature E):** Multi-turn follow-up chat within the active session ("Make it simpler", "Add input validation", "Convert to Java").
6. **History & Saved Records (Feature F):** Complete record persistence backed by IBM Db2 with search, filter, and code copy actions.

---

## 💻 Beginner-Friendly Windows 11 Setup Guide

Follow these exact steps in **Windows PowerShell**:

### 1. Prerequisites Check
Ensure Python 3.10+ and Git are installed:
```powershell
python --version
git --version
```

### 2. Open the Project Directory
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
> *Tip: If PowerShell displays a script execution policy restriction, run:*  
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`

### 4. Install Dependencies
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` to create your local `.env`:
```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```
Open `.env` in VS Code or Notepad to view settings:
```ini
SECRET_KEY=dev-secret-key-codefix-ai-hackathon-2026
PORT=5000

# Local Ollama Settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:3b
OLLAMA_TIMEOUT=120

# IBM Db2 Database Configuration (Optional for Setup Mode; Required for Live Persistence)
DB2_DATABASE=BLUDB
DB2_HOSTNAME=
DB2_PORT=32733
DB2_UID=
DB2_PWD=
DB2_PROTOCOL=TCPIP
DB2_SECURITY=SSL
```

### 6. Set Up Ollama Local AI (Free, No API Keys Required)
1. Download Ollama for Windows from [https://ollama.com/download](https://ollama.com/download).
2. Install and launch Ollama.
3. In a separate PowerShell terminal, pull the recommended coding model:
```powershell
ollama pull qwen2.5-coder:3b
```
4. Verify the model is downloaded and ready:
```powershell
ollama list
```

### 7. Run One-Click System Diagnostic Check
Run the built-in system verification tool to check your environment, dependencies, Ollama runtime, and Db2 setup:
```powershell
python demo_check.py
```

### 8. Run Automated Test Suite
```powershell
python -m pytest tests/ -v
```

### 9. Start CodeFix AI Application
```powershell
python app.py
```
Open your browser and navigate to:  
👉 **`http://localhost:5000`**

---

## 🎯 4-Step Hackathon Demonstration Script

Follow this script to demonstrate the application to hackathon judges in 3 minutes:

### Step 1: Write Code (Feature A)
1. In the top workspace bar, ensure the **Write Code** tab is active.
2. In the preset dropdown, select **"Write: Python Calculator"** (or type a custom prompt).
3. Click **"Generate Code"**.
4. Point out to judges:
   - Formatted, syntax-highlighted code output in the code panel.
   - One-click **"Copy Code"** and **"Download"** buttons.
   - Structured explanation showing overview, assumptions, and complexity.

### Step 2: Debug Code with Static AST Inspection (Feature B)
1. Click the **Debug Code** tab.
2. Select preset **"Debug: Python Syntax & Logic Bug"**.
3. Click the cyan **"Static AST Check Only"** button.
4. Show the judges:
   - Deterministic AST diagnostics card instantly pinpoints `SyntaxError: expected ':' at line 3` without executing untrusted code on the server.
5. Click **"Debug & Fix Code"** to invoke the AI agent.
6. The AI inspects both the AST diagnostics and the error trace, producing the corrected code and explaining the root cause.

### Step 3: Conversational Follow-Up (Feature E)
1. In the result view, scroll to the **Conversational Follow-Up** card.
2. Click the quick chip **"Make it simpler"** or type: `"Add type hints and comments"`.
3. Click **"Send"**.
4. Show the judges that the session history is preserved and the code block updates dynamically.

### Step 4: History & IBM Db2 Persistence (Feature F)
1. Click **History** in the top navigation bar.
2. Point out:
   - If Db2 credentials are not yet entered, the **"IBM Db2 Setup Mode"** banner is displayed explaining the configuration.
   - If connected, all records are retrieved via parameterized SQL statements from IBM Cloud Db2.
   - Filter by mode, filter by language, or search prompt text.
   - Click **"Open"** on any record to view its full permalink page.

---

## 🛡️ Security & Reliability Guardrails

- **Zero Server Code Execution:** Submitted code is never executed via `eval()`, `exec()`, or subprocess shells on the server.
- **AST Static Isolation:** Python syntax checks rely solely on Python's built-in `ast.parse()` without running the code.
- **Prompt Injection Defense:** System instructions explicitly command the AI to treat user code and comments as untrusted data, refusing to override role constraints.
- **Input Bounds:** Enforced character caps (`MAX_INPUT_CHARS=10000`) prevent buffer and memory denial of service.
- **Parameterized SQL:** All queries to IBM Db2 use parameterized markers (`?`) to prevent SQL injection vulnerabilities.
- **Credentials Protection:** Database secrets and environment keys are excluded from git via `.gitignore`.
- **Security Notice:** All AI-generated code is untrusted output and must be reviewed and tested by the user before local execution.

---

## 🔍 IBM Db2 Verification Checklist Before Submission

Use this checklist to verify real IBM Db2 database connectivity:
- [x] Dedicated database module ([`database.py`](file:///c:/Users/raiak/OneDrive/Desktop/CodeFix-AI/database.py)) using official `ibm_db` driver.
- [x] Parameterized SQL statements used for all inserts (`INSERT INTO CODEFIX_HISTORY ... VALUES (?, ?, ...)`).
- [x] Parameterized SQL statements used for all selects (`WHERE ID = ?`, `WHERE SESSION_ID = ?`).
- [x] Parameterized SQL statements used for all deletes (`DELETE FROM CODEFIX_HISTORY WHERE ID = ?`).
- [x] Automatic schema initialization script available:
  ```powershell
  python -c "import database; ok, msg = database.init_db(); print('Db2 Schema Init:', ok, msg)"
  ```
- [x] Clean separation between mocked unit tests (`tests/test_database.py`) and optional live integration tests (`test_live_db2_connectivity_optional`).
- [x] Transparent Setup Mode: when credentials are not configured, clear UI banners indicate Setup Mode rather than faking database writes.

---

## ⚠️ Limitations & Future Improvements

### Current Limitations:
1. **Language Scope for Static AST:** Deterministic static AST parsing is built using Python's native `ast` engine. For JavaScript, Java, and C++, syntax analysis relies on AI semantic inspection unless native host compiler toolchains (e.g., ESLint, javac, clang-tidy) are installed.
2. **Local Model Hardware Dependency:** Model inference speed depends on host hardware (GPU/CPU) running Ollama.

### Future Improvements:
1. **Multi-File Workspace Support:** Ingest entire Git repositories or multi-file projects for project-wide refactoring.
2. **Automated Test Generation:** Automatically generate and run pytest/Jest unit test suites in an isolated sandbox container.
3. **Language Server Protocol (LSP) Integration:** Direct connection with language servers for real-time diagnostics across JavaScript, Java, and C++.

---

## ⚖️ Disclaimers

- **Independent Project:** CodeFix AI is an independent project built for educational and hackathon demonstration purposes. It is not officially endorsed or sponsored by IBM, Ollama, or any event organizer.
- **Code Execution Warning:** CodeFix AI generates code using local language models. Always review code before executing on your system.

---

## 🗺️ Implementation Roadmap Status

- [x] **Phase 1 — Foundation and UI:** Complete.
- [x] **Phase 2 — Static Analysis:** Complete.
- [x] **Phase 3 — Local AI Agent:** Complete.
- [x] **Phase 4 — IBM Db2 Integration:** Complete.
- [x] **Phase 5 — Testing, Hackathon Demonstration & Finalization:** Complete.
