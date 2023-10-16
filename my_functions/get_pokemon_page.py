import requests
from website import model


def get_pokemon_page(data):
    results = []
    # if first group, fetch the pokemons in the database.
    if (not data["previous"]):
        database_pokemon = model.Pokemon.query.all()
        for i in range(len(database_pokemon)):
            if (not database_pokemon[i].black_listed):
                my_pokemon = {"name": database_pokemon[i].name, "image": database_pokemon[i].image,
                              "types": database_pokemon[i].type, "height": database_pokemon[i].height, "weight": database_pokemon[i].weight}
                results.append(my_pokemon)
    # fetch data from every pokemon in "results", also checking in my database if they are blacklisted
    for pokemon in data["results"]:
        current_pokemon = model.Pokemon.query.get(
            pokemon["name"])
        if (current_pokemon):
            if (current_pokemon.black_listed or current_pokemon.modified):
                continue
            new_pokemon = {"name": current_pokemon.name, "image": current_pokemon.image,
                           "types": current_pokemon.type, "height": current_pokemon.height, "weight": current_pokemon.weight}
        else:
            response = requests.get(pokemon["url"]).json()

            types = []
            for type in response["types"]:
                types.append(type["type"]["name"])

            new_pokemon = {"name": response["name"].capitalize(), "image": response["sprites"]["other"]
                           ["official-artwork"]["front_default"], "types": types, "height": response["height"], "weight": response["weight"]}

        results.append(new_pokemon)
    return results


# <!-- sprites => other => official-artwork => front_default -->
