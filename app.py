from flask import Flask
# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)
# ルートURLにアクセスしたときの処理
@app.route('/')
def home():
    return 'Hello, Flask!'
# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True)