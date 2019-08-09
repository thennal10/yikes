import requests
from jikanpy import Jikan
jikan = Jikan()

def anisearch(message):
    if len(message.content.split()) < 2:
        return "Usage: ``anime! [search]``"

    search = message.content[7:]
    search_result = jikan.search('anime', search)
    title = search_result['results'][0]['title']
    result_url = search_result['results'][0]['url']

    query = '''
    query ($search: String) {
        Media (search: $search, type: ANIME) {
            id
        }
    }
    '''
    variables = {
        'search': title
    }
    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})
    if response:
        # convert the response to a dict using json() and get the id
        anime_id = response.json()['data']['Media']['id']
        return f"{result_url}\nhttps://anilist.co/anime/{anime_id}"
    else:
        return f"{result_url}\nAnilist URL not found"


def mangasearch(message):
    if len(message.content.split()) < 2:
        return "Usage: ``manga! [search]``"

    search = message.content[7:]
    search_result = jikan.search('manga', search)
    title = search_result['results'][0]['title']
    result_url = search_result['results'][0]['url']

    query = '''
    query ($search: String) {
        Media (search: $search, type: MANGA) {
            id
        }
    }
    '''
    variables = {
        'search': title
    }
    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})

    if response:
        # convert the response to a dict using json() and get the id
        manga_id = response.json()['data']['Media']['id']
        return f"{result_url}\nhttps://anilist.co/manga/{manga_id}"
    else:
        return f"{result_url}\nAnilist URL not found"
