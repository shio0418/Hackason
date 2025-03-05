from flask import Flask, request, jsonify, render_template
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
import random
import datetime

app = Flask(__name__)

# DB初期化
def init_db():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, text TEXT, likes INTEGER DEFAULT 0)")
        c.execute("CREATE TABLE IF NOT EXISTS replies (id INTEGER PRIMARY KEY, post_id INTEGER, text TEXT, votes INTEGER DEFAULT 0)")
        c.execute("CREATE TABLE IF NOT EXISTS daily_theme (date TEXT, post_id INTEGER)")
        conn.commit()

init_db()
@app.route("/")
def index():
    return render_templete("index.html")

# # 投稿
# @app.route("/posts", methods=["POST"])
# def add_post():
#     data = request.json
#     with sqlite3.connect("database.db") as conn:
#         conn.execute("INSERT INTO posts (text) VALUES (?)", (data["text"],))
#         conn.commit()
#     return jsonify({"message": "投稿完了"})

# # 大喜利回答
# @app.route("/replies", methods=["POST"])
# def add_reply():
#     data = request.json
#     with sqlite3.connect("database.db") as conn:
#         conn.execute("INSERT INTO replies (post_id, text) VALUES (?, ?)", (data["post_id"], data["text"]))
#         conn.commit()
#     return jsonify({"message": "回答完了"})

if __name__ == "__main__":
    app.run(debug=True)
