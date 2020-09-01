from flask import(
Blueprint,render_template,request
)
import tweepy,time
from app.userdb import get_db,close_db
from app.function import like_tweepy,get_sorted_df,get_grouped_df,get_profile,retweet_tweepy,follow_tweepy,like_tweepy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from collections import defaultdict

db = get_db()
# モデルに関する設定
class User(UserMixin, db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))
 
    # モデルからインスタンスを生成するときに使います。(利便性を高めるため)
    # passwordの暗号化も自動で行うことができるので、安全性も高めることができます。
    @classmethod
    def from_args(cls, name: str, email: str, password: str):
        instance = cls()
        instance.name = name
        instance.email = email
        if password is not None:
            # passwordがあれば暗号化します。
            instance.hash_password(password)
        return instance
 
    # 暗号化するためのメソッド。
    def hash_password(self, clean_password):
        self.password = generate_password_hash(str(clean_password), method='sha256')
 
    # 登録したpasswordとユーザーがログインフォームで入力したパスワードが正しいかどうかのチェックを行うメソッド
    def check_password(self, clean_password):
        return check_password_hash(self.password, clean_password)
        