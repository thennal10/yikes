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
