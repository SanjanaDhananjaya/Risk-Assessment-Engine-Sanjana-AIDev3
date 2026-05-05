# ai-service/app.py

from flask import Flask, jsonify, g, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded

from middleware.security_middleware import security_middleware

app = Flask(__name__)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)


@app.before_request
def before_request():
    return security_middleware()


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "AI service running"}), 200


@app.route("/test", methods=["POST"])
def test():
    data = g.get("cleaned_json", {})

    return jsonify({
        "message": "Safe input received",
        "cleaned_text": data.get("text", "")
    }), 200


@app.route("/analyze", methods=["POST"])
@limiter.limit("10 per minute")
def analyze():
    data = g.get("cleaned_json", {})
    text = data.get("text", "")

    score = 0
    risk_keywords = ["attack", "hack", "malware", "phishing", "breach"]

    for word in risk_keywords:
        if word in text.lower():
            score += 10

    if score >= 30:
        level = "High Risk"
    elif score >= 10:
        level = "Medium Risk"
    else:
        level = "Low Risk"

    return jsonify({
        "message": "Analysis successful",
        "risk_score": score,
        "risk_level": level,
        "cleaned_text": text
    }), 200


@app.route("/generate-report", methods=["POST"])
@limiter.limit("10 per minute")
def generate_report():
    data = g.get("cleaned_json", {})
    text = data.get("text", "")

    return jsonify({
        "title": "Risk Assessment Report",
        "summary": "Report generated successfully",
        "input_reviewed": text,
        "recommendations": [
            "Continue monitoring risk indicators",
            "Apply access controls",
            "Review security logs regularly"
        ]
    }), 200


@app.errorhandler(RateLimitExceeded)
def handle_rate_limit(e):
    return jsonify({
        "error": "Too many requests",
        "retry_after": str(e.description)
    }), 429


@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({"error": "Internal error"}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=False)