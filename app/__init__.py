from flask import Flask, render_template
# from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import os

# # def create_app():
# app=Flask(__name__,instance_relative_config=True)
#     # login_manager = LoginManager()
#     # login_manager.login_view = 'auth.login'
#     # login_manager.init_app(app)
# app.config.from_mapping(
#         secret_key='temp',
#         DATABASE=os.path.join(app.instance_path,'user_db')
# )
#     # # instanceフォルダがあるか確認
#     # try:
#     #     os.makedirs(app.instance_path)
#     # except OSError:
#     #     pass

#     # tweetに関するルートをflaskアプリであるappに追加
# from app.views.users import users
# app.register_blueprint(users, url_prefix='/users')

# import app.userdb
# # userdb.init_app(app)

#     # from app.models.user import User

#     # @login_manager.user_loader
#     # def load_user(user_id):
#     #     return User.query.get(int(user_id))
        
#     # authに関するルーティングを追加
# from app.views.auth import auth
#     # authに関するルートをflaskアプリであるappに追加
# # app.register_blueprint(auth, url_prefix='/auth')
#     # return app

# # app=create_app()

# # if __name__ == '__main__':
# #     app.run(host="localhost")

# # @app.route('/')
# # # @login_required
# # def index():
# #     return render_template('tweet/index.html')


def create_app(test_config=None):
    # アプリケーションの生成と設定を行う
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'user_db'),
    )

    if test_config is None:
        # testではない場合に、インスタンスの設定値が存在すれば読み込む
        app.config.from_pyfile('config.py', silent=True)
    else:
        # テストの設定を読み込む
        app.config.from_mapping(test_config)

    # instanceフォルダが存在することを保証する
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    return app
app=create_app()
from app.views.users import users
app.register_blueprint(users)

    # import app.userdb
    # userdb.init_app(app)

    # authに関するルーティングを追加
from app.views.auth import auth
    # authに関するルートをflaskアプリであるappに追加
app.register_blueprint(auth)