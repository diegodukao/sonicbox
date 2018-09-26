from kivy.storage.jsonstore import JsonStore


def get_storage():
    return JsonStore('src/data/user_config.json')


def update_favorite_samples(favorites):
    store = get_storage()
    store.put('samples', favorites=favorites)
