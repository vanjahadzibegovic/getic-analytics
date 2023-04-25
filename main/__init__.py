from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

# from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:smitSmece@localhost/getic_analytics_new"
app.config["SECRET_KEY"] = "da293ksa082kda92"
db = SQLAlchemy(app)
scheduler = BackgroundScheduler(daemon=True)
# bcrypt = Bcrypt(app)

from main import views
