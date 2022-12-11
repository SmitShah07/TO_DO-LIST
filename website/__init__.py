from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from decouple import config

    
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dwljkefnsdl_jkf@65dkjl"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/todo_notes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')
    db.init_app(app)
        
    from .views import views
    from .auth import auth
        
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
        
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
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
