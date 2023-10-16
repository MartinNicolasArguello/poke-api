import requests
base_url = 'https://pokeapi.co/api/v2/pokemon/'

# search individual pokemon with the provided name


def get_searched_pokemon(searched_pokemon):
    results = []
    try:
        response = requests.get(base_url + searched_pokemon).json()
    except:
        return "not-found"

    types = []
    for type in response["types"]:
        types.append(type["type"]["name"])

    found_pokemon = {"name": response["name"], "image": response["sprites"]["other"]
                     ["official-artwork"]["front_default"], "types": types, "height": response["height"], "weight": response["weight"]}
    results.append(found_pokemon)

    return results
