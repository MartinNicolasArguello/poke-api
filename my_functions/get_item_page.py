import requests


def get_item_page(data):
    results = []
    for item in data["results"]:
        response = requests.get(item["url"]).json()

        new_item = {"name": response["name"].capitalize(), "image": response["sprites"]["default"],
                    }
        results.append(new_item)
    return results
