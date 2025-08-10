from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GOOGLE_BOOKS_API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")
if not GOOGLE_BOOKS_API_KEY:
    raise RuntimeError("Missing GOOGLE_BOOKS_API_KEY in environment")

def mask(s: str) -> str:
    return s[:5] + "..." + s[-3:] if s and len(s) > 10 else "***"

@app.route("/books")
def books():
    # 1) Берём все параметры из запроса (q, maxResults, printType, orderBy, langRestrict и т.д.)
    params = dict(request.args)
    # 2) Гарантированно добавляем ключ (перезапишем, если пришёл с клиента)
    params["key"] = GOOGLE_BOOKS_API_KEY

    # Лог для диагностики
    print("Proxy → Google Books params:", {**params, "key": mask(params["key"])})

    r = requests.get("https://www.googleapis.com/books/v1/volumes", params=params)
    print("Google status:", r.status_code, "| body:", r.text[:300].replace("\n", " "))

    # Проксируем ответ как есть
    return (r.text, r.status_code, {"Content-Type": "application/json"})

@app.route("/")
def index():
    return jsonify({"status": "Google Books Proxy running"})
