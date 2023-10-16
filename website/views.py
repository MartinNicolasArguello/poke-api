from flask import Blueprint, render_template, request, redirect
import requests
import my_functions
from . import db
from .model import Pokemon
views = Blueprint('views', __name__)
base_url = 'https://pokeapi.co/api/v2/pokemon/'
base_item_url = 'https://pokeapi.co/api/v2/item/'


@views.route('/')
def home():
    return render_template('base.html')


@views.route('/pokemon')
def pokemon():
    data = requests.get(
        base_url).json()
    pokemon_for_display = my_functions.get_pokemon_page(data)
    # after fetching all information, pass it to the template for it to generate cards in a loop, also important are "next"
    # and "previous", with handle the paginator-buttons
    return render_template("pokemon.html", data=pokemon_for_display,
                           previous="None" if data["previous"] is None else my_functions.get_endpoint(
                               data["previous"]),
                           next="None" if data["next"] is None else my_functions.get_endpoint(data["next"]))


@views.route('/pokemon/<endpoint>')
def pokemon_page(endpoint):
    # To search for a specific pokemon, first in the mysql database and then in the API

    data = requests.get(
        base_url + '?' + endpoint).json()
    pokemon_for_display = my_functions.get_pokemon_page(data)
    return render_template("pokemon.html", data=pokemon_for_display,
                           previous="None" if data["previous"] is None else my_functions.get_endpoint(
                               data["previous"]),
                           next="None" if data["next"] is None else my_functions.get_endpoint(data["next"]))


@views.route('/item')
def item():

    data = requests.get(
        base_item_url).json()
    item_for_display = my_functions.get_item_page(data)
    return render_template("item.html", data=item_for_display,
                           previous="None" if data["previous"] is None else my_functions.get_item_endpoint(
                               data["previous"]),
                           next="None" if data["next"] is None else my_functions.get_item_endpoint(data["next"]))


@views.route('/item/<endpoint>')
def item_page(endpoint):
    data = requests.get(
        base_item_url + '?' + endpoint).json()
    item_for_display = my_functions.get_item_page(data)
    return render_template("item.html", data=item_for_display,
                           previous="None" if data["previous"] is None else my_functions.get_item_endpoint(
                               data["previous"]),
                           next="None" if data["next"] is None else my_functions.get_item_endpoint(data["next"]))


@views.route('/search-pokemon', methods=["POST"])
def search_pokemon():
    # To search for a specific pokemon, first in the mysql database and then in the API

    if (request.form['search_pokemon_name']):
        searched_pokemon = Pokemon.query.get((
            request.form['search_pokemon_name'].lower()))

        if (searched_pokemon):
            if (searched_pokemon.black_listed):
                return render_template("error.html", error_message="NO POKEMON FOUND")
            return render_template("pokemon.html", data=[{"name": searched_pokemon.name, "types": [searched_pokemon.type], "height": searched_pokemon.height, "weight": searched_pokemon.weight, "image": searched_pokemon.image}],
                                   previous="None",
                                   next="None")
        else:
            data = my_functions.get_searched_pokemon(
                request.form['search_pokemon_name'].lower())
            if (data == "not-found"):
                return render_template("error.html", error_message="NO POKEMON FOUND")
            else:
                return render_template("pokemon.html", data=data,
                                       previous="None",
                                       next="None")
    else:
        return render_template('error.html', error_message="NO POKEMON FOUND")


@views.route('/search-pokemon-type/', methods=["POST"])
def search_pokemon_type_form():
    return redirect("/search-pokemon-type/" + request.form["search_pokemon_type"] + "/0")


@views.route('/search-pokemon-type/<type>/<offset>')
def search_pokemon_type(type, offset):
    # Check if type exists in API
    try:
        data = requests.get(
            "https://pokeapi.co/api/v2/type/" + type.lower()).json()
    except:
        # If not, now check the database
        my_pokemon = Pokemon.query.filter(
            Pokemon.type.contains(type))
        # Fetch database results
        if my_pokemon.count():
            results = []
            for i in range(my_pokemon.count()):
                if (not my_pokemon[i].black_listed):
                    new_pokemon = {"name": my_pokemon[i].name.capitalize(
                    ), "image": my_pokemon[i].image, "types": my_pokemon[i].type, "height": my_pokemon[i].height, "weight": my_pokemon[i].weight}
                    results.append(new_pokemon)
            return render_template("pokemon.html", data=results,
                                   previous="None", next="None")
        return render_template("error.html", error_message="NO POKEMON OF THAT TYPE FOUND")

    pokemon_for_display, previous, offset = my_functions.get_pokemon_page_type(
        data, offset, type)
    return render_template("type.html", data=pokemon_for_display, previous=previous, offset=offset, type=type)


