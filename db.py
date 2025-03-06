import sqlite3

# DB初期化(ユーザ、投稿、返信、大喜利テーマ)
def init_db():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
        c.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, text TEXT, likes INTEGER DEFAULT 0)")
        c.execute("CREATE TABLE IF NOT EXISTS replies (id INTEGER PRIMARY KEY, post_id INTEGER, text TEXT, votes INTEGER DEFAULT 0)")
        c.execute("""
            CREATE TABLE IF NOT EXISTS likes 
                (user_id INTEGER,
                post_id INTEGER,
                PRIMARY KEY (user_id, post_id),  -- ユーザーと投稿の組み合わせで一意
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (post_id) REFERENCES posts(id)
            )
        """)
        # 1ユーザーが1投稿にできるいいね数を制限するためのリスト
        c.execute("CREATE TABLE IF NOT EXISTS daily_theme (date TEXT, post_id INTEGER)")
        conn.commit()

# データデータベースに接続する
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn