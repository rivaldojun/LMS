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


@app.route('/messages')
def messages():
    # Code pour récupérer la liste des messages depuis la base de données
    # Remplacer cette ligne par votre propre code pour récupérer les messages
    messages = Message.query.all()
    return render_template('messages.html', messages=messages)

@app.route('/view_message/<int:message_id>')
def view_message(message_id):
    # Code pour récupérer les détails du message avec l'ID donné depuis la base de données
    # Remplacer cette ligne par votre propre code pour récupérer les détails du message
    message = Message.query.get_or_404(message_id)
    return render_template('view_message.html', message=message)

@app.route('/delete_message/<int:message_id>', methods=['GET', 'POST'])
def delete_message(message_id):
    # Code pour supprimer le message avec l'ID donné de la base de données
    # Remplacer cette ligne par votre propre code pour supprimer le message
    message = Message.query.get_or_404(message_id)
    if request.method == 'POST':
        db.session.delete(message)
        db.session.commit()
        return redirect(url_for('messages'))  # Rediriger vers la liste des messages
    return render_template('delete_message.html', message_id=message_id)


@app.route('/reply_message/<int:message_id>', methods=['GET', 'POST'])
def reply_message(message_id):
    # Code pour récupérer le message avec l'ID donné de la base de données
    # Remplacer cette ligne par votre propre code pour récupérer le message
    message = Message.query.get_or_404(message_id)
    if request.method == 'POST':
        # Récupérer la réponse du formulaire
        reply = request.form['reply']
        subject = 'Reponse'
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
        <p>{reply}</p>
        <p class="code"></p>
        
        <div class="thank-you">
            <p>Merci encore et à bientôt chez <span style="color: blue;" >LMS-INVENTION</span> !</p>
        </div>
        <img src="/static/assets/images/lms-logo-removebg-preview.png" style="height: 50px;width: 50px;display:flex;">
    </div>
</body>
</html>
'''
        sender_email =  'info@lms-invention.com'
        send_email(sender_email, message.email, subject, body)
        message.statut="Repondu"
        db.session.commit()
        return redirect(url_for('messages'))
    return render_template('reply_message.html', message_id=message_id)


@app.route('/auto_reply_message/<int:message_id>', methods=['GET', 'POST'])
def auto_reply_message(message_id):
    # Code pour récupérer le message avec l'ID donné de la base de données
    # Remplacer cette ligne par votre propre code pour récupérer le message
        message = Message.query.get_or_404(message_id)
        image_url = url_for('static', filename='assets/images/lms-logo-removebg-preview.png')
        # Récupérer la réponse du formulaire
        subject = 'Nous traitons votre préoccupation'
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
        <div style="font-family: Arial, sans-serif; font-size: 16px; line-height: 1.6;">
            <p>Bonjour {message.name}</p><br>
            <p>Nous vous remercions de votre prise de contact et accusons réception de votre demande .</p>
            <p>Notre délai de réponse actuel est en moyenne de 2 à 5 heures. Nous faisons le nécessaire pour vous apporter une solution le plus rapidement possible.</p>
            <br>
            <p>Petite astuce, vérifiez vos courriers indésirables et vos spams, nos réponses peuvent s’y glisser.</p><br>
            <p>Pour être plus efficace, nous vous demandons de ne pas multiplier vos demandes : tickets multipliés = temps de traitement allongé. En effet, chaque demande équivaut à un ticket ouvert pour notre service clientèle par ordre d'ancienneté. Si celles-ci sont multipliées, cela aura pour conséquence d'allonger le temps de réponse.</p><br>
            <p>En attendant, permettez-nous de partager avec vous notre <a href="{{ 'faq') }}" style="color: #0066cc; text-decoration: underline;">FAQ</a>. Vous y trouverez peut-être des réponses à votre question.</p>
            <br>
            <p>Nous vous remercions de votre confiance.</p>
            <p>L'équipe LMS-INVENTION</p>
        </div>
        
        <div class="thank-you">
            <p>Merci encore et à bientôt chez <span style="color: blue;" >LMS-INVENTION</span> !</p>
            <img src="{image_url}" style="height: 50px;width: 50px;display:flex;">

        </div>
        
    </div>
</body>
</html>
'''
        sender_email =  'info@lms-invention.com'
        print(sender_email)
        send_email(sender_email, message.email, subject, body)
        print(message.email)
        print("envoyer")
        return render_template('confirmation_postul.html', message='Nous vous reviendrons dans les délais dès que possible', title='Votre message a été soumis avec succès', image='../static/assets/newsletter.jfif')


