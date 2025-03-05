<<<<<<< Updated upstream
from flask import Flask, request, jsonify, render_template

=======
from flask import Flask, request
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream

# データベースに接続し、データを挿入する関数
def insert_post(text):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO posts (text) VALUES (?)', (text,))
    conn.commit()
    conn.close()

def insert_post_reply(post_id,text):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO replies (post_id,text) VALUES (?,?)', (post_id,text,))
    conn.commit()
    conn.close()

=======
    
>>>>>>> Stashed changes
# 投稿
@app.route("/posts", methods=["POST"])
def add_post():
    ##ここを考える
<<<<<<< Updated upstream
    data = request.json
    text = data.get('text')
    if text:
        insert_post(text)
        return jsonify({'message': 'Post created successfully'}), 201
    else:
        return jsonify ({'message': 'No text provided'}), 400

=======
    return
>>>>>>> Stashed changes
    
# 大喜利回答
@app.route("/replies", methods=["POST"])
def add_reply():
    data = request.json
<<<<<<< Updated upstream
    text = data.get('text')
    post_id = data.get('post_id')
    if post_id < 0:
        return jsonify({'message': 'Invalid post_id'}), 400
    elif text:
        insert_post_reply(post_id,text)
        return jsonify({'message': 'Post created successfully'}), 201
    else:
        return jsonify ({'message': 'No text provided'}), 400
=======

    post_id = data.get("")
    
    #ここを考える
    return
>>>>>>> Stashed changes

# いいね
@app.route("/posts/<int:post_id>/like", methods=["POST"])
def like_post(post_id):
    #ここを考える
    return


# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True)