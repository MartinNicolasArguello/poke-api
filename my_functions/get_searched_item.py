import requests
base_url = 'https://pokeapi.co/api/v2/item/'

# search individual item with the provided name


def get_searched_item(searched_item):
    results = []
    try:
        response = requests.get(base_url + searched_item).json()
    except:
        return "not-found"

    found_item = {"name": response["name"],
                  "image": response["sprites"]["default"]}
    results.append(found_item)
    return results
