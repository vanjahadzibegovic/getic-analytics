from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

# from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:smitSmece@localhost/getic_analytics"
db = SQLAlchemy(app)
scheduler = BackgroundScheduler(daemon=True)
# bcrypt = Bcrypt(app)

from main import views
