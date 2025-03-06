from flask import Flask, request, jsonify, render_template,session
from auth import auth
from db import init_db
import sqlite3
# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)
app.secret_key = 'key'

init_db()
app.register_blueprint(auth)

# ルートURLにアクセスしたときの処理
@app.route('/')
def home():
    return render_template('index.html')

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

# 投稿を取得
@app.route("/posts", methods=["GET"])
def get_posts():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row #辞書型で取得
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = [{"id": row[0], "text": row[1], "likes": row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify(posts)
# 投稿
@app.route("/posts", methods=["POST"])
def add_post():
    ##ここを考える
    data = request.get_json()
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
    data = request.json
    text = data.get('text')
    post_id = data.get('post_id')
    if post_id < 0:
        return jsonify({'message': 'Invalid post_id'}), 400
    elif text:
        insert_post_reply(post_id,text)
        return jsonify({'message': 'Post created successfully'}), 201
    else:
        return jsonify ({'message': 'No text provided'}), 400

# いいね
@app.route("/posts/<int:post_id>/like", methods=["POST"])
def like_post(post_id):
    # 1. ログイン中のユーザーidを取得、取得できなければエラー
    user_id = session.get('user_id') 
    if not user_id:
        return jsonify({'message': 'User not logged in'}), 401

    # 2. 投稿が存在するかを確認する（postsテーブルの該当するpost_idを検索）
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = c.fetchone()
    
    if not post:
        conn.close()
        #投稿が存在しない場合のエラーメッセージ
        return jsonify({'error': 'Post not found'}), 404


    c.execute("SELECT * FROM likes WHERE id = ? AND post_id = ?", (user_id, post_id))
    exsisting_like = c.fetchone()
    # 3. いいねをすでにしている場合のエラーメッセージ
    if exsisting_like:
        conn.close()
        return jsonify({'message': 'You have already liked this post'}), 400

    c.execute("INSERT INTO likes (user_id, post_id) VALUES (?, ?)", (user_id, post_id))
    c. execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return jsonify({'messaage': 'Post liked sucessfully'}), 200

# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True)


# ID,password ログインできるか確認