@app.route('/submit-offer', methods=['POST'])
def submit_offer():
    titre = request.form['titre']
    name = request.form['Name']
    email = request.form['Email']
    message = request.form['message']
    uploaded_file = request.files['fichiers']

    # smtp_host = 'mail.lms-invention.com'  # Remplacez par le serveur SMTP de votre e-mail
    # smtp_port = 465  # Port SMTP approprié
    # smtp_user = 'info@lms-invention.com'  # Votre adresse e-mail
    # smtp_password = 'LMSINV@info23'  # Mot de passe de votre adresse e-
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = 'info@lms-invention.com'
    msg['Subject'] = 'Nouvelle soumission de formulaire'

    body = f"""
    Titre: Pour le poste de {titre}
    Nom: De la part de {name}
    Email: {email}
    Message: {message}
    """
    msg.attach(MIMEText(body, 'plain'))

    if uploaded_file:
        attachment = MIMEApplication(uploaded_file.read(), _subtype="pdf")
        attachment.add_header('Content-Disposition', f'attachment; filename={uploaded_file.filename}')
        msg.attach(attachment)

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, 'info@lms-invention.com', msg.as_string())
        return render_template('confirmation_postul.html', message='Nous vous reviendrons après analyse de votre dossier', title='Votre dossier a été soumis avec succès', image='../static/assets/newsletter.jfif')
    except Exception as e:
        print(e)
        return render_template('confirmation_postul.html', message='Erreur du serveur, veuillez réessayer dans un moment', title='Veuillez réessayer dans un moment', image='../static/assets/wrong.jfif')



@app.route('/adminpage', methods=['GET'])
def admin_page():
    if 'isLoggedIn' in session and session['isLoggedIn']:
        return render_template('pageadmin.html')
    else:
        return 'Impossible'

@app.route('/addblog', methods=['GET'])
def add_blog():
    if 'isLoggedIn' in session and session['isLoggedIn']:
        return render_template('addblog.html')
    else:
        return 'Impossible'

@app.route('/addformation', methods=['GET'])
def add_formation():
    if 'isLoggedIn' in session and session['isLoggedIn']:
        return render_template('addformation.html')
    else:
        return 'Impossible'

@app.route('/addevents', methods=['GET'])
def add_events():
    if 'isLoggedIn' in session and session['isLoggedIn']:
        return render_template('addevents.html')
    else:
        return 'Impossible'

@app.route('/addoffer', methods=['GET'])
def add_offer():
    if 'isLoggedIn' in session and session['isLoggedIn']:
        return render_template('addoffer.html')
    else:
        return 'Impossible'

@app.route('/addprojet', methods=['GET'])
def add_projet():
    if 'isLoggedIn' in session and session['isLoggedIn']:
        return render_template('addprojet.html')
    else:
        return 'Impossible'

@app.route('/addblogadmin', methods=['GET'])
def add_blog_admin():
    if 'isLoggedIn' in session and session['isLoggedIn']:
        blogs = Blog.query.order_by(Blog.id.desc()).all()
        return render_template('actualitesadmin.html', blogs=blogs)
    else:
        return 'Impossible'

@app.route('/addformationsadmin', methods=['GET'])
def add_formations_admin():
    if 'isLoggedIn' in session and session['isLoggedIn']:
        formations = ThemeFormation.query.order_by(ThemeFormation.id.desc()).all()
        return render_template('formationsadmin.html', formations=formations)
    else:
        return 'Impossible'

@app.route('/addformationadmin/<int:id>', methods=['GET'])
def add_formation_admin(id):
    if 'isLoggedIn' in session and session['isLoggedIn']:
        formations = ContentFormation.query.filter_by(theme_id=id).all()
        formation = ThemeFormation.query.filter_by(id=id).first()
        return render_template('formationadmin.html', formations=formations, idform=id,formation=formation)
    else:
        return 'Impossible'

