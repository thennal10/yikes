import requests
from aniffinity import Aniffinity
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

URL = 'https://graphql.anilist.co'
MODEL = None
FRIENDLIST = None

def follower_scores(animeId, friendlist):
    return_array = [10000 for i in friendlist]
    for c, follower in enumerate(friendlist):
        for media in follower:
            if media['mediaId'] == animeId:
                return_array[c] = media['score']

    return return_array


def create_friendlist(response):
    # get the user id and name

    user_id = response.json()['data']['User']['id']
    username = response.json()['data']['User']['name']

    # get the user's following
    query = """
    query ($userId: Int!) {
      Page (page: 1, perPage: 50) {
        following (userId: $userId) {
          id
          name
        }
      }
    }
    """

    response = requests.post(URL, json={'query': query, 'variables': {'userId': user_id}})
    follower_list = response.json()['data']['Page']['following']


    # create a list of variables to pass to query
    args = ["("] + [f"$c{x}: Int!, " for x, f in enumerate(follower_list)] + [")"]
    args[-2] = args[-2][:-2]
    str_args = "".join(args)


    friendlist = [[] for i in follower_list]

    # get the follower lists and add it to friendlist
    pg = 1
    while(True):
        # complicated query that just gets the pg'th page of follower lists
        query = """
            query """ + str_args + " {"
        variables = {}

        for c, follower in enumerate(follower_list):
            query += f"\n      f{c}:" + """ Page (page: """ + f'{pg}' + """, perPage: 50) {
                mediaList(userId:""" + f"$c{c}" + """, sort: SCORE_DESC) {
                  score(format: POINT_10_DECIMAL)
                  mediaId
                }
              }"""
            variables[f'c{c}'] = follower['id']
        query += "\n    }"

        response = requests.post(URL, json={'query': query, 'variables': variables})
        fx = response.json()['data']

        # check if the score is zero and append the list of entries to each of the follower's sublist
        brk = True
        for c in range(len(follower_list)):
            fxc = fx[f'f{c}']['mediaList']
            if len(fxc) > 0 and not fxc[0]['score'] == 0:
                brk = False
                fxc = [i for i in fxc if i['score'] != 0]
                friendlist[c] += fxc

        # yeet out if all scored anime have been recorded
        if brk:
            return friendlist

        pg += 1


def model_predict(search):
    global MODEL

    query = """
    query ($search: String) {
      Media (search: $search) {
        id
        title {
          userPreferred
        }
      }
    }
    """
    response = requests.post(URL, json={'query': query, 'variables': {'search': search}})

    mediaId = response.json()['data']['Media']['id']
    print( response.json()['data']['Media']['title']['userPreferred'])

    if MODEL is None or FRIENDLIST is None:
        return "No model found. Train a model with ``score predictor: [username]``"

    X = np.array(follower_scores(mediaId, FRIENDLIST)).reshape(1, -1)
    print(X)
    return MODEL.predict(X)


def model_create(search):
    global MODEL, FRIENDLIST

    # get the userid
    query = """
    query ($search: String) {
      User (search: $search) {
        id
        name
      }
    }
    """
    User_response = requests.post(URL, json={'query': query, 'variables': {'search': search}})

    # get the user medialist
    query = """
    query ($userId: Int!) {"""

    # because the max limit of a single page is 50 entries
    for pg in range(1, 100):
        query += """
          pg""" + f"{pg}" + """: Page (page: """ + f"{pg}" + """, perPage: 50) {
            mediaList (userId: $userId, sort: SCORE_DESC) {
              score(format: POINT_10_DECIMAL)
              mediaId
            }
          }
        """

    query += """
    }
    """

    variables = {'userId': User_response.json()['data']['User']['id']}
    Userlist_response = requests.post(URL, json={'query': query, 'variables': variables})

    userlist = []

    # remove unscored media and concatenate the seperate pages into one list
    brk = False
    for i in range(1, 100):
        page = Userlist_response.json()['data'][f'pg{i}']['mediaList']
        for c, score in enumerate([x['score'] for x in page]):
            if score == 0:
                userlist += page[:c]
                brk = True
                break

        if brk:
            break
        userlist += page

    print(userlist)
    X, y = [], []
    friendlist = create_friendlist(User_response)
    for media in userlist:
        X.append(follower_scores(media['mediaId'], friendlist))
        y.append(round(media['score']))

    print(X)
    print(y)
    X = np.array(X)
    y = np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    clf = SVC(kernel='rbf', gamma='scale')
    clf.fit(X_train, y_train)
    predicted = clf.predict(X_test)
    print(y_test)
    print(predicted)
    # get the accuracy
    print(accuracy_score(y_test, predicted)*100)
    print("yoot")

    MODEL = clf
    FRIENDLIST = friendlist


model_create('ladypeach')
print(model_predict('hanappe bazooka'))