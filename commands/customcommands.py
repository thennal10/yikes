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