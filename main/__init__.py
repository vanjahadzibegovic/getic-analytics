from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
import os

# from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:smitSmece@localhost/getic_analytics_new"
app.config["SECRET_KEY"] = os.urandom(32)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
scheduler = BackgroundScheduler(daemon=True)

from main import views
