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
    # 1. 投稿が存在するかを確認する（postsテーブルの該当するpost_idを検索）
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = c.fetchone()
    if post:
        c. execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
        conn.commit()
        conn.close()
        return jsonify({'messaage': 'Post liked sucessfully'}), 200
    else:
        conn.close()
        #投稿が存在しない場合のエラーメッセージ
        return jsonify({})
    return


# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True)