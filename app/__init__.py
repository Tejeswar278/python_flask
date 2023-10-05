from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.config.from_object('config.config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from app import routes, models

# Create database tables on application startup
with app.app_context():
    db.create_all()

# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'JFJFJFJFJFJFJ'

#     return app