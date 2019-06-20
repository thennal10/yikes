import discord
import os
import psycopg2
from pixivpy3 import *
from pybooru import Danbooru
import praw
#from dotenv import load_dotenv

#load_dotenv()
oldposts = []
oldsubmissions = []


def baha_sort(l):
    return l[1]


def leaderboard_name(l):
    name = ""
    for count, element in enumerate(l):
        name += element.capitalize()
        if count != len(l) - 1:
            name += "/"
    return name

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
puser = os.environ['PIXIV_USERNAME']
ppass = os.environ['PIXIV_PASSWORD']
client_id = os.environ['REDDIT_CLIENT_ID']
client_secret = os.environ['REDDIT_CLIENT_SECRET']

danb = Danbooru('danbooru')
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='yikes:v1 by u/thennal')

client = discord.Client()
api = AppPixivAPI()
api.login(puser, ppass)

commandlist = {"peachlator:": "What it says on the tin",
               "word_leaderboard": "Creates a leaderboard based on a given word/phrase",
               "score:": "Outputs a random score based on the given word/phrase",
               "strokify:": "tUrNs GiVeN tExT iNtO tHiS",
               "custom:": "Creates a simple input output command",
               "yi!": "Calls a custom command",
               "remove:": "Removes a custom command",
               "list!": "Lists all custom commands",
               "pixiv!": "Posts a random illustration from pixiv based on rankings. Use 'pixiv! help' to get list of modes"
               "danbooru!: Posts top ranking illustrations from danbooru based on given tags. "
               }

