# heroku-appディレクトリにある__init__.pyの中で設定したflaskアプリであるappをimportしている
from app import app

# flaskサーバーを起動
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)