@views.route('/search_item', methods=["POST"])
def search_item():
    # To search for a specific item, first in the mysql database and then in the API

    if (request.form['search_item_name']):
        data = my_functions.get_searched_item(
            request.form['search_item_name'])
        if (data == "not-found"):
            return render_template("error.html", error_message="NO ITEM FOUND")
        else:
            return render_template("item.html", data=data,
                                   previous="None",
                                   next="None")
    else:
        return render_template("error.html", error_message="NO ITEM FOUND")


@views.route("/add-pokemon-form")
def add_pokemon_form():
    return render_template("add-pokemon-form.html")


@views.route("/add-pokemon", methods=["POST"])
def add_pokemon():
    new_pokemon = Pokemon(name=request.form['name'].lower(), type=request.form['type'].lower(),
                          height=request.form['height'], weight=request.form['weight'], image="https://www.outcyders.net/images/quizzes/4/quizhead1.jpg", modified=False, black_listed=False)
    # validate entries
    if (my_functions.validate_pokemon(new_pokemon, "CREATE")):
        # check if name exists
        if (requests.get("https://pokeapi.co/api/v2/pokemon/" + new_pokemon.name)):
            return render_template("error.html", error_message="POKEMON ALREADY EXISTS")

        db.session.add(new_pokemon)
        db.session.commit()
        return render_template("success.html")

    else:
        return render_template("error.html", error_message="INVALID ENTRIES DETECTED")


@views.route('/edit-pokemon/<endpoint>')
def edit_pokemon_form(endpoint):

    if (Pokemon.query.get(
            endpoint)):

        current_pokemon = Pokemon.query.get(
            endpoint)
        return render_template("edit-pokemon-form.html", name=current_pokemon.name, type=current_pokemon.type, height=current_pokemon.height, weight=current_pokemon.weight, image=current_pokemon.image)

    else:
        current_pokemon = my_functions.get_searched_pokemon(endpoint)[0]
        return render_template("edit-pokemon-form.html", name=current_pokemon["name"], type=current_pokemon["types"], height=current_pokemon["height"], weight=current_pokemon["weight"], image=current_pokemon["image"])


@views.route('/edit-pokemon/<endpoint>', methods=["POST"])
def edit_pokemon(endpoint):

    # To edit a pokemon's information, after validating the inputs I look for it in the mysql database first,
    # in case that the pokemon to edit is in the API, I create a copy in my database (that will be fetched first, ignoring the one in the API)
    #  with the blacklisted property, so the original wont show up in group searches

    form_data = Pokemon(name=endpoint, type=request.form["type"],
                        height=request.form["height"], weight=request.form["weight"], image="", modified=False, black_listed=False)

    if (my_functions.validate_pokemon(form_data, "EDIT")):
        if (Pokemon.query.get(endpoint)):
            current_pokemon = Pokemon.query.get(endpoint)
            current_pokemon.name = endpoint
            current_pokemon.type = request.form["type"]
            current_pokemon.height = request.form["height"]
            current_pokemon.weight = request.form["weight"]
            db.session.commit()
            return render_template("success.html")
        else:
            current_pokemon = my_functions.get_searched_pokemon(endpoint)[0]
            new_pokemon = Pokemon(name=endpoint, type=request.form["type"],
                                  height=request.form["height"], weight=request.form["weight"], image=current_pokemon["image"], modified=True, black_listed=False)
            db.session.add(new_pokemon)
            db.session.commit()
            return render_template("success.html")
    else:
        return render_template("error.html", error_message="INVALID ENTRIES DETECTED")


@views.route('/delete-pokemon/<endpoint>', methods=["POST"])
def delete_pokemon(endpoint):

    # deleting an entry in the mysql database, or, in case that the pokemon to be deleted is in the api,
    # creating a blacklisted copy (that will be prioritized in the fetching but ignored in the rendering process)

    if (Pokemon.query.get(endpoint)):
        current_pokemon = Pokemon.query.get(endpoint)
        db.session.delete(current_pokemon)
        db.session.commit()
        return render_template("success.html")
    else:
        current_pokemon = my_functions.get_searched_pokemon(endpoint)[0]
        new_pokemon = Pokemon(name=endpoint, type=str(current_pokemon["types"]),
                              height=current_pokemon["height"], weight=current_pokemon["weight"], image=current_pokemon["image"], modified=False, black_listed=True)
        db.session.add(new_pokemon)
        db.session.commit()
        return render_template("success.html")


@views.route('/<path:path>')
def page_not_found(path):
    return render_template("error.html", error_message="PAGE NOT FOUND")
