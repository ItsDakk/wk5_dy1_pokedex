from flask import render_template, request, flash, redirect, url_for
import requests
from app.blueprints.auth.forms import PokedexForm, CatchEm
from . import bp as main
from flask_login import login_required, current_user
from app.models import Pokemon, PokeTeam

@main.route('/', methods = ['GET'])
# @login_required
def index():
    return render_template('index.html.j2')

@main.route('/poketeam', methods = ['GET', 'POST'])
def poketeam():
    return render_template('poketeam.html.j2')

@main.route('/pokedex', methods = ['GET', 'POST'])
def pokedex():
    # @login_required
    form = PokedexForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_name = form.pokemon_name.data.lower()

        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'.lower()
        response = requests.get(url)
        if not response.ok:
            error_string = "Invalid Pokemon name"
            return render_template('pokedex.html.j2', error = error_string, form=form)
        data = response.json()
        if not response.json():
            error_string = "We had an error"
            return render_template('pokedex.html.j2', error = error_string, form=form)

        pokemon_dict = {
            "name": data['name'].capitalize(),
            "bexp" : data['base_experience'],
            "shiny": data['sprites']['front_shiny'],
            "ability": data['abilities'][0]['ability']['name'].capitalize(),
            "hp": data['stats'][0]['base_stat'],
            "attack": data['stats'][1]['base_stat'],
            "defense": data['stats'][0]['base_stat'],
            }

        p = Pokemon.query.filter_by(name = pokemon_dict['name']).first()
        if p:
            pass
        else:
            p = Pokemon()
            p.from_dict(pokemon_dict)
            p.save()

        return render_template('pokedex.html.j2', pokemon = pokemon_dict, form=form, pokemon_id = p.pokemon_id)
    return render_template('pokedex.html.j2', form=form)

@main.route('/catch/<int:id>', methods = ['GET', 'POST'])
def catch(id):
    
    flash('Captured!', 'success')
        
    p = Pokemon.query.filter_by(pokemon_id = id).first()
    t = PokeTeam.query.filter_by(user_id = current_user.id).first()
    t.edit_team(p)
    t.save_team()

    return redirect(url_for('main.pokedex'))

@main.route('/pokeroyale', methods = ['GET', 'POST'])
# @login_required
def pokeroyale():
    pass
    
    return render_template('pokeroyale.html.j2')



