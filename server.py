from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GOOGLE_BOOKS_API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")
if not GOOGLE_BOOKS_API_KEY:
    raise RuntimeError("❌ Missing GOOGLE_BOOKS_API_KEY in environment on Render")

def mask_key(key: str) -> str:
    return key[:5] + "..." + key[-3:] if key and len(key) > 10 else "***"

@app.route("/books")
def books():
    q = request.args.get("q")
    if not q:
        return jsonify({"error": "Missing 'q' parameter"}), 400

    params = dict(request.args)
    params["key"] = GOOGLE_BOOKS_API_KEY  # всегда наш ключ

    # Лог в консоль Render
    print("📤 Proxy → Google Books params:", {**params, "key": mask_key(params["key"])})

    try:
        r = requests.get("https://www.googleapis.com/books/v1/volumes", params=params, timeout=10)
        print("📥 Google status:", r.status_code)
        print("📄 Google body preview:", r.text[:300].replace("\n", " "))
        return (r.text, r.status_code, {"Content-Type": "application/json"})
    except Exception as e:
        print("❌ Proxy error:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return jsonify({"status": "Google Books Proxy running"})
