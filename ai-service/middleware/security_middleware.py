# ai-service/middleware/security_middleware.py

import re
from flask import request, jsonify, g
from services.sanitizer import sanitize_input


PII_PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone": r"\b\d{10}\b",
    "aadhaar": r"\b\d{12}\b",
    "password": r"password\s*[:=]\s*\S+"
}


def detect_pii(text):
    for key, pattern in PII_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            return key
    return None


def security_middleware():
    if request.method not in ["POST", "PUT", "PATCH"]:
        return None

    if not request.is_json:
        return jsonify({"error": "Invalid input"}), 400

    data = request.get_json(silent=True)

    # Fix JSON array / malformed body crash
    if not isinstance(data, dict) or not data:
        return jsonify({"error": "Invalid input"}), 400

    cleaned_data = {}

    for key, value in data.items():
        if not isinstance(value, str):
            return jsonify({"error": "Invalid input"}), 400

        pii_type = detect_pii(value)
        if pii_type:
            return jsonify({"error": "Invalid input"}), 400

        cleaned, error = sanitize_input(value)

        if error:
            return jsonify({"error": "Invalid input"}), 400

        cleaned_data[key] = cleaned

    # Correctly attach sanitized values for downstream routes
    g.cleaned_json = cleaned_data
    request.cleaned_json = cleaned_data

    return None