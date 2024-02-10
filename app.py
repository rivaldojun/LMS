from flask import Flask, render_template,request,redirect,session,jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = '123'
db = SQLAlchemy(app)

#Model class

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    func = db.Column(db.String)
    password = db.Column(db.String)

class Souscripconf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    idconf = db.Column(db.Integer)
    sub = db.Column(db.Boolean)

class SouscriptionFormation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    sub = db.Column(db.Boolean)

class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String)
    description = db.Column(db.String)
    imagePath = db.Column(db.String)

class Projet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String)
    description = db.Column(db.String)
    imagePath = db.Column(db.String)

class Offre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    description = db.Column(db.String)
    imagePath = db.Column(db.String, default="../assets/images/lms-logo-removebg-preview.png")
    fonc = db.Column(db.String, default="")
    date = db.Column(db.DateTime, default=datetime.now)

class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String)
    description = db.Column(db.String)
    imagePath = db.Column(db.String)
    lien = db.Column(db.String)
    lieu = db.Column(db.String, default="")
    date = db.Column(db.DateTime, default=datetime.now)

class ThemeFormation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String)
    description = db.Column(db.String)
    # content_formations = db.relationship('ContentFormation', backref='theme')

class ContentFormation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String)
    description = db.Column(db.String)
    path = db.Column(db.String)
    theme_id = db.Column(db.Integer, db.ForeignKey('theme_formation.id'))  # Renommer la colonne de clé étrangère
    # theme = db.relationship('ThemeFormation', backref='content_formations')
    # commentaires = db.relationship('CommentaireFormation', backref='formation')

class CommentaireFormation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.String)
    auteur = db.Column(db.String)
    date = db.Column(db.DateTime)
    formation_id = db.Column(db.Integer, db.ForeignKey('content_formation.id'))


with app.app_context():
        db.create_all()
#end model

@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    # Paramètres de connexion SMTP
    smtp_host = 'mail.lms-invention.com'  # Remplacez par le serveur SMTP de votre e-mail
    smtp_port = 465  # Port SMTP approprié
    smtp_user = 'info@lms-invention.com'  # Votre adresse e-mail
    smtp_password = 'LMSINV@info23'  # Mot de passe de votre adresse e-mail

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

        return render_template('confirmation_postul.html', message='Nous vous reviendrons dans les délais dès que possible', title='Votre message a été soumis avec succès', image='../assets/newsletter.jfif')
    except Exception as e:
        print(e)
        return render_template('confirmation_postul.html', message='Erreur, veuillez réessayer dans un moment', title='Veuillez réessayer dans un moment', image='../assets/wrong.jfif')


@app.route('/submit-offer', methods=['POST'])
def submit_offer():
    titre = request.form['titre']
    name = request.form['Name']
    email = request.form['Email']
    message = request.form['message']
    uploaded_file = request.files['fichiers']

    smtp_host = 'mail.lms-invention.com'  # Remplacez par le serveur SMTP de votre e-mail
    smtp_port = 465  # Port SMTP approprié
    smtp_user = 'info@lms-invention.com'  # Votre adresse e-mail
    smtp_password = 'LMSINV@info23'  # Mot de passe de votre adresse e-mail

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
        return render_template('confirmation_postul.html', message='Nous vous reviendrons après analyse de votre dossier', title='Votre dossier a été soumis avec succès', image='../assets/newsletter.jfif')
    except Exception as e:
        print(e)
        return render_template('confirmation_postul.html', message='Erreur du serveur, veuillez réessayer dans un moment', title='Veuillez réessayer dans un moment', image='../assets/wrong.jfif')


@app.route('/souscription_conf/<int:id>', methods=['POST'])
def souscription_conf(id):
    try:
        userName = request.form['userName']
        userEmail = request.form['userEmail']
        subscribeToNotifications = True if request.form.get('notif') == 'on' else False

        souscription = Souscripconf(name=userName, email=userEmail, idconf=id, sub=subscribeToNotifications)
        db.session.add(souscription)
        db.session.commit()

        return render_template('confirmation_postul.html', message='Nous vous enverrons le lien de la conférence très prochainement', title='Vous êtes désormais parmi les participants de cette conférence')
    except Exception as e:
        print(e)
        return render_template('confirmation_postul.html', message='Erreur du serveur', title='Veuillez réessayer dans un moment', image='../assets/wrong.jfif')

@app.route('/souscription_form/<int:id>', methods=['POST'])
def souscription_form(id):
    try:
        userName = request.form['userName']
        userEmail = request.form['userEmail']
        subscribeToNotifications = True if request.form.get('notif') == 'on' else False

        souscription = SouscriptionFormation(name=userName, email=userEmail, sub=subscribeToNotifications)
        db.session.add(souscription)
        db.session.commit()

        return redirect(f'/formation/{id}')
    except Exception as e:
        print(e)
        return render_template('confirmation_postul.html', message='Erreur lors de la soumission du formulaire', title='Veuillez réessayer dans un moment', image='../assets/wrong.jfif')


