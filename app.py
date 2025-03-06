from flask import Flask, request, jsonify, render_template,session
from datetime import datetime
import sqlite3
# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)
app.secret_key = 'key'

# DB初期化
def init_db():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, text TEXT, likes INTEGER DEFAULT 0, created_at TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS replies (id INTEGER PRIMARY KEY, post_id INTEGER, text TEXT, votes INTEGER DEFAULT 0, created_at TEXT)")
        conn.commit()
init_db()

# ルートURLにアクセスしたときの処理
@app.route('/')
def home():
    return render_template('index.html')

# データベースに接続し、データを挿入する関数
def insert_post(text):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 現在の日時
    c.execute('INSERT INTO posts (text, created_at) VALUES (?, ?)', (text, created_at))
    conn.commit()
    conn.close()

def insert_post_reply(post_id, text):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 現在の日時
    c.execute('INSERT INTO replies (post_id, text, created_at) VALUES (?, ?, ?)', (post_id, text, created_at))
    conn.commit()
    conn.close()


# 投稿を取得
@app.route("/posts", methods=["GET"])
def get_posts():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = [{"id": row[0], "text": row[1], "likes": row[2], "created_at": row[3]} for row in c.fetchall()]
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
    
# 特定の投稿に対するリプライを取得
@app.route("/replies/<int:post_id>", methods=["GET"])
def get_replies(post_id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM replies WHERE post_id = ? ORDER BY id DESC", (post_id,))
    replies = [{"id": row[0], "text": row[2], "votes": row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify(replies)

# 回答
@app.route("/replies", methods=["POST"])
def add_reply():
    data = request.get_json()
    text = data.get('text')
    post_id = data.get('post_id')
    if not post_id or not text:
        return jsonify({'message': 'Invalid input'}), 400

    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO replies (post_id, text) VALUES (?, ?)", (post_id, text))
        conn.commit()

    return jsonify({'message': 'Reply created successfully'}), 201

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
        return jsonify({'error': 'Post not found'}), 404
    return

# リプライに投票
@app.route("/replies/<int:reply_id>/vote", methods=["POST"])
def vote_reply(reply_id):
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("UPDATE replies SET votes = votes + 1 WHERE id = ?", (reply_id,))
        conn.commit()
    return jsonify({'message': 'Reply voted successfully'}), 200

# すべてのリプライを取得（並べ替え機能付き）
@app.route("/replies", methods=["GET"])
def get_all_replies():
    sort_order = request.args.get('sort_order', 'newest')  # デフォルトは新しい順

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # リプライを取得
    c.execute("SELECT * FROM replies")  # カラムを全て取得
    rows = c.fetchall()

    # デバッグ用に結果を確認
    print("Rows:", rows)

    replies = [{"id": row[0], "text": row[2], "votes": row[3], "created_at": row[4]} for row in rows]
    def parse_datetime(value):
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S") if value else datetime.min

    replies = [
        {"id": row[0], "text": row[2], "votes": row[3], "created_at": parse_datetime(row[4])}
        for row in rows
    ]
    # 並べ替え
    if sort_order == 'most-voted':
        replies.sort(key=lambda x: x['votes'], reverse=True)
    elif sort_order == 'newest':
        replies.sort(key=lambda x: x['created_at'], reverse=True)

    conn.close()
    return jsonify(replies)


# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True)