from routes import db
from datetime import datetime, timedelta

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2500))
    email = db.Column(db.String, unique=True)
    func = db.Column(db.String(2500))
    password = db.Column(db.String(2500))
    date=db.Column(db.DateTime, default=datetime.now)

class Souscripconf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2500))
    email = db.Column(db.String, unique=True)
    idconf = db.Column(db.Integer)
    sub = db.Column(db.Boolean)
    date=db.Column(db.DateTime, default=datetime.now)

class SouscriptionFormation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2500))
    email = db.Column(db.String, unique=True)
    sub = db.Column(db.Boolean)
    date=db.Column(db.DateTime, default=datetime.now)

class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    name=db.Column(db.String(2500))

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(2500))
    description = db.Column(db.String(2500))
    imagePath = db.Column(db.String(2500))
    date=db.Column(db.DateTime, default=datetime.now)

class Projet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(2500))
    description = db.Column(db.String(2500))
    imagePath = db.Column(db.String(2500))
    date=db.Column(db.DateTime, default=datetime.now)

class Offre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(2500))
    description = db.Column(db.String(2500))
    imagePath = db.Column(db.String, default="../static/assets/images/lms-logo-removebg-preview.png")
    fonc = db.Column(db.String, default="")
    date = db.Column(db.DateTime, default=datetime.now)

class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(2500))
    description = db.Column(db.String(2500))
    imagePath = db.Column(db.String(2500))
    conferencier=db.Column(db.String(2500))
    lien = db.Column(db.String(2500))
    type=db.Column(db.String(2500))
    lieu = db.Column(db.String, default="")
    date = db.Column(db.DateTime, default=datetime.now)


class ThemeFormation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(2500))
    description = db.Column(db.String(2500))
    date=db.Column(db.DateTime, default=datetime.now)



class ContentFormation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(2500))
    description = db.Column(db.String(2500))
    path = db.Column(db.String(2500))
    theme_id = db.Column(db.Integer, db.ForeignKey('theme_formation.id')) 
    date=db.Column(db.DateTime, default=datetime.now)


class CommentaireFormation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.String(2500))
    auteur = db.Column(db.String(2500))
    date = db.Column(db.DateTime)
    formation_id = db.Column(db.Integer, db.ForeignKey('content_formation.id'))

class CommentaireBlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.String(2500))
    auteur = db.Column(db.String(2500))
    date = db.Column(db.DateTime)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    date=db.Column(db.DateTime, default=datetime.now)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    statut = db.Column(db.String(100),default="En attente")
    message = db.Column(db.Text)
    date=db.Column(db.DateTime, default=datetime.now)

class Postul(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)
    cv = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey('offre.id'))
    date=db.Column(db.DateTime, default=datetime.now)
    
