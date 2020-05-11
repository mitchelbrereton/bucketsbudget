from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ('Please log in to access this page.')

def create_app(test_config=None):
    #Create and configure an instance of the application
    app = Flask(__name__)
    #setup the config.py to the app
    app.config.from_object(Config)
    #register the database
    db.init_app(app)
    migrate.init_app(app, db)
    #login
    login.init_app(app)
    

    #apply the blueprints to the app
    from . import routes
    from . import auth
    from . import models
    from . import transaction
    #register blueprints
    app.register_blueprint(routes.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(transaction.bp)
    #set index page
    #app.add_url_rule("/", endpoint="index")

    return app