@app.route('/newsletter', methods=['POST'])
def newsletter():
    try:
        email = request.form['email']

        # Vérifie si l'e-mail existe déjà dans la base de données
        existing_subscriber = Newsletter.query.filter_by(email=email).first()

        # Si l'abonné existe déjà, renvoyer une réponse appropriée
        if existing_subscriber:
            return render_template('newsletter_msg.html', message=f'Cet adresse mail {email} est déjà abonné à notre newsletter', title='OOPS...', image='../assets/wrong.jfif')

        # Si l'abonné n'existe pas, ajouter un nouvel enregistrement
        new_subscriber = Newsletter(email=email)
        db.session.add(new_subscriber)
        db.session.commit()

        # Réponse de succès
        return render_template('newsletter_msg.html', message='Vous recevrez prochainement le prochain numéro de notre newsletter.', title='Merci de vous être abonné', image='../assets/newsletter.jfif')
    except Exception as e:
        print(e)
        return render_template('newsletter_msg.html', message='Erreur lors de l\'abonnement à la newsletter', title='Veuillez réessayer dans un moment', image='../assets/wrong.jfif')




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
    return render_template('log.html', errorMessage='')

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
        formations = ContentFormation.query.filter_by(theme_formation_id=id).all()
        return render_template('formationadmin.html', formations=formations, idform=id)
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

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    func = request.form['function']
    password = request.form['password']
    confpassword = request.form['confpassword']
    hashed_password =generate_password_hash(password)

    if password == confpassword:
        registration = Registration(name=name, email=email, func=func, password=hashed_password)
        db.session.add(registration)
        db.session.commit()
        return redirect('/log')
    else:
        return render_template('regist.html', errorMessage='Mot de passe non correspondant')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = Registration.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['isLoggedIn'] = True
        return redirect('/adminpage')
    else:
        return render_template('log.html', errorMessage='Adresse e-mail ou mot de passe incorrect')


@app.route('/enregistrer-article', methods=['POST'])
def enregistrer_article():
    titre = request.form['titre']
    contenu = request.form['contenu']
    image = request.files['image']
    image_path = os.path.join('assets', 'images_1', image.filename)
    image.save(image_path)
    article = Blog(titre=titre, description=contenu, image_path=image_path)
    db.session.add(article)
    db.session.commit()
    return redirect('/confirmationblog')

# Route pour enregistrer un événement
@app.route('/enregistrer-event', methods=['POST'])
def enregistrer_event():
    titre = request.form['titre']
    description = request.form['contenu']
    lieu = request.form['lieu']
    date = datetime.strptime(request.form['date'], '%Y-%m-%d')
    image = request.files['image']
    image_path = os.path.join('assets', 'images_1', image.filename)
    image.save(image_path)
    lien = request.form['lien']
    conference = Conference(titre=titre, description=description, lieu=lieu, date=date, image_path=image_path, lien=lien)
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
@app.route('/enregistrer-offer', methods=['POST'])
def enregistrer_offer():
    annonce_type = request.form['annonce-type']
    contenu = request.form['contenu']
    fonc = request.form['fonc']
    image = request.files['image']
    image_path = os.path.join('assets', 'images_1', image.filename)
    image.save(image_path)
    offre = Offre(type=annonce_type, description=contenu, fonc=fonc, image_path=image_path)
    db.session.add(offre)
    db.session.commit()
    return redirect('/confirmationoffre')

# Route pour enregistrer un projet
@app.route('/enregistrer-projet', methods=['POST'])
def enregistrer_projet():
    titre = request.form['titre']
    description = request.form['contenu']
    image = request.files['image']
    image_path = os.path.join('assets', 'images_1', image.filename)
    image.save(image_path)
    projet = Projet(titre=titre, description=description, image_path=image_path)
    db.session.add(projet)
    db.session.commit()
    return redirect('/confirmationprojet')

# Route pour afficher les détails d'un article de blog
@app.route('/details_blog/<int:id>')
def details_blog(id):
    blog = Blog.query.get(id)
    if blog:
        return render_template('details_blog.html', blog=blog)
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

# Route pour afficher les détails d'un projet
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

@app.route('/addformcontent/<int:id>')
def addformcontent(id):
    if 'isLoggedIn' in session and session['isLoggedIn']:
        return render_template('addformcontent.html', idform=id)
    else:
        return "Impossible"

@app.route('/formations')
def formations():
    formations = ThemeFormation.query.all()
    return render_template('formations.html', formations=formations)

