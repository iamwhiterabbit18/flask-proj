from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = '19e9555b72fa1d80d08f84d0edc8f4d948ad3880d4cb2261e832ed926e48575339c539746ef5f7bfbf8c98bdb50db4fefd66251259a5ebf4c14e8ad49d3e570b'
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  db.init_app(app)

  

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  from .models import User, Note

  create_database(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)
  
  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))

  return app

def create_database(app):
  with app.app_context():
    if not path.exists('website/' + DB_NAME):
      db.create_all()
      print('Created Database!')