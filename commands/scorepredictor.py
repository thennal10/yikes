from jikanpy import Jikan
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
#from aniffinity import Aniffinity
from tqdm import tqdm

jikan = Jikan()

class MALfriend:
  def __init__(self, name, list, affinity):
    self.name = name
    self.list = list
    self.affinity = affinity


# Bad code but meh
def get_user(username):
    user = jikan.user(username=username, request='animelist', argument='completed')['anime']
    user = user + jikan.user(username=username, request='animelist', argument='completed', page=2)['anime']
    user = user + jikan.user(username=username, request='animelist', argument='completed', page=3)['anime']
    user = user + jikan.user(username=username, request='animelist', argument='dropped')['anime']
    return user


# Finds and compares friend scores of an anime; outputs a single number based on an equation
def find_anime(anime_id, friends):
    numerator = 0
    denominator = 0
    for friend in friends:
        for anime in friend.list:
            if anime['mal_id'] == anime_id:
                score = anime['score']
                if score != 0:
                    affinity = (friend.affinity/100) + 2
                    numerator += score*affinity
                    denominator += affinity
    try:
        final_score = numerator/denominator
    except ZeroDivisionError:
        final_score = 0
    return final_score


# creates a list of MALfriend objects based on the given user's friend list
def friendlist_creator(username):
    client_friendlist = jikan.user(username=username, request='friends')['friends']
    #af = Aniffinity(username, base_service="MyAnimeList")

    friendlist = []
    for friend in tqdm(client_friendlist):
        attempts = 0
        while attempts < 5:
            try:
                friend_animelist = get_user(username=friend['username'])
                affinity, shared = 100, 1#af.calculate_affinity(friend['username'], service="MyAnimeList")
                friendlist.append(MALfriend(friend['username'], friend_animelist, affinity))
                break
            except Exception as e:
                print(e)
                attempts += 1
    return friendlist


# creates the nn model based on the given user
def model_creator(message):
    msplit = message.content.split()
    username = msplit[2]
    user = get_user(username)
    #anime = jikan.search('anime', msplit[3])['results'][0]
    friendlist = friendlist_creator(username)
    X, y = [], []
    for anime in user:
        if anime['score'] != 0:
            final_score = find_anime(anime['mal_id'], friendlist)
            if final_score != 0:
                X.append(final_score)
                y.append(anime['score'])

    X = np.array(X).reshape(-1, 1)
    print(X.shape)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    clf = SVC(kernel='rbf', gamma='scale')
    clf.fit(X_train, y_train)
    predicted = clf.predict(X_test)
    print(y_test)
    print(predicted)
    # get the accuracy
    return f"Model saved. Accuracy score of {accuracy_score(y_test, predicted)*100}%, which, mind you, is very good for " \
           f"the laughably small sample size I got from your pitiful list.", clf, friendlist


def score_predictor(message, model, friendlist):
    search = message.content[9:]
    anime = jikan.search('anime', search)['results'][0]
    X = [[find_anime(anime['mal_id'], friendlist)]]
    return f"""I'd guess a score of {model.predict(X)[0]} for {anime['title']}"""