@app.route('/formation/<int:id>')
def formation(id):
    formation = ThemeFormation.query.get_or_404(id)
    return render_template('formation.html', formation=formation)

@app.route('/comment/<int:idform>')
def comment(idform):
    commentaires = CommentaireFormation.query.filter_by(formation_id=idform).all()
    return render_template('commentaire.html', commentaires=commentaires)

@app.route('/enregistrer-commentaire/<int:idf>', methods=['POST'])
def enregistrer_commentaire(idf):
    contenu = request.form['commentaire']
    userName = request.form['username']
    dateCommentaire = datetime.now()
    nouveau_commentaire = CommentaireFormation(contenu=contenu, auteur=userName, formation_id=idf, date=dateCommentaire)
    db.session.add(nouveau_commentaire)
    db.session.commit()
    return redirect('/comment/' + idf)

@app.route('/emploi/<int:id>')
def emploi(id):
    offre = Offre.query.get_or_404(id)
    return render_template('emploi.html', offre=offre)

@app.route('/emplois')
def emplois():
    offres = Offre.query.filter_by(type='emploi').all()
    return render_template('emplois.html', offres=offres)

@app.route('/stage')
def stage():
    offres = Offre.query.filter_by(type='stage').all()
    return render_template('emplois.html', offres=offres)

@app.route('/ajouter-formation/<int:id>', methods=['POST'])
def ajouter_formation(id):
    try:
        idform = int(id)
        titre = request.form['titre']
        description = request.form['description']
        fichiers = request.files.getlist('fichiers[]')

        # Construction des chemins des fichiers
        path = ', '.join(['/assets/images_1/' + file.filename for file in fichiers])

        # Enregistrement des données dans la base de données
        nouvelle_formation = ContentFormation(titre=titre, description=description, path=path, themeFormationId=idform)
        db.session.add(nouvelle_formation)
        db.session.commit()

        return redirect('/confirmationoffre')
    except Exception as error:
        print('Erreur lors de l\'ajout de la formation :', error)
        return jsonify(message='Une erreur s\'est produite lors de l\'ajout de la formation'), 500

@app.route('/formationview/<int:idf>/<int:id>', methods=['GET'])
def voir_formation(idf, id):
    try:
        form = ContentFormation.query.filter_by(id=id, themeFormationId=idf).first()
        if form:
            commentaires = CommentaireFormation.query.filter_by(formationId=id).all()
            formations = form.path.split(',')
            return render_template('formationview.html', form=form, formations=formations, idf=idf, commentaires=commentaires)
        else:
            return render_template('pas_element.html')
    except Exception as error:
        print('Erreur lors de la récupération de la formation :', error)
        return jsonify(message='Une erreur s\'est produite lors de la récupération de la formation'), 500

@app.route('/supprimerblog/<int:id>', methods=['GET'])
def supprimer_blog(id):
    try:
        blog = Blog.query.get(id)
        if blog:
            db.session.delete(blog)
            db.session.commit()
            return 'Blog supprimé avec succès.'
        else:
            return 'Blog non trouvé.'
    except Exception as error:
        print('Une erreur s\'est produite lors de la suppression du blog :', error)
        return 'Une erreur s\'est produite lors de la suppression du blog.', 500

@app.route('/supprimerconfs/<int:id>', methods=['GET'])
def supprimer_conference(id):
    try:
        conference = Conference.query.get(id)
        if conference:
            db.session.delete(conference)
            db.session.commit()
            return 'Conférence supprimée avec succès.'
        else:
            return 'Conférence non trouvée.'
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
            return "Offre d'emploi supprimée avec succès."
        else:
            return "Offre d'emploi non trouvée."
    except Exception as error:
        print('Une erreur s\'est produite lors de la suppression de l\'offre d\'emploi :', error)
        return "Une erreur s'est produite lors de la suppression de l'offre d'emploi.", 500


@app.route('/Supprimerformation/<int:idf>/<int:id>', methods=['GET'])
def supprimer_contenu_formation(idf, id):
    try:
        content_formation = ContentFormation.query.filter_by(id=id, theme_formation_id=idf).first()
        if content_formation:
            db.session.delete(content_formation)
            db.session.commit()
            return 'Contenu de la formation supprimé avec succès.'
        else:
            return 'Contenu de la formation non trouvé.'
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
            return 'Formations supprimées avec succès.'
        else:
            return 'Thème de formation non trouvé.'
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
            return 'Projet supprimé avec succès.'
        else:
            return 'Projet non trouvé.'
    except Exception as error:
        print('Une erreur s\'est produite lors de la suppression du projet :', error)
        return 'Une erreur s\'est produite lors de la suppression du projet.', 500


if __name__ == "__main__":
    app.run(debug=True)
