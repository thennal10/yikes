import discord

def baha_sort(l):
    return l[1]

client = discord.Client()
print("Running!")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    serv = message.guild
    #if message.content == "server_stats":
    #    chanl = serv.by_category()
    #    for i in range(len(chanl)):
    #        if chanl[i][0].id == 469563734566633473:
    #            await message.channel.send(f"""Number of rewatches: {len(chanl[i][1])}""")
    if message.content.startswith("peachlator"):
        #load dictionary
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

        #replace words
        new_message = message.content.split()
        new_message[0] = "Translation:"
        for i in range(len(new_message)):
            for key in trans_dict:
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
                if incl:
                    for k in range(len(splitval)):
                        new_message[i + k] = splitval[k]
                    for l in range((len(splitkey)) - (len(splitval))):
                        del new_message[i + l + len(splitval)]
                    i = i - len(splitval)

        #send result
        new_message = " ".join(new_message)
        await message.channel.send(new_message)
    elif message.content == "bahaha_scoreboard":
        # redo this with pandas
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
        while len(peeps) < 10:
            peeps.append(["N/A", 0])
        print(peeps)
        await message.channel.send(f"""

**The Bahaha Leaderboard**
```
Rank  | Name

[1]   > {peeps[0][0]}: {peeps[0][1]}
[2]   > {peeps[1][0]}: {peeps[1][1]}
[3]   > {peeps[2][0]}: {peeps[2][1]}
[4]   > {peeps[3][0]}: {peeps[3][1]}
[5]   > {peeps[4][0]}: {peeps[4][1]}
[6]   > {peeps[5][0]}: {peeps[5][1]}
[7]   > {peeps[6][0]}: {peeps[6][1]}
[8]   > {peeps[7][0]}: {peeps[7][1]}
[9]   > {peeps[8][0]}: {peeps[8][1]}
[10]  > {peeps[9][0]}: {peeps[9][1]}
```
      """)


# keep_alive()
# token = os.environ.get("secretToken")
client.run("NTM2NDAyMzk1MTE1MTU5NTYz.XNT_9Q.2RPxP8nQzqQL0ugOqkgS4LeFhEs")
