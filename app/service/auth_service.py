import tweepy,time
from app.userdb import get_db,close_db
from app.function import like_tweepy,get_sorted_df,get_grouped_df,get_profile,retweet_tweepy,follow_tweepy,like_tweepy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
# from app.models.user import User

# 新規登録を行うためのメソッドです。引数にはviewsで取得するformデータが送られてきます。

# def signup(data: {}) -> User:  # -> User：これはreturnする値の型を指定しています。Userはオブジェクトとして出力します。
#     try:
#         name = data.get('name')
#         password = data.get('password')
#         # ユーザーがすでに登録されているかどうかを確認します
#         user = User.query.filter_by(name=name).first()
#         if user:
#             # 同じメールアドレスでユーザーが登録されているのであればユーザーをリターンします
#             return user
#         # ユーザーがいなければ作成します
#         new_user = User.from_args(name, password)
#         # データベースに追加するところ
#         db.session.add(new_user)
#         db.session.commit()
#         return user
#     except SQLAlchemyError:
#         raise SQLAlchemyError
 
 
# def login(data: {}) -> User:
#     try:
#         name = data.get('name')
#         password = data.get('password')
#         remember = True if data.get('remember') else False
#         user = User.query.filter_by(email=email).first()
#         # ユーザーとパスワードの確認
#         if not user and not user.check_password(user.password, password):
#             raise SQLAlchemyError
 
#         # ログイン。rememberにチェックを入れていればログインが維持される
#         login_user(user, remember=remember)
#         return user
#     except SQLAlchemyError:
#         raise SQLAlchemyError