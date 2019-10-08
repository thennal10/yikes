import requests
import logging
from saucenao import SauceNao

saucenao = SauceNao(directory='commands/data', databases=999, minimum_similarity=65, combine_api_types=False, api_key='',
                    exclude_categories='', move_to_categories=False,  use_author_as_category=False,
                    output_type=SauceNao.API_HTML_TYPE, start_file='', log_level=logging.ERROR,
                    title_minimum_similarity=90)


def source_from_message(message):
    image_url = message.content[8:]
    output = sauce_finder(image_url)
    if output == 0:
        return "SauceNAO didn't find jack shit so ¯\_(ツ)_/¯"
    else:
        return output


def sauce_finder(image_url):
    img_data = requests.get(image_url).content

    with open('commands/data/anime_bois/temp.jpg', 'wb') as handler:
        handler.write(img_data)

    filtered_results = saucenao.check_file(file_name="anime_bois/temp.jpg")
    print(filtered_results)
    if len(filtered_results) == 0:
        return 0
    for result in filtered_results:
        try:
            unparsed = result['data']['content'][0].split('\n')[0].split(" ")
            for count, word in enumerate(unparsed):
                if word == "Pixiv":
                    if unparsed[count + 1] == "ID:":
                        pixiv_id = unparsed[count + 2]
                    elif unparsed[count + 1][0] == "#":
                        pixiv_id = unparsed[count + 1][1:]
            return f"Source: <https://www.pixiv.net/en/artworks/{pixiv_id}>"
        except Exception as e:
            print(e)