@app.route('/addeventsadmin', methods=['GET'])
def add_events_admin():
    if 'isLoggedIn' in session and session['isLoggedIn']:
        confs = Conference.query.order_by(Conference.id.desc()).all()
        return render_template('conferencesadmin.html', confs=confs)
    else:
        return 'Impossible'
    

# Routes
@app.route('/addofferadminemploi', methods=['GET'])
def add_offer_admin_emploi():
    if 'isLoggedIn' in session and session['isLoggedIn']:
        offers = Offre.query.filter_by(type='emploi').all()
        return render_template('emploisadmin.html', offers=offers)
    else:
        return 'Impossible'

@app.route('/addofferadminstage', methods=['GET'])
def add_offer_admin_stage():
    if 'isLoggedIn' in session and session['isLoggedIn']:
        offers = Offre.query.filter_by(type='stage').all()
        return render_template('emploisadmin.html', offers=offers)
    else:
        return 'Impossible'

@app.route('/addprojetadmin', methods=['GET'])
def add_projet_admin():
    if 'isLoggedIn' in session and session['isLoggedIn']:
        projects = Projet.query.order_by(Projet.id.desc()).all()
        return render_template('projetadmin.html', projects=projects)
    else:
        return 'Impossible'

@app.route('/regist', methods=['GET'])
def regist():
    return render_template('regist.html', errorMessage='')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        func = request.form['function']
        password = request.form['password']
        confpassword = request.form['confpassword']
        hashed_password = generate_password_hash(password)

        if password == confpassword:
            registration = Registration(name=name, email=email, func=func, password=hashed_password)
            db.session.add(registration)
            db.session.commit()
            return redirect('/log')
        else:
            return render_template('regist.html', errorMessage='Mot de passe non correspondant')
    else:
        # Gérer le cas où la méthode est GET (chargement initial de la page)
        return render_template('regist.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = Registration.query.filter_by(email=email).first()

    if email=='a@gmail.com' and password=='qwerty12':
        session['isLoggedIn'] = True
        return redirect('/adminpage')
    else:
        return render_template('log.html', errorMessage='Adresse e-mail ou mot de passe incorrect')


@app.route('/enregistrer-article', methods=['POST'])
def enregistrer_article():
    titre = request.form['titre']
    contenu = request.form['contenu']
    image = request.files['image']
    imagePath = os.path.join('static','assets', 'images_1', image.filename)
    image.save(imagePath)
    article = Blog(titre=titre, description=contenu, imagePath=imagePath)
    db.session.add(article)
    db.session.commit()
    return redirect('/confirmationblog')

# Route pour enregistrer un événement
@app.route('/enregistrer-event', methods=['POST'])
def enregistrer_event():
    titre = request.form['titre']
    description = request.form['contenu']
    type = request.form['conf-type']
    conferencier = request.form['conferencier']
    lieu = request.form['lieu']
    date = datetime.strptime(request.form['date'], '%Y-%m-%dT%H:%M')
    image = request.files['image']
    imagePath = os.path.join('static','assets', 'images_1', image.filename)
    image.save(imagePath)
    lien = request.form['lien']
    conference = Conference(titre=titre, description=description, lieu=lieu,type=type, date=date, imagePath=imagePath, lien=lien,conferencier=conferencier)
    db.session.add(conference)
    db.session.commit()
    return redirect('/confirmationevent')

# Route pour enregistrer une formation
@app.route('/enregistrer-formation', methods=['POST'])
def enregistrer_formation():
    titre = request.form['titre']
    contenu = request.form['contenu']
    formation = ThemeFormation(titre=titre, description=contenu)
    db.session.add(formation)
    db.session.commit()
    return redirect('/confirmationformation')

# Route pour enregistrer une offre
@app.route('/enregistrer-offer', methods=['POST','GET'])
def enregistrer_offer():
    if request.method == 'POST':
        annonce_type = request.form['annonce-type']
        contenu = request.form['contenu']
        fonc = request.form['fonc']
        image = request.files['image']
        imagePath = os.path.join('static','assets', 'images_1', image.filename)
        image.save(imagePath)
        offre = Offre(type=annonce_type, description=contenu, fonc=fonc, imagePath=imagePath)
        db.session.add(offre)
        db.session.commit()
    return redirect('/confirmationoffre')

# Route pour enregistrer un projet
@app.route('/enregistrer-projet', methods=['POST'])
def enregistrer_projet():
    titre = request.form['titre']
    description = request.form['contenu']
    image = request.files['image']
    imagePath = os.path.join('static','assets', 'images_1', image.filename)
    image.save(imagePath)
    projet = Projet(titre=titre, description=description, imagePath=imagePath)
    db.session.add(projet)
    db.session.commit()
    return redirect('/confirmationprojet')

@app.route('/details_confs_admin/<int:id>')
def details_confs_admin(id):
    conf = Conference.query.get(id)
    nb=Souscripconf.query.filter_by(idconf=conf.id, sub=True).count()
    if conf:
        return render_template('details_confs_admin.html', conf=conf,nb=nb)
    else:
        return 'Conférence non trouvée'
    

@app.route('/addformcontent/<int:id>')
def addformcontent(id):
    if 'isLoggedIn' in session and session['isLoggedIn']:
        return render_template('addformcontent.html', idform=id)
    else:
        return "Impossible"


@app.route('/enregistrer-commentaire/<int:idf>', methods=['POST'])
def enregistrer_commentaire(idf):
    contenu = request.form['commentaire']
    userName = request.form['username']
    dateCommentaire = datetime.now()
    nouveau_commentaire = CommentaireFormation(contenu=contenu, auteur=userName, formation_id=idf, date=dateCommentaire)
    db.session.add(nouveau_commentaire)
    db.session.commit()
    return redirect(url_for('comment',idform=idf))

@app.route('/enregistrer-commentaire-blog/<int:idf>', methods=['POST'])
def enregistrer_commentaire_blog(idf):
    contenu = request.form['commentaire']
    userName = request.form['username']
    dateCommentaire = datetime.now()
    nouveau_commentaire = CommentaireBlog(contenu=contenu, auteur=userName, blog_id=idf, date=dateCommentaire)
    db.session.add(nouveau_commentaire)
    db.session.commit()
    return redirect(url_for('comment_blog',idblog=idf))

@app.route('/voir_candidats/<int:postul_id>')
def voir_candidats(postul_id):
    # Code pour récupérer les informations du postulant avec l'ID donné
    postulant = Postul.query.get_or_404(postul_id)
    return render_template('details_candidats.html', postulant=postulant)

@app.route('/candidats/<int:id>')
def candidat(id):
    postuls = Postul.query.filter_by(post_id=id).all()
    return render_template('candidat.html', postuls=postuls)

@app.route('/ajouter-formation/<int:id>', methods=['POST'])
def ajouter_formation(id):
    path_abs=[]
    try:
        idform = int(id)
        titre = request.form['titre']
        description = request.form['description']
        fichiers = request.files.getlist('fichiers[]')
        for file in fichiers:
            imagePath=os.path.join('static','assets','images_1', file.filename)
            path_abs.append(imagePath)
            file.save(imagePath)
        # Construction des chemins des fichiers
        path = ','.join([file.filename for file in fichiers])
        # Enregistrement des données dans la base de données
        nouvelle_formation = ContentFormation(titre=titre, description=description, path=path, theme_id=idform)
        db.session.add(nouvelle_formation)
        db.session.commit()

        return redirect('/confirmationoffre')
    except Exception as error:
        print('Erreur lors de l\'ajout de la formation :', error)
        return jsonify(message='Une erreur s\'est produite lors de l\'ajout de la formation'), 500
    

@app.route('/supprimerblog/<int:id>', methods=['GET'])
def supprimer_blog(id):
    try:
        blog = Blog.query.get(id)
        if blog:
            db.session.delete(blog)
            db.session.commit()
            return render_template('confirmation_supp.html',message='supprimé avec succès.',title='Suppression',image='../static/assets/vecteur/delete.jpeg')
        else:
            return render_template('confirmation_supp.html',message='Element non trouvé .',title='Suppression',image='../static/assets/vecteur/delete.jpeg') 
    except Exception as error:
        print('Une erreur s\'est produite lors de la suppression du blog :', error)
        return 'Une erreur s\'est produite lors de la suppression du blog.', 500

@app.route('/supprimerconfs/<int:id>', methods=['GET'])
def supprimer_conference(id):
    try:
        conference = Conference.query.filter_by(id=id).first()
        if conference:
            db.session.delete(conference)
            db.session.commit()
            return render_template('confirmation_supp.html',message='supprimé avec succès.',title='Suppression',image='../static/assets/vecteur/delete.jpeg')
        else:
            return render_template('confirmation_supp.html',message='Element non trouvé .',title='Suppression',image='../static/assets/vecteur/delete.jpeg') 
    except Exception as error:
        print('Une erreur s\'est produite lors de la suppression de la conférence :', error)
        return 'Une erreur s\'est produite lors de la suppression de la conférence.', 500

@app.route('/supprimeremploi/<int:id>', methods=['GET'])
def supprimer_offre_emploi(id):
    try:
        offre_emploi = Offre.query.get(id)
        if offre_emploi:
            db.session.delete(offre_emploi)
            db.session.commit()
            return render_template('confirmation_supp.html',message='supprimé avec succès.',title='Suppression',image='../static/assets/vecteur/delete.jpeg')
        else:
            return render_template('confirmation_supp.html',message='Element non trouvé .',title='Suppression',image='../static/assets/vecteur/delete.jpeg') 
    except Exception as error:
        print('Une erreur s\'est produite lors de la suppression de l\'offre d\'emploi :', error)
        return "Une erreur s'est produite lors de la suppression de l'offre d'emploi.", 500


@app.route('/Supprimerformation/<int:idf>/<int:id>', methods=['GET'])
def supprimer_contenu_formation(idf, id):
    try:
        content_formation = ContentFormation.query.filter_by(id=id, theme_id=idf).first()
        if content_formation:
            db.session.delete(content_formation)
            db.session.commit()
            return render_template('confirmation_supp.html',message='Contenu de la formation supprimé avec succès.',title='Suppression',image='../static/assets/vecteur/delete.jpeg')  
        else:
            return  render_template('confirmation_supp.html',message='Contenu de la formation non trouvé.',title='Suppression',image='../static/assets/vecteur/delete.jpeg')  
    except Exception as error:
        print('Une erreur s\'est produite lors de la suppression du contenu de la formation :', error)
        return 'Une erreur s\'est produite lors de la suppression du contenu de la formation.', 500

@app.route('/supprimerformations/<int:id>', methods=['GET'])
def supprimer_formations(id):
    try:
        theme_formation = ThemeFormation.query.get(id)
        if theme_formation:
            db.session.delete(theme_formation)
            db.session.commit()
            return render_template('confirmation_supp.html',message='supprimé avec succès.',title='Suppression',image='../static/assets/vecteur/delete.jpeg')
        else:
            return render_template('confirmation_supp.html',message='Element non trouvé .',title='Suppression',image='../static/assets/vecteur/delete.jpeg') 
    except Exception as error:
        print('Une erreur s\'est produite lors de la suppression des formations :', error)
        return 'Une erreur s\'est produite lors de la suppression des formations.', 500


@app.route('/supprimerprojet/<int:id>', methods=['GET'])
def supprimer_projet(id):
    try:
        projet = Projet.query.get(id)
        if projet:
            db.session.delete(projet)
            db.session.commit()
            return render_template('confirmation_supp.html',message='supprimé avec succès.',title='Suppression',image='../static/assets/vecteur/delete.jpeg')
        else:
            return render_template('confirmation_supp.html',message='Element non trouvé.',title='Suppression',image='../static/assets/vecteur/delete.jpeg')
    except Exception as error:
        print('Une erreur s\'est produite lors de la suppression du projet :', error)
        return 'Une erreur s\'est produite lors de la suppression du projet.', 500


@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

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
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = 'info@lms-invention.com'  # Adresse e-mail du destinataire
        msg['Subject'] = subject
        msg.attach(MIMEText(f'Name: {name}\nEmail: {email}\nMessage: {message}', 'html'))

        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, 'info@lms-invention.com', msg.as_string())

        new_message = Message(name=name, email=email, subject=subject, message=message)
        # Ajouter l'instance à la session SQLAlchemy et committez les changements
        db.session.add(new_message)
        db.session.commit()
        print(new_message)
        return redirect(url_for('auto_reply_message',message_id=new_message.id))
    except Exception as e:
        print(e)
        return render_template('confirmation_postul.html', message='Erreur, veuillez réessayer dans un moment', title='Veuillez réessayer dans un moment', image='../static/assets/wrong.jfif')
