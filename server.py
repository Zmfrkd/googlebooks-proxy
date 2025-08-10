from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GOOGLE_BOOKS_API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")

if not GOOGLE_BOOKS_API_KEY:
    # Без ключа не запускаемся — так сразу видно проблему в логах Render
    raise RuntimeError("Missing GOOGLE_BOOKS_API_KEY in environment")

def mask(s: str) -> str:
    return s[:5] + "..." + s[-3:] if s and len(s) > 10 else "***"

@app.route("/books")
def books():
    # Берем все входные параметры как есть (q, maxResults, langRestrict и т.д.)
    params = dict(request.args)
    # Гарантированно добавляем ключ (перезаписываем, если вдруг передали с клиента)
    params["key"] = GOOGLE_BOOKS_API_KEY

    # В логи Render: что именно отправляем (ключ маскируем)
    print("Proxy → Google Books params:", {**params, "key": mask(params["key"])})

    r = requests.get("https://www.googleapis.com/books/v1/volumes", params=params)
    # Проксируем ответ как есть (JSON+статус)
    return (r.text, r.status_code, {"Content-Type": "application/json"})

@app.route("/")
def index():
    return jsonify({"status": "Google Books Proxy running"})
