from Main import *
from datetime import datetime, timedelta

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250000))
    email = db.Column(db.String(250000), unique=True)
    func = db.Column(db.String(250000))
    password = db.Column(db.String(250000))
    date=db.Column(db.DateTime, default=datetime.now)

class Souscripconf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250000))
    email = db.Column(db.String(250000))
    idconf = db.Column(db.Integer)
    sub = db.Column(db.Boolean)
    date=db.Column(db.DateTime, default=datetime.now)

class SouscriptionFormation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250000))
    email = db.Column(db.String(250000))
    sub = db.Column(db.Boolean)
    date=db.Column(db.DateTime, default=datetime.now)

class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250000), unique=True)
    name=db.Column(db.String(250000))

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(250000))
    description = db.Column(db.String(250000))
    imagePath = db.Column(db.String(250000))
    date=db.Column(db.DateTime, default=datetime.now)

class Projet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(250000))
    description = db.Column(db.String(250000))
    imagePath = db.Column(db.String(250000))
    date=db.Column(db.DateTime, default=datetime.now)

class Offre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(250000))
    description = db.Column(db.String(250000))
    imagePath = db.Column(db.String(250000), default="../static/assets/images/lms-logo-removebg-preview.png")
    fonc = db.Column(db.String(250000), default="")
    date = db.Column(db.DateTime, default=datetime.now)

class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(250000))
    description = db.Column(db.String(250000))
    imagePath = db.Column(db.String(250000))
    conferencier=db.Column(db.String(250000))
    lien = db.Column(db.String(250000))
    type=db.Column(db.String(250000))
    lieu = db.Column(db.String(250000), default="")
    date = db.Column(db.DateTime, default=datetime.now)


class ThemeFormation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(250000))
    description = db.Column(db.String(250000))
    date=db.Column(db.DateTime, default=datetime.now)



class ContentFormation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(250000))
    description = db.Column(db.String(250000))
    path = db.Column(db.String(250000))
    theme_id = db.Column(db.Integer, db.ForeignKey('theme_formation.id')) 
    date=db.Column(db.DateTime, default=datetime.now)


class CommentaireFormation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.String(250000))
    auteur = db.Column(db.String(250000))
    date = db.Column(db.DateTime)
    formation_id = db.Column(db.Integer, db.ForeignKey('content_formation.id'))

class CommentaireBlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.String(2500000))
    auteur = db.Column(db.String(250000))
    date = db.Column(db.DateTime)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    date=db.Column(db.DateTime, default=datetime.now)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100000))
    email = db.Column(db.String(100000))
    subject = db.Column(db.String(100000))
    statut = db.Column(db.String(100000),default="En attente")
    message = db.Column(db.Text)
    date=db.Column(db.DateTime, default=datetime.now)

class Postul(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100000))
    name = db.Column(db.String(100000))
    email = db.Column(db.String(100000))
    message = db.Column(db.Text)
    cv = db.Column(db.String(255000))
    post_id = db.Column(db.Integer, db.ForeignKey('offre.id'))
    date=db.Column(db.DateTime, default=datetime.now)
    
