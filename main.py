from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Tournament, Game, AutoReply
from . import db

main = Blueprint('main', __name__, template_folder='templates')

LINKS = [{
        'name':'Create New',
        'path': '/create',
    },{
        'name': 'Current Tournaments',
        'path': '/current'
    },{
        'name':'Automatic Replys',
        'path': '/autoreplies'
    },{
        'name': 'Manage Games',
        'path': '/managegames'
    }
]

@main.route('/')
def index():
    return render_template('login.html')

PATH_CREATE = '/create'
@main.route(PATH_CREATE)
@login_required
def profile():
    available_games = Game.query.all()
    print(available_games)
    return render_template('create_new_tournament.html', path=PATH_CREATE, name=current_user.name, links=LINKS, games=available_games)

@main.route(PATH_CREATE, methods=['POST'])
def create_new_tournament():
    print('Received new tournament')
    tournament_name = request.form.get('tournamentName')
    tournament_game = request.form.get('game')
    tournament_days = request.form.getlist('days') #Use getlist() to get multiple checked checkboxes
    tournament_hour = request.form.get('gameHour')

    print('Imprimiendo toda la data')
    print(request.form)

    #Yes, this is quite dumb
    tournament_hour_lunes = request.form.get('Lunes')
    tournament_hour_martes = request.form.get('Martes')
    tournament_hour_miercoles = request.form.get('Miercoles')
    tournament_hour_jueves = request.form.get('Jueves')
    tournament_hour_viernes = request.form.get('Viernes')
    tournament_hour_sabado = request.form.get('Sabado')
    tournament_hour_domingo = request.form.get('Domingo')

    new_Tournament = Tournament(tournament_name=tournament_name, game_id=1)
    db.session.add(new_Tournament)
    db.session.commit()
    print(new_Tournament.tournament_name)

    return redirect(url_for('main.profile'))

PATH_CURRENT = '/current'

@main.route(PATH_CURRENT)
@login_required
def current_tournaments():
    tournament_lit = Tournament.query.limit(10).all()
    print( dir(tournament_lit[0].game) )   
    return render_template('current_tournament.html', path=PATH_CURRENT, links=LINKS, tournaments=tournament_lit )

PATH_AUTOREPLIES = '/autoreplies'
@main.route(PATH_AUTOREPLIES)
@login_required
def autoreplies():
    replies_list = AutoReply.query.limit(20).all()
    return render_template('autoreplies.html', replies_list=replies_list, path=PATH_AUTOREPLIES, links=LINKS )

@main.route('/autoreplies', methods=['POST'])
@login_required
def add_new_reply():
    print('Recibiendo peticion')
    print(request.form['trigger'])
    print(request.form['reply'])
    new_autoreply = AutoReply(trigger=request.form['trigger'], reply=request.form['reply'])
    db.session.add(new_autoreply)
    db.session.commit()
    return redirect(url_for('main.autoreplies'))

@main.route('/autoreplies/remove/<id>')
@login_required
def remove_autoreply_by_id(id):
    print('Removing autoreply from DB')
    autoreply = AutoReply.query.filter_by(id=id).first()
    db.session.delete(autoreply)
    db.session.commit() 
    return redirect(url_for('main.add_new_reply'))

@main.route('/managegames')
@login_required
def manage_games():
    games_list = Game.query.limit(10).all()
    return render_template('managegames.html', games_list=games_list, links=LINKS, path='/managegames')

@main.route('/managegames', methods=['POST'])
@login_required
def add_new_game():
    print('Create new game petition received')
    game_title_form = request.form['game_title']
    game_query = Game.query.filter_by(title=game_title_form).first()
    if game_query:
        #Mandar un Flash diciendo que ya existe el juego
        print('Ya existe este juego en la base de datos')
    else:
        #Guardar el juego en la DB
        print('Creando juego en la Base de datos')
        new_game = Game(title=game_title_form)
        db.session.add(new_game)
        db.session.commit()
    print(game_query)
    return redirect(url_for('main.manage_games'))

@main.route('/remove/<id>')
@login_required
def remove_game_by_id(id):
    print('Remove Game from DB')
    game = Game.query.filter_by(id=id).first()
    print(game.title)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for('main.manage_games'))