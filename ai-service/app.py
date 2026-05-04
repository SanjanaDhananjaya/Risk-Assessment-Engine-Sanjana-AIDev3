from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re

app = Flask(__name__)

# ✅ Rate Limiter (Day 4 + Day 10 verification)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)

# ✅ Security Headers (Day 8)
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# ✅ Input Sanitization (Day 3)
def sanitize_input(text):
    text = re.sub(r'<.*?>', '', text)  # remove HTML

    if re.search(r'ignore previous instructions|bypass|override|act as', text, re.IGNORECASE):
        return "PROMPT_INJECTION"

    if re.search(r'(SELECT|DROP|INSERT|DELETE|OR 1=1)', text, re.IGNORECASE):
        return "SQL_INJECTION"

    return text

# ✅ Health Check (used by backend)
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Flask API running"}), 200

# ✅ AI Check Endpoint (used in Day 6 + Day 10)
@app.route("/check-ai", methods=["GET"])
def check_ai():
    return jsonify({"status": "AI service is running"}), 200

# ✅ Analyze Endpoint (Day 2 + 3 + 5)
@app.route("/analyze", methods=["POST"])
@limiter.limit("10 per minute")
def analyze():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400

    result = sanitize_input(data["text"])

    if result == "PROMPT_INJECTION":
        return jsonify({"error": "Prompt injection detected"}), 400

    if result == "SQL_INJECTION":
        return jsonify({"error": "SQL injection detected"}), 400

    return jsonify({
        "risk_level": "LOW",
        "message": "Input is safe"
    }), 200

# ✅ Run App
if __name__ == "__main__":
    app.run(debug=True, port=5000)