import re
from flask import request, jsonify

# 🔐 Regex patterns
HTML_PATTERN = re.compile(r"<.*?>")

PROMPT_INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"bypass",
    r"override",
    r"jailbreak",
    r"act as"
]

SQL_INJECTION_PATTERNS = [
    r"select\s",
    r"drop\s",
    r"insert\s",
    r"delete\s",
    r"or\s+1=1"
]

# 🔐 NEW — PII Detection Patterns (Day 9)
PII_PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone": r"\b\d{10}\b",
    "aadhaar": r"\b\d{12}\b",
    "password": r"password\s*[:=]\s*\S+"
}


def sanitize_input(text):
    return re.sub(HTML_PATTERN, "", text)


def detect_pattern(text, patterns):
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def detect_pii(text):
    for key, pattern in PII_PATTERNS.items():
        if re.search(pattern, text):
            return key
    return None


def security_middleware():
    # ✅ Skip GET requests
    if request.method == "GET":
        return None

    # ✅ Must be JSON
    if not request.is_json:
        return jsonify({"error": "Invalid content type"}), 400

    data = request.get_json()

    # ✅ Empty check
    if not data:
        return jsonify({"error": "Empty request body"}), 400

    cleaned_data = {}

    for key, value in data.items():
        if not isinstance(value, str):
            return jsonify({"error": "All fields must be strings"}), 400

        # 🔹 Sanitize HTML
        cleaned = sanitize_input(value)

        # 🔹 Detect Prompt Injection
        if detect_pattern(cleaned, PROMPT_INJECTION_PATTERNS):
            return jsonify({
                "error": "Prompt injection detected",
                "field": key
            }), 400

        # 🔹 Detect SQL Injection
        if detect_pattern(cleaned, SQL_INJECTION_PATTERNS):
            return jsonify({
                "error": "SQL injection detected",
                "field": key
            }), 400

        # 🔴 NEW — Detect PII (Day 9)
        pii_type = detect_pii(cleaned)
        if pii_type:
            return jsonify({
                "error": f"PII detected ({pii_type})",
                "field": key
            }), 400

        cleaned_data[key] = cleaned

    # ✅ Attach safe data
    request.cleaned_json = cleaned_data

    return None