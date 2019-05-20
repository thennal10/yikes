import discord
import os


def baha_sort(l):
    return l[1]


client = discord.Client()
print("Running!")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    serv = message.guild

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
        new_message[0] = "Translation:"
        for i in range(len(new_message)):
            for key in trans_dict:
                #don't ask
                splitkey = key.split()
                for j in range(len(splitkey)):
                    if i + j >= len(new_message):
                        incl = False
                        break
                    elif splitkey[j] != new_message[i + j]:
                        incl = False
                        break
                    incl = True
                splitval = trans_dict[key].split()
                #still need to add a case for when splitval > splitkey but eh
                if incl:
                    for k in range(len(splitval)):
                        new_message[i + k] = splitval[k]
                    for l in range((len(splitkey)) - (len(splitval))):
                        del new_message[i + l + len(splitval)]
                    i = i - len(splitval)

        # send result
        new_message = " ".join(new_message)
        await message.channel.send(new_message)
    elif message.content == "bahaha_leaderboard":
        # redo this with pandas later
        await message.channel.send("Loading...")
        peeps = [["N/A", 0]]

        for chan in serv.text_channels:
            perm = chan.permissions_for(serv.me)
            if perm.read_message_history:
                async for msg in chan.history(limit=3000):
                    if "the" in msg.content:
                        found = 0
                        for j in range(len(peeps)):
                            if msg.author.name == peeps[j][0]:
                                peeps[j][1] += 1
                                found = 1
                                break
                        if found == 0:
                            peeps.append([msg.author.name, 0])

        peeps.sort(key=baha_sort, reverse=True)
        leaderboard = "**The Bahaha Leaderboard**```\nRank  | Name\n\n"
        for i in range(len(peeps)):
            leaderboard += f"""[{i + 1}]   > {peeps[i][0]}: {peeps[i][1]}\n"""
        leaderboard += "```"
        await message.channel.send(leaderboard)
    elif message.content.startswith("immortalize:"):
        msplit = message.content.split()
        if len(msplit) == 3:
            file = open("customcommands.txt", "+a")
            file.write(msplit[1] + " - " + msplit[2])
            await message.channel.send("works?")
        await message.channel.send("kinda?")



token = os.environ.get("TOKEN")
client.run(token)
