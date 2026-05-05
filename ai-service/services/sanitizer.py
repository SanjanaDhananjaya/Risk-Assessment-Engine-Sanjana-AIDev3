# ai-service/services/sanitizer.py

import re
import html
import urllib.parse
import unicodedata


def normalize_text(text):
    text = urllib.parse.unquote_plus(text)
    text = unicodedata.normalize("NFKC", text)
    return text


def sanitize_input(text):
    if not text or not isinstance(text, str):
        return None, "Invalid input"

    normalized_text = normalize_text(text)

    # Safer than regex stripping: escapes nested/broken HTML safely
    cleaned_text = html.escape(normalized_text, quote=True)

    lower_text = normalized_text.lower()

    # Stronger prompt injection detection
    dangerous_patterns = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "disregard previous instructions",
        "reveal system prompt",
        "show system prompt",
        "system prompt",
        "developer message",
        "bypass",
        "override",
        "jailbreak",
        "act as",
        "pretend to be",
        "disable safety",
        "forget instructions"
    ]

    for pattern in dangerous_patterns:
        if pattern in lower_text:
            return None, "Invalid input"

    # Block dangerous URI schemes
    blocked_uri_patterns = [
        "javascript:",
        "data:text/html",
        "vbscript:"
    ]

    for pattern in blocked_uri_patterns:
        if pattern in lower_text:
            return None, "Invalid input"

    # Less aggressive SQL detection: blocks real attack-like SQL, not normal prose
    sql_patterns = [
        r"\bdrop\s+table\b",
        r"\bdelete\s+from\b",
        r"\binsert\s+into\b",
        r"\bselect\s+\*\s+from\b",
        r"\bunion\s+select\b",
        r"\bor\s+1\s*=\s*1\b",
        r"--",
        r"/\*",
        r"\*/"
    ]

    for pattern in sql_patterns:
        if re.search(pattern, lower_text, re.IGNORECASE):
            return None, "Invalid input"

    return cleaned_text, None