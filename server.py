from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Пропиши свой ключ тут
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY", "ТВОЙ_КЛЮЧ")

@app.route("/books")
def books():
    q = request.args.get("q")
    if not q:
        return jsonify({"error": "Missing 'q' parameter"}), 400

    params = {
        "q": q,
        "maxResults": request.args.get("maxResults", 10),
        "printType": "books",
        "orderBy": "relevance",
        "key": GOOGLE_BOOKS_API_KEY
    }

    r = requests.get("https://www.googleapis.com/books/v1/volumes", params=params)
    return (r.text, r.status_code, {"Content-Type": "application/json"})

@app.route("/")
def index():
    return jsonify({"status": "Google Books Proxy running"})
