from flask import Flask, render_template,request,redirect,session,jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
# Charger les variables d'environnement du fichier .env
load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
csrf = CSRFProtect(app)

app.secret_key = '123'
db = SQLAlchemy(app)

migrate=Migrate(app,db)

from Main.routes.admin import *
from Main.routes.user import *