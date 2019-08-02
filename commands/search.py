import requests


def anisearch(message):
    if len(message.content.split()) < 2:
        return "Usage: ``anime! [search]``"

    search = message.content[7:]

    query = '''
    query ($search: String) {
        Media (search: $search, type: ANIME) {
            id
        }
    }
    '''
    variables = {
        'search': search
    }
    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})

    if response:
        # convert the response to a dict using json() and get the id
        anime_id = response.json()['data']['Media']['id']
        return f"https://anilist.co/anime/{anime_id}"
    else:
        return "ERROR. ERROR. ERROR. PING PREMED SO HE CAN SACRIFICE A GOAT TO THE BOT GODS"


def mangasearch(message):
    if len(message.content.split()) < 2:
        return "Usage: ``manga! [search]``"

    search = message.content[7:]

    query = '''
    query ($search: String) {
        Media (search: $search, type: MANGA) {
            id
        }
    }
    '''
    variables = {
        'search': search
    }
    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})

    if response:
        # convert the response to a dict using json() and get the id
        manga_id = response.json()['data']['Media']['id']
        return f"https://anilist.co/manga/{manga_id}"
    else:
        return "ERROR. ERROR. ERROR. PING PREMED SO HE CAN SACRIFICE A GOAT TO THE BOT GODS"
