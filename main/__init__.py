from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
db_username = os.environ["DB_USER"]
db_password = os.environ["DB_PASS"]
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{db_username}:{db_password}@localhost/getic_analytics_new"
app.config["SECRET_KEY"] = os.urandom(32)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = None
app.config["MAIL_SERVER"] = "smtp.zoho.eu"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ["EMAIL_USER"]
app.config["MAIL_PASSWORD"] = os.environ["EMAIL_PASS"]
mail = Mail(app)
scheduler = BackgroundScheduler(daemon=True)

from main import views
