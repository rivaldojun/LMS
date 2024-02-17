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
from routes import db
from controllers.scheduler import *
from routes import app
from models.models import *
from dotenv import load_dotenv

# Charger les variables d'environnement du fichier .env
load_dotenv()

def send_email(sender_email, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    html_content = MIMEText(body, 'html')
    msg.attach(html_content)
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



@app.route('/souscription_conf/<int:id>', methods=['POST','GET'])
def souscription_conf(id):
    try:
        if request.method == 'POST':
            userName = request.form['userName']
            userEmail = request.form['userEmail']
            subscribeToNotifications = True if request.form.get('notif') == 'on' else False
            user=Souscripconf.query.filter_by(email=userEmail,idconf=id).first()
            conference=Conference.query.filter_by(id=id).first()
            if user:
                return redirect(url_for('deja_souscrit',id=id))
            souscription = Souscripconf(name=userName, email=userEmail, idconf=id, sub=subscribeToNotifications)
            db.session.add(souscription)
            db.session.commit()
            sender_email='info@lms-invention.com'
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
                <p>Vous êtes abonné à la conférence '{conference.titre}' qui aura lieu le {conference.date}.</p>
                <p>Rejoignez la conférence en cliquant sur ce lien: {conference.lien}</p>

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
                <p>Vous êtes abonné à la conférence '{conference.titre}' qui aura lieu le {conference.date}.</p>
                <p>Rejoignez la conférence en suivant ce lien: {conference.lieu}</p>

                <div class="thank-you">
                    <p>Merci encore et à bientôt chez <span style="color: blue;" >LMS-INVENTION</span> !</p>
                </div>
                <img src="/static/assets/images/lms-logo-removebg-preview.png" style="height: 50px;width: 50px;display:flex;">
            </div>
        </body>
        </html>
        '''
            sender_email='info@lms-invention.com'
            send_email(sender_email, userEmail,'LMS-Invention/Event', body)

            return render_template('confirmation_postul.html', message='Nous vous enverrons le lien de la conférence très prochainement', title='Vous êtes désormais parmi les participants de cette conférence',image='../static/assets/newsletter.jfif')
    except Exception as e:
        print(e)
        return render_template('confirmation_postul.html', message='Erreur du serveur', title='Veuillez réessayer dans un moment', image='../static/assets/wrong.jfif')

@app.route('/deja_souscrit/<id>', methods=['GET'])
def deja_souscrit(id):
    return render_template('deja_souscrit.html',id=id)


@app.route('/souscription_form/<int:id>', methods=['POST'])
def souscription_form(id):
    try: 
        userName = request.form['userName']
        userEmail = request.form['userEmail']
        subscribeToNotifications = True if request.form.get('notif') == 'on' else False
        user=SouscriptionFormation.query.filter_by(email=userEmail).first()
        session['userName']=userName
        if user:
            return redirect(f'/formation/{id}')
        else:
            souscription = SouscriptionFormation(name=userName, email=userEmail, sub=subscribeToNotifications)
            db.session.add(souscription)
            db.session.commit()
            return redirect(f'/formation/{id}')
    except Exception as e:
        return render_template('confirmation_postul.html', message='Erreur lors de la soumission du formulaire', title='Veuillez réessayer dans un moment', image='../static/assets/wrong.jfif')


@app.route('/newsletter', methods=['POST'])
def newsletter():
    try:
        email = request.form['email']
        name = request.form['name']
        # Vérifie si l'e-mail existe déjà dans la base de données
        existing_subscriber = Newsletter.query.filter_by(email=email).first()

        # Si l'abonné existe déjà, renvoyer une réponse appropriée
        if existing_subscriber:
            return render_template('newsletter_msg.html', message=f'Cet adresse mail {email} est déjà abonné à notre newsletter', title='OOPS...', image='../static/assets/wrong.jfif')

        # Si l'abonné n'existe pas, ajouter un nouvel enregistrement
        new_subscriber = Newsletter(email=email,name=name)
        db.session.add(new_subscriber)
        db.session.commit()

        # Réponse de succès
        return render_template('newsletter_msg.html', message='Vous recevrez prochainement le prochain numéro de notre newsletter.', title='Nous vous remercions', image='../static/assets/newsletter.jfif')
    except Exception as e:
        print(e)
        return render_template('newsletter_msg.html', message='Erreur lors de l\'abonnement à la newsletter', title='Veuillez réessayer dans un moment', image='../static/assets/wrong.jfif')




@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/actualites', methods=['GET'])
def actualites():
    blogs = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('actualites.html', blogs=blogs)


@app.route('/opportunite', methods=['GET'])
def carriere():
    return render_template('carriere.html')

@app.route('/evenement', methods=['GET'])
def evenement():
    return render_template('evenement.html')

@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')

@app.route('/log', methods=['GET'])
def log():
    if 'isLoggedIn' in session and session['isLoggedIn']:
       return redirect(url_for('admin_page'))
    else:
       return render_template('log.html', errorMessage='')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('isLoggedIn', None)
    return redirect(url_for('homepage'))

@app.route('/details_blog/<int:id>')
def details_blog(id):
    blog = Blog.query.get(id)
    blogs=Blog.query.filter_by().all()
    if blog:
        return render_template('details_blog.html', blog=blog,blogs=blogs)
    else:
        return 'Article de blog non trouvé'
    

# Route pour afficher les détails d'une conférence
@app.route('/details_confs/<int:id>')
def details_confs(id):
    conf = Conference.query.get(id)
    if conf:
        return render_template('details_confs.html', conf=conf)
    else:
        return 'Conférence non trouvée'


@app.route('/details_projet/<int:id>')
def details_projet(id):
    proj = Projet.query.get(id)
    if proj:
        return render_template('details_projet.html', proj=proj)
    else:
        return 'Projet non trouvé'

# Route pour afficher toutes les conférences
@app.route('/conferences')
def conferences():
    confs = Conference.query.order_by(Conference.id.desc()).all()
    return render_template('conferences.html', confs=confs)

# Routes pour les pages statiques
@app.route('/mentions_legales')
def mentions_legales():
    return render_template('mentions_legales.html')

@app.route('/politique_confidentialite')
def politique_confidentialite():
    return render_template('politique_confidentialite.html')

@app.route('/term')
def term():
    return render_template('term.html')

# Routes pour les pages de confirmation
@app.route('/confirmationblog')
def confirmationblog():
    return render_template('confirmation_blog.html')

@app.route('/confirmationevent')
def confirmationevent():
    return render_template('confirmation_event.html')

@app.route('/confirmationformation')
def confirmationformation():
    return render_template('confirmation_formation.html')

@app.route('/confirmationoffre')
def confirmationoffre():
    return render_template('confirmation_offre.html')

@app.route('/confirmationprojet')
def confirmationprojet():
    return render_template('confirmation_projet.html')

# Route pour la page des partenaires
@app.route('/partenaires')
def partenaires():
    return render_template('partenaire.html')

# Route pour afficher tous les projets
@app.route('/projet')
def projet():
    projets = Projet.query.order_by(Projet.id.desc()).all()
    return render_template('projet.html', projets=projets)

# Route pour la page "Qui sommes-nous ?"
@app.route('/quisommesnous')
def quisommesnous():
    return render_template('quisommesnous.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/contacte')
def contacte():
    return render_template('contacter.html')

@app.route('/formations')
def formations():
    formations = ThemeFormation.query.all()
    print(formations)
    return render_template('formations.html', formations=formations)

@app.route('/formation/<int:id>')
def formation(id):
    formations = ContentFormation.query.filter_by(theme_id=id).all()
    formation = ThemeFormation.query.filter_by(id=id).first()
    return render_template('formation.html', formations=formations,form=formation)

@app.route('/comment/<int:idform>')
def comment(idform):
    commentaires = CommentaireFormation.query.filter_by(formation_id=idform).all()
    return render_template('commentaire.html', commentaires=commentaires,idform=idform)


@app.route('/comment_blog/<int:idblog>')
def comment_blog(idblog):
    commentaires = CommentaireBlog.query.filter_by(blog_id=idblog).all()
    return render_template('commentaire_blog.html', commentaires=commentaires,idblog=idblog)


@app.route('/emploi/<int:id>')
def emploi(id):
    offre = Offre.query.get_or_404(id)
    return render_template('emploi.html', offre=offre)

@app.route('/emplois')
def emplois():
    offres = Offre.query.filter_by(type='emploi').all()
    return render_template('emplois.html', offres=offres,type="d'emplois")

@app.route('/stage')
def stage():
    offres = Offre.query.filter_by(type='stage').all()
    return render_template('emplois.html', offres=offres,type="de stage")

@app.route('/postul/<int:id>', methods=['POST'])
def postul(id):
    if request.method == 'POST':
        titre = request.form['titre']
        name = request.form['Name']
        email = request.form['Email']
        message = request.form['message']
        cv = request.files['fichiers']
        
        # Enregistrement du CV
        if cv:
            Path = os.path.join('static','assets', 'images_1', cv.filename)
            cv.save(Path)
        postul = Postul(titre=titre, name=name, email=email, message=message, cv=Path,post_id=id)
        db.session.add(postul)
        db.session.commit()

    return redirect(url_for('postulation_offre',id=id))

@app.route('/postulation_offre/<int:id>', methods=['GET'])
def postulation_offre(id):
    offre = Offre.query.filter_by(id-id).first()
    return render_template('confirmation_postul.html', message="Félicitations ! Votre candidature pour l'offre d'emploi {offre.fonc} a été soumise avec succès. Nous vous remercions pour l'intérêt que vous portez à notre entreprise.Nous reviendrons vers vous dès que possible.", title='Merci pour votre candidature !',image='../static/assets/newsletter.jfif')


@app.route('/formationview/<int:idf>/<int:id>', methods=['GET'])
def voir_formation(idf, id):
    try:
        form = ContentFormation.query.filter_by(id=id, theme_id=idf).first()
        if form:
            commentaires = CommentaireFormation.query.filter_by(formation_id=id).all()
            formations = form.path.split(',')
            print(formations)
            return render_template('formationview.html', form=form, formations=formations, idf=idf, commentaires=commentaires)
        else:
            return render_template('pas_element.html')
    except Exception as error:
        print('Erreur lors de la récupération de la formation :', error)
        return jsonify(message='Une erreur s\'est produite lors de la récupération de la formation'), 500