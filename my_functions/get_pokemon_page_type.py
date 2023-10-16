import requests
from website import model


def get_pokemon_page_type(data, offset, type):
    results = []
    offset = int(offset)
    limit = len(data["pokemon"])

    # If offset is 0, check for pokemon of the wanted type in my database
    if (offset == 0):
        my_pokemon = model.Pokemon.query.filter(
            model.Pokemon.type.contains(type))

        if (my_pokemon.count()):
            for i in range(my_pokemon.count()):
                if (not my_pokemon[i].black_listed):
                    new_pokemon = {"name": my_pokemon[i].name.capitalize(
                    ), "image": my_pokemon[i].image, "types": my_pokemon[i].type, "height": my_pokemon[i].height, "weight": my_pokemon[i].weight}
                    results.append(new_pokemon)

    for pokemon in data["pokemon"][offset:offset+20 if offset+20 < limit else limit]:
        current_pokemon = model.Pokemon.query.get(
            pokemon["pokemon"]["name"])
        if (current_pokemon):
            if (current_pokemon.black_listed or current_pokemon.modified):
                continue
        else:
            response = requests.get(pokemon["pokemon"]["url"]).json()

            types = []
            for type in response["types"]:
                types.append(type["type"]["name"])

            new_pokemon = {"name": response["name"].capitalize(), "image": response["sprites"]["other"]
                           ["official-artwork"]["front_default"], "types": types, "height": response["height"], "weight": response["weight"]}

            results.append(new_pokemon)

    offset = offset + 20
    previous = offset - 40
    if (offset > limit):
        offset = "limit"

    return results, str(previous), str(offset)
