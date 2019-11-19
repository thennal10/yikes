import pandas as pd
import numpy as np
from discord.ext import commands


def make_pairs(corpus):
    for i in range(len(corpus) - 1):
        yield (corpus[i], corpus[i + 1])


class GeneratorCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='generator')
    async def generate(self, ctx, user, first_word='N/A', n_words: int = 30):

        print(user)
        print(first_word)
        print(n_words)

        df = pd.read_csv('data/content_analysis.csv')
        df = df.loc[df['name'] == user]['content']
        ls = [x for x in df.values.tolist() if str(x) != 'nan']
        precorpus = " \n ".join(ls)
        corpus = precorpus.split(" ")

        if corpus == ['']:
            await ctx.send("Couldn't find that user. Note that it is case-sensitive, and try again.")
            return

        pairs = make_pairs(corpus)

        word_dict = {}
        for word_1, word_2 in pairs:
            if word_1 in word_dict.keys():
                word_dict[word_1].append(word_2)
            else:
                word_dict[word_1] = [word_2]

        if first_word == 'N/A':
            first_word = np.random.choice(corpus)
        chain = [first_word]

        i = 0
        while i < n_words:
            try:
                new_word = np.random.choice(word_dict[chain[-1]])
            except KeyError:
                await ctx.send("First word given is not in the corpus. Try again with a word that the user has said"
                               " at least once.")
                return
            chain.append(new_word)
            if new_word != "\n":
                i += 1
        await ctx.send(' '.join(chain))

    @generate.error
    async def generate_error(self, ctx, error):
        await ctx.send("Usage: ``!generator [user] [first word] [number of words]``")


def setup(bot):
    bot.add_cog(GeneratorCog(bot))
