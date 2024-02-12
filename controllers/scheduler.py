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
from controllers.scheduler import *
from routes import app
from models.models import *
from dotenv import load_dotenv
import os

# Charger les variables d'environnement du fichier .env
load_dotenv()



def send_email(sender_email, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    html_content = MIMEText(body, 'html')
    msg.attach(html_content)
    # Paramètres de connexion au serveur SMTP
    # Paramètres de connexion SMTP
    # smtp_host = 'mail.lms-invention.com'  # Remplacez par le serveur SMTP de votre e-mail
    # smtp_port = 465  # Port SMTP approprié
    # smtp_user = 'info@lms-invention.com'  # Votre adresse e-mail
    # smtp_password = 'LMSINV@info23'  # Mot de passe de votre adresse e-mail

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    # Configuration et envoi de l'e-mail
    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        return True
    except Exception as e:
        return False

def schedule_email_reminders():
    with app.app_context():
        scheduler = BackgroundScheduler()
        conferences = Conference.query.all()
        for conference in conferences:
            subject = 'Reminder for %s' % conference.titre
            if conference.type == 'online' or conference.type == 'hybrid':
                body = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                /* Stylize the email with CSS */
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    padding: 20px;
                    background-color: #ffffff; /* Lernender blue */
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    color: white;
                    text-align: center;
                }}
                
                h1 {{
                    color: #3498db; /* Lernender blue */
                    font-size: 36px;
                    margin-bottom: 10px;
                }}
                
                p {{
                    color: rgb(0, 0, 0);
                    font-size: 18px;
                    line-height: 1.6;
                    text-align: center;
                }}
                
                .code {{
                    font-size: 42px;
                    font-weight: bold;
                }}
                
                
                .thank-you {{ 
                    margin-top: 30px;
                    font-style: italic;
                    font-size: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1><span >LMS-INVENTION</span></h1>
                <p>Vous êtes abonné à la conférence '{conference.titre}' qui commence dans 24 heure.</p>
                <p>Rejoignez la conférence en suivant ce lien: {conference.lien}</p>

                <div class="thank-you">
                    <p>Merci encore et à bientôt chez <span style="color: blue;" >LMS-INVENTION</span> !</p>
                </div>
                <img src="/static/assets/images/lms-logo-removebg-preview.png" style="height: 50px;width: 50px;display:flex;">
            </div>
        </body>
        </html>
        '''
            else:
                body = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                /* Stylize the email with CSS */
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    padding: 20px;
                    background-color: #ffffff; /* Lernender blue */
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    color: white;
                    text-align: center;
                }}
                
                h1 {{
                    color: #3498db; /* Lernender blue */
                    font-size: 36px;
                    margin-bottom: 10px;
                }}
                
                p {{
                    color: rgb(0, 0, 0);
                    font-size: 18px;
                    line-height: 1.6;
                    text-align: center;
                }}
                
                .code {{
                    font-size: 42px;
                    font-weight: bold;
                }}
                
                
                .thank-you {{ 
                    margin-top: 30px;
                    font-style: italic;
                    font-size: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1><span >LMS-INVENTION</span></h1>
                <p>Vous êtes abonné à la conférence '{conference.titre}' qui commence dans 24 heures.</p>
                <p>Rejoignez la conférence en suivant ce lien: {conference.lieu}</p>

                <div class="thank-you">
                    <p>Merci encore et à bientôt chez <span style="color: blue;" >LMS-INVENTION</span> !</p>
                </div>
                <img src="/static/assets/images/lms-logo-removebg-preview.png" style="height: 50px;width: 50px;display:flex;">
            </div>
        </body>
        </html>
        '''

            sender_email =  'info@lms-invention.com'
            # Récupérer les abonnements pour cette conférence
            subscriptions = Souscripconf.query.filter_by(idconf=conference.id, sub=True).all()
            for subscription in subscriptions:
                # Vérifier si un job existe déjà pour cet abonnement
                job_id = f'{subscription.idconf}_{subscription.id}'
                existing_jobs = scheduler.get_job(job_id, jobstore='default')
                if not existing_jobs:
                    # Planifier l'envoi de l'e-mail une heure avant le début de la conférence
                    reminder_time = conference.date - timedelta(hours=1)
                    scheduler.add_job(send_email, 'date', run_date=reminder_time,
                                    args=[sender_email,subscription.email,subject,body], id=f'{subscription.idconf}_{subscription.id}')
        scheduler.start()