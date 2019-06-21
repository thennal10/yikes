def leaderboard_sort(l):
    return l[1]


def leaderboard_name(l):
    name = ""
    for count, element in enumerate(l):
        name += element.capitalize()
        if count != len(l) - 1:
            name += "/"
    return name


def peachlator(message):
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
    return " ".join(new_message)


async def word_leaderboard(message, serv):
    spacedmsg = message.content.split()
    actmsg = " ".join(spacedmsg[2:])
    if len(spacedmsg) >= 3 and spacedmsg[1].isdigit():
        msglimit = int(spacedmsg[1])
        searchwords = actmsg.split(" + ")
        print(searchwords)
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
        peeps.sort(key=leaderboard_sort, reverse=True)
        leaderboard = f"**The {leaderboard_name(searchwords)} Leaderboard**```\nRank  | Name\n\n"
        for count, peep in enumerate(peeps[:10]):
            leaderboard += f"""[{count + 1}]   > {peep[0]}: {peep[1]}\n"""
        leaderboard += "```"
        return leaderboard
    else:
        return "Usage: ``word_leaderboard [no. of messages] [phrase1] + [phrase2]...``"


def strokify(message):
    try:
        iscap = False
        outputmsg = message.content[9:]
        for count, character in enumerate(outputmsg):
            if character.isalpha():
                if iscap:
                    outputmsg[count] = character.capitalize()
                iscap = not iscap
        return "".join(outputmsg)
    except:
        return "Usage: ``strokify: [sentence]``"


def score(message):
    num = 0
    for character in message.content[7:]:
        num += ord(character)
    num = (num % 10) + 1
    print(num)
    return f"bout {num}/10"


def custom(message, conn):
    msplit = message.content.split()
    if len(msplit) == 3:

        # SQL shit
        sql = """INSERT INTO customcommands (command, output) VALUES (%s, %s);"""
        data = (msplit[1], msplit[2])
        cur = conn.cursor()
        try:
            cur.execute(sql, data)
            conn.commit()
            cur.close()
            return "Immortalized!"
        except:
            conn.rollback()
            conn.commit()
            cur.close()
            return "Command already exists, or you fucking broke the bot. Congrats, asshole."
    else:
        return "Usage: ``custom: [command] [link/text]``"


def call_custom(message, conn):
    msplit = message.content.split()
    if len(msplit) == 2:

        # More SQL shit
        sql = """SELECT command, output FROM customcommands;"""
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()

        while row is not None:
            if row[0] == msplit[1]:
                cur.close()
                return row[1]
            row = cur.fetchone()
        return "That command doesn't exist, you dumb fuck. Use ``list!`` for a list of existing commands"
    else:
        return "Usage: ``yi! [command]``"


def remove(message, conn):
    msplit = message.content.split()
    # Even more SQL
    sql = """SELECT command, output FROM customcommands;"""
    cur = conn.cursor()
    cur.execute(sql)
    row = cur.fetchone()
    while row is not None:
        if row[0] == msplit[1]:
            sql = f"""DELETE FROM customcommands WHERE command ='{msplit[1]}';"""
            cur.execute(sql)
            return "Removal successful."
        row = cur.fetchone()
    cur.close()
    return "That command doesn't exist, you dumb fuck. Use ``list!`` to get a list of existing commands"


def cclist(conn):
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
    cur.close()
    return listoutput


async def pixiv(message, api, os, discord):
    msplit = message.content.split()
    x = 0

    if len(msplit) == 1:
        msplit.append('day')
    elif msplit[1] == "help":
        await message.channel.send("**Usable modes:** ```day, week, month, day_male, day_female, week_original, "
                                   "week_rookie, day_r18, day_male_r18, day_female_r18, week_r18, week_r18g```")
        return 1

    # get ranking: 1-30
    # mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
    json_result = api.illust_ranking(msplit[1])
    print(json_result)

    try:
        print(json_result.illusts)
    except AttributeError:
        await message.channel.send(f"The flying fuck is {msplit[1]}? Use ``pixiv! help`` to see the available modes")
        return 1

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
                    return 0
                except:
                    x = x + 1


def danbooru(message, danb, oldposts):
    msplit = message.content.split()
    pg = 1
    tag = ["order:score", "rating:safe"]
    tag.extend(msplit[1:])

    stag = " ".join(tag)
    print(stag)
    while True:
        try:
            postlist = danb.post_list(limit=100, page=pg, tags=stag)
        except:
            return "U dun fucked up boi. Probably used more than one tag."
        if len(postlist) == 0:
            return "Tag not found. Try again?"
        for count, post in enumerate(postlist):
            if post['id'] in oldposts:
                continue
            else:
                oldposts.append(post['id'])
                try:
                    return post['large_file_url']
                except KeyError:
                    return post['file_url']
        pg = pg + 1


def reddit_get(message, reddit, oldsubmissions):
    msplit = message.content.split()
    
    if msplit[0] == "reddit!search":
        searchmode = True
    else:
        searchmode = False

    if len(msplit) <= 1:
        return "Usage: ``reddit! [subreddit] [hot/top/new/controversial] [timeframe for top]`` \nor ``reddit!search " \
               "[subreddit] [relevance/top/new] [search terms]``"

    subreddit = reddit.subreddit(msplit[1])

    # check if inputs are valid
    try:
        if subreddit != 'all':
            reddit.subreddits.search_by_name(subreddit, exact=True)
            subreddit.subreddit_type
    except:
        return "Not a valid subreddit."

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
                    return "Not a valid timeframe."

            elif msplit[2] == 'new':
                submission_list = subreddit.new()
            elif msplit[2] == 'controversial':
                submission_list = subreddit.controversial()
            else:
                return "Not a valid sort type."
        else:
            submission_list = subreddit.hot()

    # go through submissions to find a suitable one
    for submission in submission_list:
        if not submission.is_self:
            if submission not in oldsubmissions:
                oldsubmissions.append(submission)
                return submission.url
    return "Either the subreddit only has text posts, or you've been calling the command too many times. Try a different" \
           " subreddit or sorting mode, or just wait a while."


async def yikes(message, discord):

    commandlist = {"peachlator:": "What it says on the tin",
                   "word_leaderboard": "Creates a leaderboard based on a given word/phrase",
                   "score:": "Outputs a random score based on the given word/phrase",
                   "strokify:": "tUrNs GiVeN tExT iNtO tHiS",
                   "custom:": "Creates a simple input output command",
                   "yi!": "Calls a custom command",
                   "remove:": "Removes a custom command",
                   "list!": "Lists all custom commands",
                   "pixiv!": "Posts a random illustration from pixiv based on rankings. Use 'pixiv! help' to get list of modes",
                   "danbooru!": "Posts top ranking illustrations from danbooru based on given tags.",
                   "reddit!": "Posts a reddit submission based on given parameters",
                   "reddit!search": "Posts the results from a reddit search query based on given parameters"
                   }

    embed = discord.Embed(title="**Yikes! at your service.**",
                          description="What would you like for your order?\n \n \n", color=9911100)
    embed.set_author(name="Someone called?",
                     icon_url="https://cdn.discordapp.com/attachments/469524231244349452/584658974515920912/360fx360f.png")
    embed.set_footer(text="Ping premed if anything breaks down.",
                     icon_url="https://cdn.discordapp.com/attachments/469524231244349452/584658974515920912/360fx360f.png")
    for command in commandlist:
        embed.add_field(name=f"**{command}**", value=commandlist[command], inline=False)
    await message.channel.send(content=None, embed=embed)
