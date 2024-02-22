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
from flask_caching import Cache


# Charger les variables d'environnement du fichier .env
load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
csrf = CSRFProtect(app)

app.secret_key = '123'
db = SQLAlchemy(app)

migrate=Migrate(app,db)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Définition de la route pour servir les fichiers CSS mis en cache
@app.route('/static/css/<path:filename>')
@cache.cached(timeout=360000)  # Mettre en cache pendant 1 heure (3600 secondes)
def cached_css(filename):
    return app.send_static_file('css/' + filename)

@app.route('/static/assets/images/<path:filename>')
@cache.cached(timeout=360000)  # Mettre en cache pendant 1 heure (3600 secondes)
def cached_images(filename):
    return app.send_static_file('assets/images/' + filename)


from Main.routes.admin import *
from Main.routes.user import *