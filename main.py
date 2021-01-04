from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
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
    }
]

GAMES = [
    'League of Legends',
    'Valorant',
    'Rainbow6 Siege',
    'CSGO'
]

@main.route('/')
def index():
    return render_template('login.html')

PATH_CREATE = '/create'
@main.route(PATH_CREATE)
@login_required
def profile():
    return render_template('create_new_tournament.html', path=PATH_CREATE, name=current_user.name, links=LINKS, games=GAMES)

@main.route(PATH_CREATE, methods=['POST'])
def create_new_tournament():
    print('Received new torunament')
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


    return redirect(url_for('main.profile'))

PATH_CURRENT = '/current'

@main.route(PATH_CURRENT)
@login_required
def current_tournaments():
    return render_template('current_tournament.html', path=PATH_CURRENT, links=LINKS )

PATH_AUTOREPLIES = '/autoreplies'
@main.route(PATH_AUTOREPLIES)
@login_required
def autoreplies():
    return render_template('autoreplies.html', path=PATH_AUTOREPLIES, links=LINKS )
