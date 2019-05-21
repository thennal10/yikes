import discord
import os


def baha_sort(l):
    return l[1]


def leaderboard_name(l):
    name = ""
    for count, element in enumerate(l):
        name += element.capitalize()
        if count != len(l) - 1:
            name += "/"
    return name


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
        if len(new_message) <= 1:
            new_message[0] = "Peachlator, at your service. Usage: ``peachlator: [text]``"
        else:
            new_message[0] = "Translation:"
        for i in range(len(new_message)):
            for key in trans_dict:
                splitkey = key.split()
                #don't ask
                for j, skey in enumerate(splitkey):
                    if i + j >= len(new_message):
                        incl = False
                        break
                    elif skey != new_message[i + j]:
                        incl = False
                        break
                    incl = True
                splitval = trans_dict[key].split()
                #still need to add a case for when splitval > splitkey but eh
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
        smsg = message.content.split()
        if len(smsg) >= 3 and smsg[1].isdigit():
            msglimit = int(smsg[1])
            searchwords = smsg[2:]
            print(searchwords)
            await message.channel.send("Loading...")
            peeps = [["N/A", 0]]
            for chan in serv.text_channels:
                perm = chan.permissions_for(serv.me)
                if perm.read_message_history:
                    async for msg in chan.history(limit=msglimit):
                        for searchword in searchwords:
                            if searchword in msg.content and not msg.author.bot:
                                found = 0
                                for peep in peeps:
                                    if msg.author.name == peep[0]:
                                        peep[1] += 1
                                        found = 1
                                        break
                                if found == 0:
                                    peeps.append([msg.author.name, 0])
                print(chan)
            peeps.sort(key=baha_sort, reverse=True)
            leaderboard = f"**The {leaderboard_name(searchwords)} Leaderboard**```\nRank  | Name\n\n"
            for count, peep in enumerate(peeps[:10]):
                leaderboard += f"""[{count + 1}]   > {peep[0]}: {peep[1]}\n"""
            leaderboard += "```"
            await message.channel.send(leaderboard)
        else:
            await message.channel.send("Usage: ``word_leaderboard [no. of messages] [word1] [word2]...``")
    elif message.content.startswith("score:"):
        num = 0
        for character in message.content[7:]:
            num += ord(character)
        num = (num % 10) + 1
        print(num)
        await message.channel.send(f"bout {num}/10")


token = os.environ.get("TOKEN")
client.run(token)