print("Running!")
@client.event
async def on_message(message):

    if message.author == client.user:
        return

    serv = message.guild

    # commands
    if message.content.startswith("peachlator:"):
        # load dictionary
        trans_dict = {}
        file = open("peachdict.txt", "r")
        for line in file:
            isv = False
            value = ""
            key = ""
            for word in line.split():
                if word == "-":
                    isv = True
                elif isv:
                    strword = word.rstrip("\n")
                    value += strword + " "
                else:
                    key += word + " "
            trans_dict[key.rstrip()] = value.rstrip()

        # replace words
        new_message = message.content.split()
        if len(new_message) <= 1:
            new_message[0] = "Peachlator, at your service. Usage: ``peachlator: [text]``"
        else:
            new_message[0] = "Translation:"
        for i in range(len(new_message)):
            for key in trans_dict:
                splitkey = key.split()
                # don't ask
                for j, skey in enumerate(splitkey):
                    if i + j >= len(new_message):
                        incl = False
                        break
                    elif skey != new_message[i + j]:
                        incl = False
                        break
                    incl = True
                splitval = trans_dict[key].split()
                # still need to add a case for when splitval > splitkey but eh
                if incl:
                    for k, val in enumerate(splitval):
                        new_message[i + k] = val
                    for l in range((len(splitkey)) - (len(splitval))):
                        del new_message[i + l + len(splitval)]
                    i = i - len(splitval)

        # send result
        new_message = " ".join(new_message)
        await message.channel.send(new_message)
    elif message.content.startswith("word_leaderboard"):
        # redo this with pandas later
        spacedmsg = message.content.split()
        actmsg = " ".join(spacedmsg[2:])
        if len(spacedmsg) >= 3 and spacedmsg[1].isdigit():
            msglimit = int(spacedmsg[1])
            searchwords = actmsg.split(" + ")
            print(searchwords)
            await message.channel.send("Loading...")
            peeps = [["N/A", 0]]
            for chan in serv.text_channels:
                perm = chan.permissions_for(serv.me)
                if perm.read_message_history:
                    async for msg in chan.history(limit=msglimit):
                        for searchword in searchwords:
                            if searchword in msg.content.lower() and not msg.author.bot:
                                found = 0
                                for peep in peeps:
                                    if msg.author.name == peep[0]:
                                        peep[1] += 1
                                        found = 1
                                        break
                                if found == 0:
                                    peeps.append([msg.author.name, 1])
                print(chan)
            peeps.sort(key=baha_sort, reverse=True)
            leaderboard = f"**The {leaderboard_name(searchwords)} Leaderboard**```\nRank  | Name\n\n"
            for count, peep in enumerate(peeps[:10]):
                leaderboard += f"""[{count + 1}]   > {peep[0]}: {peep[1]}\n"""
            leaderboard += "```"
            await message.channel.send(leaderboard)
        else:
            await message.channel.send("Usage: ``word_leaderboard [no. of messages] [phrase1] + [phrase2]...``")
    elif message.content.startswith("score:"):
        num = 0
        for character in message.content[7:]:
            num += ord(character)
        num = (num % 10) + 1
        print(num)
        await message.channel.send(f"bout {num}/10")
    elif message.content.startswith("strokify:"):
        try:
            iscap = False
            outputmsg = list(message.content[9:])
            for count, character in enumerate(outputmsg):
                if character.isalpha():
                    if iscap:
                        outputmsg[count] = character.capitalize()
                    iscap = not iscap
            await message.channel.send("".join(outputmsg))
        except:
            await message.channel.send("Usage: ``strokify: [sentence]``")
    elif message.content.startswith("custom:"):
        msplit = message.content.split()
        if len(msplit) == 3:

            # SQL shit
            sql = """INSERT INTO customcommands (command, output) VALUES (%s, %s);"""
            data = (msplit[1], msplit[2])
            cur = conn.cursor()
            try:
                cur.execute(sql, data)
                await message.channel.send("Immortalized!")
            except:
                await message.channel.send("Command already exists, or you fucking broke the bot. Congrats, asshole.")
                conn.rollback()
            conn.commit()
            cur.close()
        else:
            await message.channel.send("Usage: ``custom: [command] [link/text]``")
    elif message.content.startswith("yi!"):
        msplit = message.content.split()
        if len(msplit) == 2:

            # More SQL shit
            sql = """SELECT command, output FROM customcommands;"""
            cur = conn.cursor()
            cur.execute(sql)
            row = cur.fetchone()
            found = False
            while row is not None:
                if row[0] == msplit[1]:
                    await message.channel.send(row[1])
                    found = True
                    break
                row = cur.fetchone()
            if not found:
                await message.channel.send("That command doesn't exist, you dumb fuck")
            cur.close()
        else:
            await message.channel.send("Usage: ``yi! [command]``")
    elif message.content.startswith("remove:"):
        msplit = message.content.split()
        # Even more SQL
        sql = """SELECT command, output FROM customcommands;"""
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        found = False
        while row is not None:
            if row[0] == msplit[1]:
                sql = f"""DELETE FROM customcommands WHERE command ='{msplit[1]}'';"""
                cur.execute(sql)
                found = True
                break
            row = cur.fetchone()
        if not found:
            await message.channel.send("That command doesn't exist, you dumb fuck")
    elif message.content == "list!":
        # EVEN MORE SQL
        sql = """SELECT command, output FROM customcommands;"""
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        listoutput = "**List of Custom Commands**\n```"
        while row is not None:
            listoutput += f"""{row[0]}\n"""
            row = cur.fetchone()
        listoutput += "```"
        await message.channel.send(listoutput)
    elif message.content.startswith("pixiv!"):
        msplit = message.content.split()
        cont = True
        x = 0

        if len(msplit) == 1:
            msplit.append('day')
        elif msplit[1] == "help":
            await message.channel.send("**Usable modes:** ```day, week, month, day_male, day_female, week_original,"
                                       " week_rookie, day_r18, day_male_r18, day_female_r18, week_r18, week_r18g```")
            cont = False

        # get ranking: 1-30
        # mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
        json_result = api.illust_ranking(msplit[1])
        print(json_result)
        if cont:
            try:
                print(json_result.illusts)
            except AttributeError:
                await message.channel.send(f"The flying fuck is {msplit[1]}? Use ``pixiv! help`` to see the available modes")
                cont = False
        if cont:
            # download random illust in top 30 week rankings to 'dl' dir
            directory = "dl"
            if not os.path.exists(directory):
                os.makedirs(directory)

            # while loop is for if the first 30 results all have blacklisted tags
            while True:
                notfound = True
                for count, illust in enumerate(json_result.illusts[x:]):
                    if illust.type != "manga" and len(illust.meta_pages) == 0:
                        tempillust = illust
                        x = x + 1
                        print(x)
                        notfound = False
                        break
                if notfound or x >= 29:
                    print(json_result)
                    x = 0
                    next_qs = api.parse_qs(json_result.next_url)
                    json_result = api.illust_ranking(**next_qs)
                else:
                    # dl the illust
                    illust = tempillust
                    image_url = illust.meta_single_page.get('original_image_url', illust.image_urls.large)
                    url_basename = os.path.basename(image_url)
                    extension = os.path.splitext(url_basename)[1]
                    name = "illust_id_%d_%s_%s" % (illust.id, illust.title, extension)
                    print(illust)
                    if os.path.isfile(f"dl/{name}"):
                        x = x + 1
                        print(x)
                    else:
                        try:
                            api.download(image_url, path=directory, name=name)
                            f = open(f"dl/{name}", "rb")
                            outputfile = discord.File(fp=f)
                            await message.channel.send(
                                content=f"Source: <https://www.pixiv.net/member_illust.php?mode=medium&illust_id={illust.id}>",
                                file=outputfile)
                            break
                        except:
                            x = x + 1
    elif message.content.startswith("danbooru!"):
        msplit = message.content.split()
        pg = 1
        tag = ["order:score", "rating:safe"]
        tag.extend(msplit[1:])

        stag = " ".join(tag)
        print(stag)
        found = False
        while True:
            try:
                postlist = danb.post_list(limit=100, page=pg, tags=stag)
            except:
                await  message.channel.send("U dun fucked up boi. Probably used more than one tag.")
                break
            if len(postlist) == 0:
                await message.channel.send("Tag not found. Try again?")
                break
            for count, post in enumerate(postlist):
                if post['id'] in oldposts:
                    continue
                else:
                    oldposts.append(post['id'])
                    try:
                        await message.channel.send(post['large_file_url'])
                    except KeyError:
                        await  message.channel.send(post['file_url'])
                    found = True
                    break
            if found:
                break
            else:
                pg = pg + 1
    elif message.content.startswith("reddit!"):
        msplit = message.content.split()
        cont = True
        if msplit[0] == "reddit!search":
            searchmode = True
        else:
            searchmode = False

        if len(msplit) <= 1:
            await message.channel.send("Usage: ``reddit! [subreddit] [hot/top/new/controversial] [timeframe for top]``"
                                       "\nor ``reddit!search [subreddit] [relevance/top/new] [search terms]``")
            cont = False

        subreddit = reddit.subreddit(msplit[1])

        # check if inputs are valid
        try:
            if cont and subreddit != 'all':
                reddit.subreddits.search_by_name(subreddit, exact=True)
                subreddit.subreddit_type
        except:
            await message.channel.send("Not a valid subreddit.")
            cont = False

        if cont:
            if searchmode:
                if len(msplit) > 2:
                    if msplit[2] == 'relevance':
                        submission_list = subreddit.search(query=" ".join(msplit[3:]))
                    elif msplit[2] == 'top':
                        submission_list = subreddit.search(query=" ".join(msplit[3:]), sort='top')
                    elif msplit[2] == 'new':
                        submission_list = subreddit.search(query=" ".join(msplit[3:]), sort='new')
                    else:
                        submission_list = subreddit.search(query=" ".join(msplit[2:]))
                else:
                    submission_list = subreddit.search(query=" ".join(msplit[2:]))
            else:
                if len(msplit) > 2:
                    if msplit[2] == 'hot':
                        submission_list = subreddit.hot()
                    elif msplit[2] == 'top':
                        if len(msplit) > 3:
                            timeframe = msplit[3]
                        else:
                            timeframe = 'day'
                        try:
                            submission_list = subreddit.top(timeframe)
                        except ValueError:
                            await message.channel.send("Not a valid timeframe.")
                            cont = False

                    elif msplit[2] == 'new':
                        submission_list = subreddit.new()
                    elif msplit[2] == 'controversial':
                        submission_list = subreddit.controversial()
                    else:
                        await message.channel.send("Not a valid sort type.")
                        cont = False
                else:
                    submission_list = subreddit.hot()

        # go through submissions to find a suitable one
        if cont:
            found = False
            for submission in submission_list:
                if not submission.is_self:
                    if submission not in oldsubmissions:
                        await message.channel.send(submission.url)
                        oldsubmissions.append(submission)
                        found = True
                        break
            if not found:
                await message.channel.send("Either the subreddit only has text posts, or you've been calling the "
                                           "command too many times. Try a different subreddit or sorting mode, or just "
                                           "wait a while.")

    elif message.content == "yikes!":
        embed = discord.Embed(title="**Yikes! at your service.**",
                              description="What would you like for your order?\n \n \n", color=9911100)
        embed.set_author(name="Someone called?",
                         icon_url="https://cdn.discordapp.com/attachments/469524231244349452/584658974515920912/360fx360f.png")
        embed.set_footer(text="Ping premed if anything breaks down.",
                         icon_url="https://cdn.discordapp.com/attachments/469524231244349452/584658974515920912/360fx360f.png")
        for command in commandlist:
            embed.add_field(name=f"**{command}**", value=commandlist[command], inline=False)
        await message.channel.send(content=None, embed=embed)


token = os.environ.get("TOKEN")
client.run(token)
