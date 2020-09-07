from flask import(
Blueprint,render_template,request,session,redirect, url_for,
)
import tweepy,time
from app.userdb import get_db,close_db
from app.function import like_tweepy,get_sorted_df,get_grouped_df,get_profile,retweet_tweepy,follow_tweepy,like_tweepy,getTweetBySearch,sessget
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

users = Blueprint('users', __name__)
@users.route('/tweet', methods = ["GET" , "POST"])
def tweet():
    if request.method == 'POST':
        try:
            db = get_db()
            d = db.cursor()
            error_message = None
            # pass1=[]
            # user1=[]
            username  = request.form['username']
            password = request.form['pass']
            user = d.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()
            if user is None:
                error_message = 'ユーザー名が正しくありません'
            elif not check_password_hash(user['password'], password):
                error_message = 'パスワードが正しくありません'
            
            if error_message is not None:
                # エラーがあればそれを表示したうえでログイン画面に遷移
                return render_template(
                'auth/login.html',
                message2=error_message
                )
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            db.commit()
            close_db()
            return redirect(url_for('auth.index'))

        except Exception as e:
            print(e)
            message2 = "usernameが間違っております"
            return render_template(
            'auth/login.html',
            message2 = message2
            )
    else:
        return render_template('auth/login.html')

@users.route('/tweetaction', methods =["GET","POST"])
def tweetaction():
    if request.method == 'POST':
       query = request.form['query']# formのname = "query"を取得
       cnt = int(request.form['count'])
       button = request.form['button']
       userid = session["user_id"]
       api = sessget(userid)
       posts = []
       try:
           if button == "like":
               posts = like_tweepy(userid,query,cnt,api,posts)
           if button == "retweet":
               posts = retweet_tweepy(userid,query,cnt,api,posts)
           if button == "follow":
               posts = follow_tweepy(userid,query,cnt,api,posts)
           # grouped_df = get_grouped_df(tweets_df)
           # sorted_df = get_sorted_df(tweets_df)
           # 送られてきたものを返すしなきゃ返されない
           return render_template(
               'tweet/index.html',
               query = query,
               count = cnt,
               # profile=get_profile(user_id),
               posts = posts
               # grouped_df = grouped_df,
               # sorted_df = sorted_df
               )
       except Exception as e:
            print(e)
            messages = "APIが違います"
            title = "APIエラー"
            return render_template(
            'auth/login.html',
            message2 = messages,
            title = title
            )

    else:
            return render_template('index.html')

@users.route('/searchtweet', methods =["GET","POST"])
def search_tweet():
    return render_template('tweet/search_tweet.html')

@users.route('/search_tweet2', methods =["GET","POST"])
def search_tweet2():
    if request.method == 'POST':
       query = request.form['query']
       cnt = int(request.form['count'])
       button = request.form['button']
       startdate = request.form['startdate']
       enddate = request.form['enddate']
       posts2 = []
       userid = session["user_id"]
       api = sessget(userid)
       try:
           if button == "search":
               posts2 = getTweetBySearch(userid, query, startdate, enddate, cnt, api, posts2)
           # 送られてきたものを返すしなきゃ返されない
           return render_template(
               'tweet/search_tweet.html',
               yydd1 = startdate,
               yydd2 = enddate,
               word = query,
               posts2 = posts2
               )
       except Exception as e:
            print(e)
            messages = "APIが違います"
            title = "APIエラー"
            return render_template(
            'auth/login.html',
            message2 = messages,
            title = title
            )

    else:
            return render_template('index.html')

@users.route('/logcheck', methods =["GET","POST"])
def logcheck():
    db = get_db()
    c = db.cursor()
    datas=[]
    c.execute("select * from tweet")
    userid = session["user_id"]
    # print(userid)
    for d3 in c:
        data = {}
        if(d3["id"] == userid):
            data["created_at"] = str(d3["created_at"])
            data["text"] = str(d3["text"])
            data["user_id"] = str(d3["user_id"])
            data["fav"] = str(d3["fav"])
            data["retweet"] = str(d3["retweet"])
            data["action"] = str(d3["action"])
            datas.append(data)
    close_db()
    return render_template(
    'tweet/logcheck.html',
    posts=datas
    )

