from flask import Flask
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
    return 'Hello, Flask!'
# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True)