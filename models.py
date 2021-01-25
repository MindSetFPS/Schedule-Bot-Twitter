from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))   
    tournaments = db.relationship('Tournament', backref='game')

class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_name = db.Column(db.String(128))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

#########################################################
class AutoReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trigger = db.Column(db.String(280))
    reply = db.Column(db.String(280))
##########################################################