@users.route('/anary', methods =["GET","POST"])
def anarylog():
    # db = get_db()
    # c = db.cursor()
    # datas=[]
    # c.execute("select * from tweet")
    # for d3 in c:
    #     data = {}
    #     if(d3["id"]==id):
    #         print(str(d3["created_at"]))
    #         data["created_at"] = str(d3["created_at"])
    #         data["text"] = str(d3["text"])
    #         data["user_id"] = str(d3["user_id"])
    #         data["fav"] = str(d3["fav"])
    #         data["retweet"] = str(d3["retweet"])
    #         data["action"] = str(d3["action"])
    #         datas.append(data)
    # close_db()
    return render_template(
    'tweet/anary.html',
    # posts=datas
    )

columns = [
   "tweet_id",
   "created_at",
   "text",
   "fav",
   "retweets"
   ]

@users.route('/anary2', methods = ["GET" , "POST"])
def anary2():
   if request.method == 'POST':
       user_id = request.form['user_id']
       tweets_df = get_tweets_df(user_id)
       grouped_df = get_grouped_df(tweets_df)
       sorted_df = get_sorted_df(tweets_df)
       sorted_df2 = get_sorted_df2(tweets_df)
       return render_template(
           'tweet/anary.html',
           profile=get_profile(user_id),
           tweets_df = tweets_df,
           grouped_df = grouped_df,
           sorted_df = sorted_df,
           sorted_df2 = sorted_df2
           )
   else:
       return render_template('tweet/anary.html')

@users.route('/anary3', methods = ["GET" , "POST"])
def anary3():
   if request.method == 'POST':
       user_id = request.form['user_id']
       tweets_df = get_tweets_df(user_id)
       grouped_df = get_grouped_df(tweets_df)
       sorted_df = get_sorted_df(tweets_df)
       sorted_df2 = get_sorted_df2(tweets_df)
       return render_template(
           'tweet/anary.html',
           profile=get_profile(user_id),
           tweets_df = tweets_df,
           grouped_df = grouped_df,
           sorted_df = sorted_df,
           sorted_df2 = sorted_df2
           )
   else:
       return render_template('tweet/anary.html')

def get_tweets_df(user_id):
   userid = session["user_id"]
   api = sessget(userid)
   tweets_df = pd.DataFrame(columns=columns) #1
   for tweet in tweepy.Cursor(api.user_timeline,screen_name = user_id, exclude_replies = True).items(): #2
       try:
           if not "RT @" in tweet.text: #3
               se = pd.Series([ #4
                       tweet.id,
                       tweet.created_at,
                       tweet.text.replace('\n',''),
                       tweet.favorite_count,
                       tweet.retweet_count
                   ]
                   ,columns
                   )
               tweets_df = tweets_df.append(se,ignore_index=True) #5
       except Exception as e:
           print (e)
   tweets_df["created_at"] = pd.to_datetime(tweets_df["created_at"]) #6
   return tweets_df #7

def get_profile(user_id):
   userid = session["user_id"]
   api = sessget(userid)
   user = api.get_user(screen_name= user_id) #1
   profile = { #2
       "id": user.id,
       "user_id": user_id,
       "image": user.profile_image_url,
       "description": user.description # 自己紹介文の取得
   }
   return profile #3

def get_grouped_df(tweets_df):
   grouped_df = tweets_df.groupby(tweets_df.created_at.dt.date).sum().sort_values(by="created_at", ascending=False)
   return grouped_df

def get_sorted_df(tweets_df):
   sorted_df = tweets_df.sort_values(by="fav", ascending=False)
   return sorted_df

def get_sorted_df2(tweets_df):
   sorted_df = tweets_df.sort_values(by="retweets", ascending=False)
   return sorted_df


# @bp.route('/anary', methods =["GET","POST"])
# def anary():
#     db = get_db()
#     c = db.cursor()
#     datas=[]
#     c.execute("select * from tweet")
#     for d3 in c:
#         data = {}
#         if(d3["id"]==id):
#             print(str(d3["created_at"]))
#             data["created_at"] = str(d3["created_at"])
#             data["text"] = str(d3["text"])
#             data["user_id"] = str(d3["user_id"])
#             data["fav"] = str(d3["fav"])
#             data["retweet"] = str(d3["retweet"])
#             data["action"] = str(d3["action"])
#             datas.append(data)
#     close_db()
#     return render_template(
#     'anary.html',
#     posts=datas
#     )
#
# @bp.route('/tweetlog', methods = ["GET" , "POST"])
# def tweetlog():
#    if request.method == 'POST':
#        user_id = request.form['user_id'] # formのname = "user_id"を取得
#        return render_template('anary.html', user_id = user_id)
#    else:
#        return render_template('anary.html')
