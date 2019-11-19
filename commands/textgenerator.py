import pandas as pd
import numpy as np


def make_pairs(corpus):
    for i in range(len(corpus) - 1):
        yield (corpus[i], corpus[i + 1])

def generate(message):
    msplit = message.content.split()
    print(msplit)
    if len(msplit) == 3:
        user = msplit[2]
        n_words = 30
        first_word = False
    elif len(msplit) == 4:
        user, first_word = msplit[2:4]
        n_words = 30
    elif len(msplit) == 5:
        user, first_word, n_words = msplit[2:]
        try:
            n_words = int(n_words)
        except ValueError:
            return "Number of words must be an integer. Format: ``text generator! [user] [first word]" \
                   " [number of words]``"
    else:
        return "Format: ``text generator! [user] [first word] [number of words]``"

    print(user)
    print(first_word)
    print(n_words)

    df = pd.read_csv('data/content_analysis.csv')
    df = df.loc[df['name'] == user]['content']
    ls = [x for x in df.values.tolist() if str(x) != 'nan']
    precorpus = " \n ".join(ls)
    corpus = precorpus.split(" ")

    if corpus == ['']:
        return "Couldn't find that user. Note that it is case-sensitive, and try again."

    pairs = make_pairs(corpus)

    word_dict = {}
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

    if not first_word:
        first_word = np.random.choice(corpus)
    chain = [first_word]

    i = 0
    while i < n_words:
        try:
            new_word = np.random.choice(word_dict[chain[-1]])
        except KeyError:
            return "First word given is not in the corpus. Try again with a word that the user has said at least once."
        chain.append(new_word)
        if new_word != "\n": i+= 1
    return ' '.join(chain)