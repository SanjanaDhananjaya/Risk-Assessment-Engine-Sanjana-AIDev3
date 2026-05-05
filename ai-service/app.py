from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)

# Secret key for JWT
app.config['SECRET_KEY'] = 'your_secret_key_here'

# -------------------------------
# Rate Limiter
# -------------------------------
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# -------------------------------
# Security Headers
# -------------------------------
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# -------------------------------
# Dummy User (for demo)
# -------------------------------
USER_DATA = {
    "username": "admin",
    "password": "password123"
}

# -------------------------------
# JWT Token Required Decorator
# -------------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'error': 'Invalid or expired token'}), 401

        return f(*args, **kwargs)

    return decorated

# -------------------------------
# Login Route
# -------------------------------
@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()

    if not auth or not auth.get("username") or not auth.get("password"):
        return jsonify({"error": "Missing credentials"}), 400

    if auth["username"] == USER_DATA["username"] and auth["password"] == USER_DATA["password"]:
        token = jwt.encode({
            'user': auth["username"],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({
            "token": token
        })

    return jsonify({"error": "Invalid credentials"}), 401

# -------------------------------
# Protected Analyze Route
# -------------------------------
@app.route('/analyze', methods=['POST'])
@token_required
@limiter.limit("10 per minute")
def analyze():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400

    text = data["text"]
    lower_text = text.lower()

    # XSS Detection
    dangerous_patterns = ["<script>", "javascript:", "onerror=", "alert("]

    for pattern in dangerous_patterns:
        if pattern in lower_text:
            return jsonify({"error": "Potential XSS detected"}), 400

    # Risk logic
    risk_keywords = ["attack", "hack", "malware", "phishing", "breach"]
    score = sum(10 for word in risk_keywords if word in lower_text)

    if score >= 30:
        level = "High Risk"
    elif score >= 10:
        level = "Medium Risk"
    else:
        level = "Low Risk"

    return jsonify({
        "message": "Analysis successful",
        "risk_score": score,
        "risk_level": level
    })

# -------------------------------
# Rate Limit Handler
# -------------------------------
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Too many requests"
    }), 429

# -------------------------------
# Run App
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)