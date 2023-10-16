from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/pokemon'

    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')
    app.app_context().push()

    # TO CREATE TABLE:
    db.create_all()

    return app
