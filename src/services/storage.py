from kivy.storage.jsonstore import JsonStore


def save_favorite_sample(sample_name):
    store = JsonStore('src/data/user_config.json')

    if store.exists('samples') and ('favorites' in store.get('samples')):
        fav_list = store.get('samples')['favorites']
    else:
        fav_list = []

    fav_list.append(sample_name)
    store.put('samples', favorites=fav_list)


def remove_favorite_sample(sample_name):
    store = JsonStore('src/data/user_config.json')

    fav_list = store.get('samples')['favorites']
    fav_list.remove(sample_name)

    store.put('samples', favorites=fav_list)
