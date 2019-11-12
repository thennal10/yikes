import requests
from bs4 import BeautifulSoup

def expand(message):
    msplit = message.split()
    URL = msplit[0]

    if "twitter.com" not in URL:
        return "Not a link to a tweet."

    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')
    images_unparsed = soup.find_all("meta", {"property": "og:image"})

    if len(images_unparsed) == 1:
        return "Tweet does not have any images or only has one image."

    output = ""
    for image in images_unparsed[1:]:
        output += f"{image['content']}\n"

    return output