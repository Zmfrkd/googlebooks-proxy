from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GOOGLE_BOOKS_API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")

@app.route("/books")
def books():
    query_params = dict(request.args)
    query_params["key"] = GOOGLE_BOOKS_API_KEY  # всегда добавляем ключ
    r = requests.get("https://www.googleapis.com/books/v1/volumes", params=query_params)
    return jsonify(r.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
