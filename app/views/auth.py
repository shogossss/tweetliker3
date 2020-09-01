from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.service import auth_service
import tweepy,time
from app.userdb import get_db,close_db
from app.function import like_tweepy,get_sorted_df,get_grouped_df,get_profile,retweet_tweepy,follow_tweepy,like_tweepy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

auth = Blueprint('auth', __name__)

@auth.route('/')
# @login_required
def index():
    return render_template('auth/login.html')

# signupページと、postするページを共通化。
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    else:
        user = auth_service.signup(request.form)
        if user:
            flash('このユーザー名は既に登録されています。')
            return redirect(url_for('index'))
        flash('新規登録に成功しました。')
        return redirect(url_for('index'))
 
 
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        user = auth_service.login(request.form)
        if not user:
            flash('メールアドレスもしくはパスワードに誤りがあります。')
            return render_template('auth.login')
        flash('ログインしました。')
        return redirect(url_for('index'))

@auth.route('/create_user', methods = ["GET","POST"])
def create_user():
    return render_template('auth/create_user.html')

@auth.route('/login4', methods = ["GET" , "POST"])
def login4():
    if request.method == 'POST':
        try:
            # global username,password,CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_SECRET
            username = request.form['username']
            password = request.form['password']
            CONSUMER_KEY  = request.form['ck']
            CONSUMER_SECRET = request.form['cs']
            ACCESS_TOKEN = request.form['at']
            ACCESS_SECRET = request.form['ats']
            return render_template(
            'auth/check.html',
            username=username,
            password=password,
            ck=CONSUMER_KEY,
            cs=CONSUMER_SECRET,
            at=ACCESS_TOKEN,
            ats=ACCESS_SECRET
            )

        except Exception as e:
            print(e)
            return render_template(
            'auth/create_user.html'
            )
    else:
        return render_template('auth/create_user.html')

@auth.route('/login2', methods = ["GET" , "POST"])
def login2():
    if request.method == 'POST':
        try:
            db = get_db()
            username = request.form['username']
            password = request.form['password']
            print(password)
            CONSUMER_KEY  = request.form['ck']
            CONSUMER_SECRET = request.form['cs']
            ACCESS_TOKEN = request.form['at']
            ACCESS_SECRET = request.form['ats']
            db.execute("INSERT INTO user (username,password) values(?,?)", (username,generate_password_hash(str(password), method='sha256')))
            db.execute("INSERT INTO api (ck,cs,at,ats) values(?,?,?,?)", (CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_SECRET))
            # #tweepy
            # auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            # auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
            # #グローバル変数
            # global api
            # #APIインスタンスを作成
            # api = tweepy.API(auth)
            db.commit()
            close_db()
        # index.html をレンダリングする
            return render_template('auth/login.html')

        except Exception as e:
            print(e)
            message = "そのusernameはすでに使われております"
            username = request.form['username']
            password = request.form['password']
            CONSUMER_KEY  = request.form['ck']
            CONSUMER_SECRET = request.form['cs']
            ACCESS_TOKEN = request.form['at']
            ACCESS_SECRET = request.form['ats']
            return render_template(
            'auth/create_user2.html',
            message=message,
            username=username,
            password=password,
            ck=CONSUMER_KEY,
            cs=CONSUMER_SECRET,
            at=ACCESS_TOKEN,
            ats=ACCESS_SECRET
            )
    else:
        return render_template('auth/login.html')

@auth.route('/login3', methods = ["GET" , "POST"])
def login3():
    return render_template(
    'auth/create_user2.html',
    username=username,
    password=password,
    ck=CONSUMER_KEY,
    cs=CONSUMER_SECRET,
    at=ACCESS_TOKEN,
    ats=ACCESS_SECRET
    )