from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import join_room, leave_room, send, SocketIO
from os import path, getenv
from flask_login import LoginManager
from dotenv import load_dotenv
from .crypto import crypto_manager

db = SQLAlchemy()
socketio = SocketIO()
DB_NAME = "database.db"

def create_app():
  app = Flask(__name__)
  load_dotenv()
  app.config['SECRET_KEY'] = getenv('SECRET_KEY', 'fallback_key')
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  db.init_app(app)
  socketio.init_app(app, cors_allowed_origins='*')
  crypto_manager.init_app(app)

  from .utils import generate_room_code

  from .views import views
  from .auth import auth
  from .rooms import rooms

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  app.register_blueprint(rooms, url_prefix='/')

  from .models import User, Note

  from .sockets import init_socket_handlers
  init_socket_handlers(socketio)

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