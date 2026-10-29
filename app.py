import os
import uuid
import logging
from typing import Dict, Any, Tuple
import requests
from flask import Flask, render_template, request, jsonify, session, abort

from config import Config
import analyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("CodeFixAI")

def create_app() -> Flask:
    """Application factory for CodeFix AI."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # In-memory session history store for Phase 1 demonstration
    # (Replaced by IBM Db2 in Phase 4)
    app.history_store: Dict[str, Dict[str, Any]] = {}

    # Register Context Processors
    @app.context_processor
    def inject_globals():
        return {
            "config": Config,
            "session_id": session.get("session_id", str(uuid.uuid4()))
        }

    # =========================================================================
    # Utility & Validation Helpers
    # =========================================================================
    def get_or_create_session_id() -> str:
        """Retrieve existing session ID or assign a new secure UUID."""
        if "session_id" not in session:
            session["session_id"] = str(uuid.uuid4())
        return session["session_id"]

    def validate_request_payload(data: Dict[str, Any], required_fields: list) -> Tuple[bool, str]:
        """Validate incoming JSON payload for size, types, and required fields."""
        if not data or not isinstance(data, dict):
            return False, "Request body must be a valid JSON object."

        # Check required fields
        for field in required_fields:
            if field not in data or not str(data.get(field, "")).strip():
                return False, f"Missing required parameter: '{field}'."

        # Validate language
        language = str(data.get("language", "")).lower()
        if language and language not in Config.SUPPORTED_LANGUAGES:
            return False, f"Unsupported language '{language}'. Supported: {', '.join(Config.SUPPORTED_LANGUAGES)}."

        # Validate mode
        mode = str(data.get("mode", "")).lower()
        if mode and mode not in Config.SUPPORTED_MODES:
            return False, f"Unsupported mode '{mode}'. Supported: {', '.join(Config.SUPPORTED_MODES)}."

        # Input length guardrail to prevent DOS / resource exhaustion
        total_len = len(str(data.get("prompt", ""))) + len(str(data.get("code", ""))) + len(str(data.get("error_message", "")))
        if total_len > Config.MAX_INPUT_CHARS:
            return False, f"Input payload exceeds maximum character limit of {Config.MAX_INPUT_CHARS} characters."

        return True, ""

    # =========================================================================
    # Core Application Routes
    # =========================================================================
    @app.route("/", methods=["GET"])
    def index():
        """Render the primary CodeFix AI workspace."""
        sess_id = get_or_create_session_id()
        return render_template("index.html", session_id=sess_id)

    @app.route("/api/status", methods=["GET"])
    def api_status():
        """Check live connectivity to Ollama and IBM Db2 configuration."""
        ollama_online = False
        available_models = []
        try:
            res = requests.get(f"{Config.OLLAMA_BASE_URL}/api/tags", timeout=1.5)
            if res.status_code == 200:
                ollama_online = True
                data = res.json()
                available_models = [m.get("name", "") for m in data.get("models", [])]
        except Exception:
            ollama_online = False

        return jsonify({
            "status": "online",
            "ollama_online": ollama_online,
            "ollama_host": Config.OLLAMA_BASE_URL,
            "model": Config.OLLAMA_MODEL,
            "models_available": available_models,
            "db2_configured": Config.is_db2_configured(),
            "max_input_chars": Config.MAX_INPUT_CHARS
        })

    # =========================================================================
    # Operation Endpoints (Phase 1 Baseline & Validation Layer)
    # =========================================================================
    @app.route("/generate", methods=["POST"])
    def generate_code():
        """Feature A: Write Code endpoint."""
        data = request.get_json(silent=True) or {}
        is_valid, err_msg = validate_request_payload(data, required_fields=["prompt", "language"])
        if not is_valid:
            return jsonify({"success": False, "error": err_msg}), 400

        language = data["language"].lower()
        prompt = data["prompt"].strip()
        sess_id = data.get("session_id", get_or_create_session_id())

        # In Phase 1: Validates and establishes contract response structure
        # (Connected to LangChain Ollama agent in Phase 3)
        record_id = str(uuid.uuid4())
        response_payload = {
            "id": record_id,
            "mode": "write",
            "language": language,
            "prompt": prompt,
            "generated_code": (
                f"# Generated {language.capitalize()} Solution for: {prompt}\n"
                f"# [Phase 1 Pipeline Verified: Ready for Ollama LangChain Integration]\n\n"
                f"def solution():\n"
                f"    \"\"\"\n"
                f"    Task: {prompt}\n"
                f"    \"\"\"\n"
                f"    print('CodeFix AI workspace ready. Connect Ollama in Phase 3.')\n\n"
                f"if __name__ == '__main__':\n"
                f"    solution()\n"
            ),
            "explanation": (
                f"### Solution Overview\n"
                f"Phase 1 Foundation and UI is active. Your request for language **{language}** has been validated against system constraints.\n\n"
                f"- **Task Prompt**: {prompt}\n"
                f"- **Model**: `{Config.OLLAMA_MODEL}`\n"
                f"- **Session ID**: `{sess_id}`"
            ),
            "diagnostics": [],
            "suggestions": [
                "Verify Ollama is installed and running (`ollama serve`).",
                "Ensure local model `qwen2.5-coder:3b` is pulled (`ollama pull qwen2.5-coder:3b`)."
            ],
            "model_name": Config.OLLAMA_MODEL
        }

        app.history_store[record_id] = {
            "id": record_id,
            "session_id": sess_id,
            "language": language,
            "mode": "write",
            "user_prompt": prompt,
            "original_code": "",
            "error_message": "",
            "generated_code": response_payload["generated_code"],
            "explanation": response_payload["explanation"],
            "model_name": Config.OLLAMA_MODEL,
            "created_at": "Just now"
        }

        return jsonify(response_payload)

    @app.route("/analyze", methods=["POST"])
    def analyze_code():
        """Feature B: Debug Code endpoint with deterministic Python AST static analysis."""
        data = request.get_json(silent=True) or {}
        is_valid, err_msg = validate_request_payload(data, required_fields=["code", "language"])
        if not is_valid:
            return jsonify({"success": False, "error": err_msg}), 400

        language = data["language"].lower()
        code = data["code"]
        prompt = data.get("prompt", "").strip()
        error_msg = data.get("error_message", "").strip()
        static_only = bool(data.get("static_only", False))
        sess_id = data.get("session_id", get_or_create_session_id())

        # Execute deterministic AST static analysis
        analysis = analyzer.analyze_code(code, language)
        diagnostics = analysis.get("diagnostics", [])

        # Formulate suggestions from static issues
        suggestions = []
        if analysis.get("syntax_error") and analysis["syntax_error"].get("suggestion"):
            suggestions.append(analysis["syntax_error"]["suggestion"])
        for w in analysis.get("warnings", []):
            if w.get("suggestion"):
                suggestions.append(w["suggestion"])

        if not suggestions:
            suggestions.append("Ensure required dependencies and libraries are imported.")
            suggestions.append("Verify runtime parameters and edge cases.")

        record_id = str(uuid.uuid4())

        if static_only:
            # Deterministic static analysis result without AI call
            explanation = (
                f"### Python AST Static Analysis Report\n"
                f"- **Syntax Valid**: {'Yes' if analysis.get('is_valid_syntax') else 'No (SyntaxError detected)'}\n"
                f"- **Static Warnings Found**: {len(analysis.get('warnings', []))}\n\n"
                f"{analysis.get('summary', '')}"
            )
            response_payload = {
                "id": record_id,
                "mode": "debug",
                "language": language,
                "prompt": prompt or "Deterministic Static AST Check",
                "generated_code": code,
                "explanation": explanation,
                "diagnostics": diagnostics,
                "suggestions": suggestions,
                "is_valid_syntax": analysis.get("is_valid_syntax", True),
                "model_name": "Deterministic Python AST"
            }
        else:
            # Full debug response (Phase 2 static analysis + Phase 3 ready for AI repair)
            explanation = (
                f"### Static Diagnostic Inspection\n"
                f"{analysis.get('summary', '')}\n\n"
                f"Static AST inspection completed. In Phase 3, this static diagnostic output is delivered "
                f"to the local Ollama `{Config.OLLAMA_MODEL}` agent to generate the targeted fix."
            )
            response_payload = {
                "id": record_id,
                "mode": "debug",
                "language": language,
                "prompt": prompt,
                "generated_code": code,
                "explanation": explanation,
                "diagnostics": diagnostics,
                "suggestions": suggestions,
                "is_valid_syntax": analysis.get("is_valid_syntax", True),
                "model_name": Config.OLLAMA_MODEL
            }

        app.history_store[record_id] = {
            "id": record_id,
            "session_id": sess_id,
            "language": language,
            "mode": "debug",
            "user_prompt": prompt,
            "original_code": code,
            "error_message": error_msg,
            "generated_code": code,
            "explanation": response_payload["explanation"],
            "model_name": response_payload["model_name"],
            "created_at": "Just now"
        }

        return jsonify(response_payload)

    @app.route("/improve", methods=["POST"])
    def improve_code():
        """Feature C: Improve Code endpoint."""
        data = request.get_json(silent=True) or {}
        is_valid, err_msg = validate_request_payload(data, required_fields=["code", "language"])
        if not is_valid:
            return jsonify({"success": False, "error": err_msg}), 400

        language = data["language"].lower()
        code = data["code"]
        prompt = data.get("prompt", "Improve readability and structure.").strip()
        sess_id = data.get("session_id", get_or_create_session_id())

        record_id = str(uuid.uuid4())
        response_payload = {
            "id": record_id,
            "mode": "improve",
            "language": language,
            "prompt": prompt,
            "generated_code": code,
            "explanation": (
                "### Refactoring Request Received\n"
                f"Optimization target: {prompt}\n\n"
                "Phase 3 LangChain agent will perform behavioral-preserving refactoring."
            ),
            "diagnostics": [],
            "suggestions": [
                "Check for time and memory complexity bottlenecks.",
                "Adhere to idiomatic naming conventions."
            ],
            "model_name": Config.OLLAMA_MODEL
        }

        app.history_store[record_id] = {
            "id": record_id,
            "session_id": sess_id,
            "language": language,
            "mode": "improve",
            "user_prompt": prompt,
            "original_code": code,
            "error_message": "",
            "generated_code": code,
            "explanation": response_payload["explanation"],
            "model_name": Config.OLLAMA_MODEL,
            "created_at": "Just now"
        }

        return jsonify(response_payload)

    @app.route("/explain", methods=["POST"])
    def explain_code():
        """Feature D: Explain Code endpoint."""
        data = request.get_json(silent=True) or {}
        is_valid, err_msg = validate_request_payload(data, required_fields=["code", "language"])
        if not is_valid:
            return jsonify({"success": False, "error": err_msg}), 400

        language = data["language"].lower()
        code = data["code"]
        prompt = data.get("prompt", "Explain code structure.").strip()
        sess_id = data.get("session_id", get_or_create_session_id())

        record_id = str(uuid.uuid4())
        response_payload = {
            "id": record_id,
            "mode": "explain",
            "language": language,
            "prompt": prompt,
            "generated_code": code,
            "explanation": (
                "### Code Structure Overview\n"
                f"Analyzing submitted {language} snippet.\n\n"
                "In Phase 3, the AI agent will deconstruct execution flow, key functions, time complexity, and limitations."
            ),
            "diagnostics": [],
            "suggestions": [
                "Examine algorithm design for potential recursion limits or unbound loops."
            ],
            "model_name": Config.OLLAMA_MODEL
        }

        app.history_store[record_id] = {
            "id": record_id,
            "session_id": sess_id,
            "language": language,
            "mode": "explain",
            "user_prompt": prompt,
            "original_code": code,
            "error_message": "",
            "generated_code": code,
            "explanation": response_payload["explanation"],
            "model_name": Config.OLLAMA_MODEL,
            "created_at": "Just now"
        }

        return jsonify(response_payload)

    @app.route("/chat", methods=["POST"])
    def chat_followup():
        """Feature E: Conversational follow-up endpoint."""
        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()
        if not message:
            return jsonify({"success": False, "error": "Follow-up message cannot be empty."}), 400

        current_code = data.get("current_code", "")
        language = data.get("language", "python")

        return jsonify({
            "success": True,
            "reply": f"Received follow-up: '{message}'. The conversation history pipeline is active.",
            "generated_code": current_code,
            "language": language
        })

    # =========================================================================
    # History Routes (Feature F)
    # =========================================================================
    @app.route("/history", methods=["GET"])
    def history():
        """List session and database saved records."""
        records = list(app.history_store.values())
        return render_template("history.html", records=records)

    @app.route("/history/<record_id>", methods=["GET"])
    def view_history_record(record_id: str):
        """View a single saved history record."""
        record = app.history_store.get(record_id)
        if not record:
            return render_template("error.html",
                                   status_code=404,
                                   error_title="Record Not Found",
                                   error_message=f"No saved record found with ID '{record_id}'.",
                                   suggestions=["Return to the History page to browse valid records."]), 404

        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify(record)
        return render_template("result.html", record=record)

    @app.route("/history/<record_id>/delete", methods=["POST"])
    def delete_history_record(record_id: str):
        """Delete a single saved history record."""
        if record_id in app.history_store:
            del app.history_store[record_id]
            return jsonify({"success": True, "message": "Record deleted successfully."})
        return jsonify({"success": False, "error": "Record not found."}), 404

    # =========================================================================
    # Error Handlers
    # =========================================================================
    @app.errorhandler(400)
    def bad_request_error(e):
        if request.is_json:
            return jsonify({"success": False, "error": "Bad request", "details": str(e)}), 400
        return render_template("error.html",
                               status_code=400,
                               error_title="Invalid Request",
                               error_message="The server could not understand the request due to invalid syntax or parameters.",
                               suggestions=["Check the form fields and ensure input does not exceed character limits."]), 400

    @app.errorhandler(404)
    def not_found_error(e):
        if request.is_json:
            return jsonify({"success": False, "error": "Resource not found"}), 404
        return render_template("error.html",
                               status_code=404,
                               error_title="Page Not Found",
                               error_message="The requested URL was not found on this server.",
                               suggestions=["Double check the URL or use the navigation bar to return to the Workspace."]), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        logger.error(f"Internal server error: {e}", exc_info=True)
        if request.is_json:
            return jsonify({"success": False, "error": "Internal server error"}), 500
        return render_template("error.html",
                               status_code=500,
                               error_title="Internal Application Error",
                               error_message="An unexpected condition was encountered on the server.",
                               suggestions=[
                                   "Verify that the Flask application and environment variables are properly configured.",
                                   "Check server console logs for detailed diagnostic information."
                               ]), 500

    return app


# Application Entry Point
app = create_app()

if __name__ == "__main__":
    port = Config.PORT
    debug = Config.DEBUG
    logger.info(f"Starting CodeFix AI on port {port} (Debug: {debug})...")
    app.run(host="0.0.0.0", port=port, debug=debug)
