from flask import Flask, request, jsonify, render_template

import sqlite3
# Flaskアプリケーションのインスタンスを作成
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

# ルートURLにアクセスしたときの処理
@app.route('/')
def home():
    data = request.json

    return 'Hello, Flask!'

# データベースに接続し、データを挿入する関数
def insert_post(text):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO posts (text) VALUES (?)', (text,))
    conn.commit()
    conn.close()
# 投稿
@app.route("/posts", methods=["POST"])
def add_post():
    ##ここを考える
    data = request.json
    text = data.get('text')
    if text:
        insert_post(text)
        return jsonify({'message': 'Post created successfully'}), 201
    else:
        return jsonify ({'message': 'No text provided'}), 400

    print(data)

    return
    
# 大喜利回答
@app.route("/replies", methods=["POST"])
def add_reply():
    #ここを考える
    return

# いいね
@app.route("/posts/<int:post_id>/like", methods=["POST"])
def like_post(post_id):
    #ここを考える
    return


# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True)