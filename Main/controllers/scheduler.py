from flask import Flask, render_template,request,redirect,session,jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from Main.controllers.scheduler import *
from Main import *
from Main.models.models import *
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
    image = MIMEImage(open('Main/static/assets/images/lms-logo-removebg-preview.png', 'rb').read())
    image.add_header('Content-ID', '<image1>')
    msg.attach(image)
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
            subscriptions = Souscripconf.query.filter_by(idconf=conference.id, sub=True).first()
            subject = 'Reminder for %s' % conference.titre
            if conference.type == 'online' or conference.type == 'hybrid':
                
                body = '''
<!DOCTYPE html>
        <html>
        <head>
            <style>
        body {
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        
        .container {
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background-color: #ffffff; /* Lernender blue */
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            color: white;
        }
        
        h1 {
            color: #3498db; /* Lernender blue */
            font-size: 36px;
            margin-bottom: 10px;
        }
        
        p {
            color: rgb(0, 0, 0);
            font-size: 15px;
            line-height: 1.6;
            text-align: start;
        }
        
        .thank-you { 
            margin-top: 30px;
            font-style: italic;
            font-size: 20px;
        }
        .text{
            font-size: 10px;
        }

            </style>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        </head>
        <body>
            <div class="container">
                <h1><span >LMS-INVENTION</span></h1>
                <br>
                <p style="font-weight: bold;">Bonjour {subscriptions}</p>
                <p>Vous êtes abonné à la conférence '{conference.titre}' qui aura lieu dans 24 heures.</p>
                <br>
                <p style="text-align: center;font-weight: bold;">Rejoignez la conférence en suivant ce lien:<br>
                <a class="btn btn-primary" href='{conference.lien}'>Lien du meet</a></p>

                <div class="thank-you">
                    <p>Merci encore et à bientôt chez <br><span style="color: blue;" >LMS-INVENTION</span> !</p>
                    <div class="embed-responsive embed-responsive-16by9">
                        <img class="card-img-top embed-responsive-item" src="cid:image1" alt="LOGO" >
                    </div>
                </div>
                <hr style="border: 2px solid #3498db;">
                <p style="font-size: 10px;">Adresse: Meknes, Maroc, CP 50000</p>
                <p style="font-size: 10px;">Téléphone: <a href="tel://1234567920">+212 644304209</a></p>
                <p style="font-size: 10px;">Email: <a href="mailto:info@lms-invention.com">info@lms-invention.com</a></p>
                <p style="font-size: 10px;">Site web: <a href="{{url_for('homepage')}}">lms-invention</a></p>
                <br>
                <br>
                <div class="container" style="color: rgb(0, 173, 0);">
                    <p style="font-size: 10px;color: rgb(0, 173, 0);">
                        <span><i class="fas fa-plus"></i></span>
                        Pensez à l'environnement ! Nettoyez votre messagerie régulièrement en supprimant les mails traités et les pièces jointes enregistrées !
                    </p>
                </div>
            </div>
        </body>
        </html>'''
            else:
                body = '''
<!DOCTYPE html>
        <html>
        <head>
            <style>
        body {
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        
        .container {
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background-color: #ffffff; /* Lernender blue */
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            color: white;
        }
        
        h1 {
            color: #3498db; /* Lernender blue */
            font-size: 36px;
            margin-bottom: 10px;
        }
        
        p {
            color: rgb(0, 0, 0);
            font-size: 15px;
            line-height: 1.6;
            text-align: start;
        }
        
        .thank-you { 
            margin-top: 30px;
            font-style: italic;
            font-size: 20px;
        }
        .text{
            font-size: 10px;
        }

            </style>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        </head>
        <body>
            <div class="container">
                <h1><span >LMS-INVENTION</span></h1>
                <br>
                <p style="font-weight: bold;">Bonjour {subscriptions}</p>
                <p>Vous êtes abonné à la conférence '{conference.titre}' qui aura lieu dans 24 heures.</p>
                <p>Rejoignez la conférence en vous presentant au lieu de rendez-vous :<a href='#'>{conference.lieu}</a></p>
                <br>
                <p style="text-align: center;font-weight: bold;">Rejoignez la conférence en suivant ce lien:<br>
                <a class="btn btn-primary" href='{conference.lien}'>Lien du meet</a></p>

                <div class="thank-you">
                    <p>Merci encore et à bientôt chez <br><span style="color: blue;" >LMS-INVENTION</span> !</p>
                    <div class="embed-responsive embed-responsive-16by9">
                        <img class="card-img-top embed-responsive-item" src="cid:image1" alt="LOGO" >
                    </div>
                </div>
                <hr style="border: 2px solid #3498db;">
                <p style="font-size: 10px;">Adresse: Meknes, Maroc, CP 50000</p>
                <p style="font-size: 10px;">Téléphone: <a href="tel://1234567920">+212 644304209</a></p>
                <p style="font-size: 10px;">Email: <a href="mailto:info@lms-invention.com">info@lms-invention.com</a></p>
                <p style="font-size: 10px;">Site web: <a href="{{url_for('homepage')}}">lms-invention</a></p>
                <br>
                <br>
                <div class="container" style="color: rgb(0, 173, 0);">
                    <p style="font-size: 10px;color: rgb(0, 173, 0);">
                        <span><i class="fas fa-plus"></i></span>
                        Pensez à l'environnement ! Nettoyez votre messagerie régulièrement en supprimant les mails traités et les pièces jointes enregistrées !
                    </p>
                </div>
            </div>
        </body>
        </html>'''
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