# The Hunger Games
from math import ceil
import random

numOfDistricts = 0  # set the number of districts
initializing = True
numOfTributes = 1
# initialize some more stuff
events = []
tributes = []
dead = []
deadthisday = []
day = 1
weapon_list = ['axe', 'cleaver', 'naked waifu figurine', 'broadsword', 'bow', 'blowdart', 'anime DVD', 'dagger',
               'giant screwdriver', 'wooden club', 'explosives', 'scimitar', 'trident', 'mace']
cleavers = ['axe', 'broadsword', 'cleaver', 'scimitar']
stabbers = ['dagger', 'giant screwdriver', 'trident', 'naked waifu figurine']
clubbers = ['wooden club', 'anime DVD', 'mace']
rare_weapons_list = ['cursed sword', 'a fucking gun']


class Tribute:

    def __init__(self, nme, dist):
        self.name = nme[:-2]  # Set the name to whatever the player entered MINUS the gender and space at the end
        self.district = dist  # set the district to whatever it was assigned to.
        self.inj = False  # set inj to false by default
        self.supplies = None
        self.weapon = None
        self.partner = None
        self.done = False
        self.asleep = False
        self.kills = 0
        self.gender = nme[(len(nme) - 1):]  # get the gender the player entered. the last letter of the input

        if self.gender.lower() == "m":  # if the player is male
            # give him male pronouns
            self.hisher = "his"
            self.himher = "him"
            self.heshe = "he"
            self.hesshes = "he's"
        elif self.gender.lower() == "f":
            # give her female pronouns
            self.hisher = "her"
            self.himher = "her"
            self.heshe = "she"
            self.hesshes = "she's"
        else:
            # give them nonbinary pronouns
            # you friggin sjw ree
            self.hisher = "their"
            self.himher = "them"
            self.heshe = "they"
            self.hesshes = "they've"


def initialize(message):
    global tributes, numOfDistricts, numOfTributes, initializing
    if message.content == 'hunger games start!':
        return "Enter number of districts"
    else:
        if numOfDistricts == 0:
            numOfDistricts = int(message.content)
            return f"Name tribute #{numOfTributes}\n"
        elif numOfTributes < numOfDistricts * 2:
            tributes.append(Tribute(message.content, ceil(numOfTributes / 2)))
            numOfTributes += 1
            return f"Name tribute #{numOfTributes}\n"
        else:
            tributes.append(Tribute(message.content, ceil(numOfTributes / 2)))
            return_string = ""
            for j in range(len(tributes)):
                # Print their name, district, and gender. This is mainly for debugging purposes.
                return_string += f"{tributes[j].name}, district {tributes[j].district}, {tributes[j].gender}\n"
            initializing = False
            return return_string



def correct_grammar(input):
    changed = False
    isplit = input.split()
    olist = []
    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
                  'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'z', 'w', 'y']
    for count, word in enumerate(isplit):
        if word == 'a':
            if isplit[count + 1][0] in vowels:
                olist.append('an')
                changed = True
            else:
                olist.append(word)
        elif word == 'an':
            if isplit[count + 1][0] in consonants:
                olist.append('a')
                changed = True
            else:
                olist.append(word)
        else:
            olist.append(word)
    if not changed:
        return input
    else:
        return " ".join(olist)
# ===============================================================================

def kill(tribute):
    global tributes, dead, deadthisday
    tributes.remove(tribute)
    dead.append(tribute)
    deadthisday.append(tribute)


def pick_random_action(tribute1, tribute2):
    global tributes, dead, deadthisday

    # make their names easier to access.
    t1 = tribute1.name
    t2 = "Placeholder. If you're seeing this, premed has fucked up somewhere, that fucking idiot."
    # num picks between three overarching scenarios

    if tribute2 is None:
        num = random.randint(1, 3)  # skip tribute encounter scenarios
    else:
        t2 = tribute2.name
        if tribute1.partner == tribute2:
            num = -1
        else:
            num = random.randint(0, 3)

    if num == -1:  # partner tribute scenarios
        # check if these two chucklefucks are the only tributes alive
        if len(tributes) == 2:
            scenario = random.randint(0, 2)
            if scenario == 0:
                kill(tribute1)
                kill(tribute2)
                return f"As the game comes down to it's final day, {t1} and {t2} contemplate on what they should do." \
                    f" In the end, their bond is too strong; They try and pull the good ol' berry trick but " \
                    f"the producers ain't having it and the game ends a tragedy."
            else:
                output = f"As the game comes down to it's final day, {t1} and {t2} both know what must be done. " \
                    f"They make their way to the Cornucopia, and get ready for the final showdown.\n"

                if tribute1.weapon is not None and tribute2.weapon is None:
                    strong = tribute1
                    weak = tribute2
                elif tribute2.weapon is not None and tribute1.weapon is None:
                    strong = tribute2
                    weak = tribute1
                elif tribute1.inj and not tribute2.inj:
                    strong = tribute2
                    weak = tribute1
                elif tribute2.inj and not tribute1.inj:
                    strong = tribute1
                    weak = tribute2
                else:
                    strong = tribute1
                    weak = tribute2

                str = strong.name
                wk = weak.name

                if strong.weapon == 'cursed sword':
                    kill(strong)
                    output += f"As the fight starts, a purple light fills the sky as {str}'s cursed sword shatters and reveals it's " \
                        f"final form: A giant fucking Gundam emerges from the blinding light. Because of course it does.\n" \
                        f" As {str} prepares to become one with the robot, {strong.heshe} bids {wk} a final farewell" \
                        f" before flying off to the stars. {wk} just stands there amazed."
                    strong.name = 'Ascended ' + strong.name
                elif weak.weapon == 'cursed sword':
                    kill(weak)
                    output += f"As the fight starts, a purple light fills the sky as {wk}'s cursed sword shatters and reveals it's " \
                        f"final form; A giant fucking Gundam emerges from the blinding light. Because of course it does.\n" \
                        f" As {wk} prepares to become one with the robot, {weak.heshe} bids {str} a final farewell" \
                        f" before flying off to the stars. {str} just stands there amazed."
                    strong.name = 'Ascended ' + weak.name

                elif strong.weapon == 'a fucking gun' or weak.weapon == 'a fucking gun':
                    if strong.weapon == 'a fucking gun':
                        strong.kills += 1
                        kill(weak)
                        output += f"{str} just straights up shoots {wk} in the head with {strong.weapon}. Kind of" \
                            f"anticlimactic really."
                    elif weak.weapon == 'a fucking gun':
                        weak.kills += 1
                        kill(strong)
                        output += f"{wk} just straights up shoots {str} in the head with {weak.weapon}. Kind of" \
                            f"anticlimactic really."

                elif strong.weapon in cleavers:
                    strong.kills += 1
                    kill(weak)
                    if scenario > 7:
                        output += f"After a long battle, {str} savagely decapitates {wk} with {strong.hisher} {strong.weapon}."
                    else:
                        output += f"{str}, without hesitation, cuts {wk} down with {strong.hisher} {strong.weapon} in a single stroke."

                elif strong.weapon in stabbers:
                    strong.kills += 1
                    kill(weak)
                    if scenario > 7:
                        output += f"A final, well aimed stab by {str}'s {strong.weapon} ends {wk}'s life."
                    else:
                        output += f"After a drawn-out fight, {str} manages to catch {wk} in the throat with {strong.hisher}" \
                            f" {strong.weapon} and ends {wk}'s life."

                elif strong.weapon in clubbers:
                    strong.kills += 1
                    kill(weak)
                    output += f"A ferocious battle commences, and {str} eventually smashes {wk}'s head in with " \
                        f"{strong.hisher} {strong.weapon}."

                elif strong.weapon == 'bow' or strong.weapon == 'blowdart':
                    if strong.weapon == 'bow':
                        kill(weak)
                        output += f"After a tactical battle of wits fully utilizing their surroudings, {str} finally " \
                            f"figures out where {wk} is hiding and manages to catch {weak.himher} in the throat with" \
                            f"an arrow."
                    if strong.weapon == 'blowdart':
                        kill(weak)
                        output += f"After a tactical battle of wits fully utilizing their surroudings, {str} finally " \
                            f"figures out where {wk} is hiding and shoots out a poisoned dart. It barely pricks {wk}'s" \
                            f"skin, but it's enough: {weak.heshe} collapses soon after."
                else:
                    kill(weak)
                    kill(strong)
                    output += f"In a magnificent display of manliness, {str} and {wk} fight it out to the death, with " \
                        f"their fists, and in the end simultaneously collapse, with smiles on their faces."
                return output

        # RETAKE!
        num = random.randint(0, 5)

        # Time for us to follow our own paths, Kenny
        if num == 0:
            scenario = random.randint(0, 2)

            tribute1.partner = None
            tribute2.partner = None

            if scenario == 0:
                return f"{t1} and {t2} decide to split up and go their own ways in amicable terms while they still can."
            elif scenario == 1:
                return f"{t1} and {t2} decide to split up to hunt for food. {t2} manages to snag a wild boar and " \
                    f"makes {tribute2.hisher} way towards the rendezvous point, but {t1} is nowhere to be found.\n" \
                    f"{t1}, while chasing a rabbit, goes a little bit too far into the forest and finds " \
                    f"{tribute1.himher}self lost in a labyrinth of trees."
            elif scenario == 2:
                choice = random.choice([f'It contains simple words of farewell, fitting for {t2}.',
                                        'It contains a single word scrawled out with fresh ink - Goodbye.',
                                        f"It contains a heartfelt message thanking {t1} for their friendship.",
                                        f"Oh wait, it isn't a note, just the tissue that {t2} used for "
                                        f"{tribute2.hisher} 'stress relief session' last night. Yikes."])
                return f"{t1} wakes up at dawn to find {t2} missing, and a note left behind; {choice}"

        # 3v1 always going to be unfair
        elif num == 1:
            tribute3 = random.choice([x for x in tributes if (x != tribute1 and x != tribute2)])
            t3 = tribute3.name
            scenario = random.randint(0, 2)
            if tribute3.weapon == 'cursed sword':
                temp = random.randint(0, 2)

                if temp == 0:
                    tribute3.kills += 2
                    kill(tribute1)
                    kill(tribute2)
                    return f"{t1} and {t2} spot {t3} in the distance and tries to hunt {tribute3.himher} down, but {t3} uses the mystic" \
                        f" power of {tribute3.hisher} {tribute3.weapon} and banishes both {t1} and {t2} into the void."

                elif temp == 1:
                    tribute3.kills += 2
                    tribute3.inj = True
                    kill(tribute1)
                    kill(tribute2)
                    return f"{t1} and {t2} spot {t3} in the distance and tries to hunt {tribute3.himher} down, but " \
                        f"{t3} scorches both of them to dust using the overwhelming power of {tribute3.hisher} " \
                        f"{tribute3.weapon}. However, the flames are fierce and {t3} injures {tribute3.himher}self in " \
                        f"the process."

                elif temp == 2:
                    kill(tribute1)
                    kill(tribute2)
                    kill(tribute3)
                    choice = random.choice([f"After getting ganged on by {t1} and {t2}, {t3} tries using the full "
                                            f"potential of {tribute3.hisher} {tribute3.weapon}, but the influx of "
                                            f"power is too much for {tribute3.himher} to control and all three get "
                                            f"obliterated in a proceeding explosion.",
                                            f"After getting ganged on by {t1} and {t2}, {t3} uses {tribute3.hisher}"
                                            f" {tribute3.weapon} to summon an eldritch monstrosity from the otherworld "
                                            f"to fight for {tribute3.himher}. However, the monstrosity was in the "
                                            f"middle of watching Gundam when it was summoned, and in its rage at being"
                                            f" interrupted, dismembered everyone in the vicinity."])
                    return choice
            elif tribute3.weapon == 'a fucking gun':
                kill(tribute1)
                kill(tribute2)
                if scenario == 0:
                    tribute3.weapon = None
                    return f"{t3} spots {t1} and {t2} nearby, and before they even have time to react, {t3} mows em " \
                        f"down with {tribute3.hisher} gun - though {tribute3.heshe} runs out of bullets in the process."
                else:
                    return f"{t3} spots {t1} and {t2} nearby, and before they even have time to react, {t3} mows em " \
                        f"down with {tribute3.hisher} gun."

            elif tribute3.weapon == 'explosives':
                kill(tribute1)
                kill(tribute2)
                kill(tribute3)
                return f"After getting ganged on by {t1} and {t2}, {t3} tries to defend {tribute3.himher}self using " \
                    f"{tribute3.weapon} but blows everyone up in the process."
            elif ((tribute3.weapon is not None) and (tribute2.weapon is None) and (tribute1.weapon is None)) or (tribute1.inj and tribute2.inj):
                if tribute1.inj:
                    kill(tribute1)
                    tribute2.inj = True
                    return f"{t3} covetly stalks {t1} and {t2} as they stumble around the arena, and when " \
                        f"{tribute3.heshe} feels the time is right, {t3} strikes; {tribute3.heshe} smashes {t1}'s face" \
                        f" in, but {t2} manages to escape, wounded."
                elif tribute2.inj:
                    kill(tribute2)
                    tribute1.inj = True
                    return f"{t3} covetly stalks {t1} and {t2} as they stumble around the arena, and when " \
                        f"{tribute3.heshe} feels the time is right, {t3} strikes; {tribute3.heshe} smashes {t2}'s face" \
                        f" in, but {t1} manages to escape, wounded."
                else:
                    tribute1.inj = True
                    tribute2.inj = True
                    return f"{t3} covetly stalks {t1} and {t2} as they stumble around the arena, and when" \
                        f"{tribute3.heshe} feels the time is right, {t3} stikes; both {t1} and {t2} take quite" \
                        f" the beating, but they manage to escape, wounded."
            else:
                if scenario == 0:
                    tribute1.kills += 1
                    tribute2.kills += 1
                    kill(tribute3)
                    return f"{t1} and {t2} spot {t3} from afar and hunts {tribute3.himher} down before " \
                        f"{tribute3.heshe} can escape."
                elif scenario == 1:
                    if tribute1.inj:
                        tribute2.kills += 1
                        tribute3.kills += 1
                        kill(tribute1)
                        kill(tribute3)
                        return f"{t1} and {t2} spot {t3} from afar and hunts {tribute3.himher} down, but {t3} puts up" \
                            f" quite a fight, and manages to take out a weakened {t1}."
                    else:
                        tribute1.inj = True
                        tribute1.kills += 1
                        tribute2.kills += 1
                        kill(tribute3)
                        return f"{t1} and {t2} spot {t3} from afar and hunts {tribute3.himher} down, but {t3} puts up" \
                            f" quite a fight and leaves {t1} injured."
                elif scenario == 2:
                    if tribute2.inj:
                        tribute1.kills += 1
                        tribute3.kills += 1
                        kill(tribute2)
                        kill(tribute3)
                        return f"{t1} and {t2} spot {t3} from afar and hunts {tribute3.himher} down, but {t3} puts up" \
                            f" quite a fight, and manages to take out a weakened {t2}."
                    else:
                        tribute2.inj = True
                        tribute1.kills += 1
                        tribute2.kills += 1
                        kill(tribute3)
                        return f"{t1} and {t2} spot {t3} from afar and hunts {tribute3.himher} down, but {t3} puts up" \
                            f" quite a fight and leaves {t2} injured."


        # This God *does* play dice
        else:
            scenario = random.randint(0, 19)

            if scenario == 0:
                return f"{t1} and {t2} hunt {random.choice(['boars', 'deers', 'rabbits'])} together."
            elif scenario == 1:
                return f"{t1} and {t2} hunt for other tributes."
            elif scenario == 2:
                tribute1.inj = True
                return f"{t1} falls in a ditch and {t2} laughs {tribute2.hisher} ass off while helping {t1} up."
            elif scenario == 3:
                if tribute1.inj and tribute2.inj:
                    kill(tribute1)
                    kill(tribute2)
                    return f"{t1} and {t2} both get killed by a giant bat while exploring a dark cave."
                else:
                    return f"{t1} and {t2} take down a giant bat while exploring a dark cave."
            elif scenario == 4:
                tribute1.inj = False
                tribute2.inj = False
                return f"{t1} and {t2} chance upon a magical hot springs, and a quick bath rejuvenates them both."
            elif scenario == 5:
                return f"{t1} and {t2} pool their shroom knowledge together and manage to isolate and collect the ones " \
                    f"that actually get you high; They spend the rest of the day tripping on shrooms."
            elif scenario == 6:
                return f"{t1} and {t2} splits up to look for supplies."
            elif scenario == 7:
                if tribute1.weapon is not None or tribute2.weapon is not None:
                    return f"{t1} and {t2} fend off a sudden attack by a savage bunny with a british accent."
                else:
                    injured = random.choice([tribute1, tribute2])
                    injured.inj = True
                    return f"{t1} and {t2} fend off a sudden attack by a savage bunny with a british accent, but" \
                        f" {injured.name} is wounded in the process."
            elif scenario == 8:
                return f"{t2} almost steps on a landmine before {t1} pulls {tribute2.himher} out of the way."
            elif scenario == 9:
                weapon = random.choice(weapon_list)
                if tribute1.weapon is None and tribute2.weapon is None:
                    temp = random.randint(0,5)
                    if temp == 0:
                        tribute1.weapon = weapon
                        tribute2.weapon = weapon
                        return f"{t1} and {t2} find a chest with a {weapon} inside, and bicker over who gets to keep it," \
                            f" before finding another one hidden behind the chest."
                    elif temp < 5:
                        if temp < 3:
                            tribute1.weapon = weapon
                            return f"{t1} and {t2} find a {weapon} lying around, and bicker over who gets to keep it," \
                                f"before {t2} gives in and lets {t1} hold on to it."
                        else:
                            tribute2.weapon = weapon
                            return f"{t1} and {t2} find a {weapon} lying around, and bicker over who gets to keep it," \
                                f"before {t1} gives in and lets {t2} hold on to it."
                    elif temp == 5:
                        if tribute1.inj:
                            tribute1.kills += 1
                            tribute1.weapon = weapon
                            kill(tribute2)
                            return f"{t1} and {t2} find a {weapon} lying around, and an argument over who gets to keep" \
                                f" it heats up into a fight; {t1} ends up bashing {t2}'s skull in."
                        else:
                            tribute2.kills += 1
                            tribute2.weapon = weapon
                            kill(tribute1)
                            return f"{t1} and {t2} find a {weapon} lying around, and an argument over who gets to keep" \
                                f" it heats up into a fight; {t2} ends up bashing {t1}'s skull in."
                elif tribute1.weapon is None:
                    tribute1.weapon = weapon
                    return f"{t1} and {t2} find a {weapon} while " \
                        f"{random.choice(['scavenging in a shed', 'exploring a derelict mansion', 'looting an oddly-placed chest'])}," \
                        f" and {t1} takes a liking to it."
                elif tribute2.weapon is None:
                    tribute2.weapon = weapon
                    return f"{t1} and {t2} find a {weapon} while " \
                        f"{random.choice(['scavenging in a shed', 'exploring a derelict mansion', 'looting an oddly-placed chest'])}," \
                        f" and {t2} takes a liking to it."
                else:
                    return f"{t1} and {t2} spend the day exploring " \
                        f"{random.choice(['a derelict mansion', 'a bamboo forest', 'a dark cave'])} but finds nothing of interest."
            elif scenario == 10:
                if len(dead) > 0:
                    temp = random.choice(dead)
                    return f"{t1} and {t2} find {temp.name}'s corpse while exploring."
                else:
                    return f"{t1} tries to catch a rabbit by chasing it while {t2} lays a trap for it; neither are" \
                        f"successful in their endeavours."
            elif scenario == 11:
                if tribute1.supplies is None:
                    tribute1.supplies = 'medkit'
                if tribute2.supplies is None:
                    tribute2.supplies = 'medkit'
                tribute1.inj = False
                tribute2.inj = False
                return f"{t1} and {t2} chance upon a warehouse of medical supplies."
            elif scenario == 12:
                return f"{t1} and {t2} can't find a decent source of water before they remember that one Bear Grylls meme," \
                    f" and they decide that watersports isn't all that degenerate of a kink anyway."
            elif scenario == 13:
                return f"{t1} and {t2} find a river and decide to do some fishing; {t1} stumbles around without catching anything" \
                    f" at all while {t2} catches buttloads with {tribute2.hisher} secret fishing technique passed down the" \
                    f" generations."
            elif scenario == 14:
                return f"{t1} and {t2} find a mysterious book simply labeled 'Breaking Bad Coworker's Journal'. {t1} goes to" \
                    f" read it but {t2} senses something very wrong and stops {t1} before {tribute1.heshe} opens it."
            elif scenario == 15:
                return f"{t1} throws a rock at {t2}'s head when {tribute2.heshe} reveals that {tribute2.heshe} gave " \
                    f"{random.choice(['Darling in the Franxx', 'Eromanga Sensei', 'Sword Art Online', 'Shobitch', 'Sakurasou'])} a 10" \
                    f" on MAL."
            elif scenario == 16:
                tribute1.inj = True
                tribute2.inj = True
                return f"{t2} stands in the rain for 0.2 nanoseconds and catches a bad cold; {tribute2.heshe} spreads " \
                    f"it to {t1} too."
            elif scenario == 17:
                if tribute1.weapon is not None or tribute2.weapon is not None:
                    tribute1.inj = True
                    tribute2.inj = True
                    return f"{t1} and {t2} accidentally awaken a sleeping bear in a cave, but they manage to fight it off."
                elif tribute1.inj or tribute2.inj:
                    kill(tribute1)
                    kill(tribute2)
                    return f"{t1} and {t2} accidentally awaken a sleeping bear in a cave, and they both get mauled."
                else:
                    return f"{t1} and {t2} accidentally awaken a sleeping bear in a cave, but they both manage to escape."
            elif scenario == 18:
                if tribute1.inj:
                    kill(tribute1)
                    return f"{t1} accidentally steps on a snake and gets bitten. Despite {t2}'s best efforts, " \
                        f"{tribute1.heshe} dies of venom a few hours later."
                else:
                    tribute1.inj = True
                    return f"{t1} accidentally steps on a snake and gets bitten. {t2} helps {tribute1.himher} through" \
                        f" the ordeal and {t1} manages to mostly wear the venom off."
            elif scenario == 19:
                choice = random.choice(['an enraged bull', 'a territorial rhino', 'a pack of wolves'])
                if tribute2.inj:
                    kill(tribute2)
                    return f"{t1} and {t2} accidentally end up walking right in front of {choice}, and while " \
                        f"{t1} manages to escape unscathed, {t2} isn't quite as lucky."
                else:
                    return f"{t1} and {t2} accidentally end up walking right in front of {choice}, and while they " \
                        f"both manage to escape in one piece, {t2}'s " \
                        f"{random.choice(['right', 'left'])} {random.choice(['leg', 'arm'])} ain't lookin' that hot."

    elif num == 0:  # tribute encounter

        aggro_multiplier = 1
        # checks if either tribute has weapons
        if (tribute1.weapon is None) is not (tribute2.weapon is None):
            if tribute1.inj != tribute2.inj:
                aggro_multiplier =  2
            else:
                aggro_multiplier = 1.5

        scenario = int(random.randint(0, 10) * aggro_multiplier)
        #0-3 neutral scenarios, 3-5 teaming up scenarios
        if scenario == 0:
            return f"{t1} sees {t2} in the distance, but ignores {tribute2.himher} for now."
        elif scenario == 1:
            return f"{t1} and {t2} both spot each other, but both of them slowly back off and run into the distance."
        elif scenario == 2:
            return f"{t1} covertly stalks {t2} through the bushes."
        elif scenario == 3:
            tribute1.partner = tribute2
            tribute2.partner = tribute1
            tribute2.done = True
            return f"{t1} and {t2} decide to stick together for the day and go hunting for supplies."
        elif scenario == 4:
            temp = random.randint(0, 9)
            if temp == 9:
                tribute2.done = True
                return f"{t1} and {t2} have hot, steamy, sweaty sex, then go about their separate ways."
            else:
                tribute1.partner = tribute2
                tribute2.partner = tribute1
                tribute2.done = True
                return f"{t1} and {t2} decide to team up and hunt other tributes."
        elif scenario == 5:
            tribute1.partner = tribute2
            tribute2.partner = tribute1
            tribute2.done = True
            return f"{t1} and {t2} remember an anime-watching contract that they forged long ago, and in its honour, decide to team up."
        # 6+ violent scenarios
        elif scenario > 5:
            tribute2.done = True
            # figure out who's stronger
            even = False
            if tribute1.weapon is not None and tribute2.weapon is None:
                if not tribute1.inj or tribute2.inj:
                    strong = tribute1
                    weak = tribute2
                else:
                    strong = tribute1
                    weak = tribute2
                    even = True
            elif tribute2.weapon is not None and tribute1.weapon is None:
                if not tribute2.inj or tribute1.inj:
                    strong = tribute2
                    weak = tribute1
                else:
                    strong = tribute1
                    weak = tribute2
                    even = True
            elif tribute1.inj and not tribute2.inj:
                strong = tribute2
                weak = tribute1
            elif tribute2.inj and not tribute1.inj:
                strong = tribute1
                weak = tribute2
            else:
                strong = tribute1
                weak = tribute2
                even = True

            str = strong.name
            wk = weak.name

            if strong.weapon == 'cursed sword' or weak.weapon == 'cursed sword':
                temp = random.randint(0,2)
                if temp == 0:
                    if weak.weapon == 'cursed sword':
                        weak.kills += 1
                        kill(strong)
                        return f"{wk} uses the ancient power of {weak.hisher} {weak.weapon} to banish {str} into oblivion."
                    if strong.weapon == 'cursed sword':
                        strong.kills += 1
                        kill(weak)
                        return f"{str} uses the ancient power of {strong.hisher} {strong.weapon} to banish {wk} into oblivion."
                elif temp == 1:
                    if weak.weapon == 'cursed sword':
                        weak.inj = True
                        weak.kills += 1
                        kill(strong)
                        return f"{wk} scorches {str} to dust using the overwhelming power of {weak.hisher} " \
                            f"{weak.weapon}, but injures {weak.himher}self in the process."
                    if strong.weapon == 'cursed sword':
                        strong.inj = True
                        strong.kills += 1
                        kill(weak)
                        return f"{str} scorches {wk} to dust using the overwhelming power of {strong.hisher} " \
                            f"{strong.weapon}, but injures {strong.himher}self in the process."
                elif temp == 2:
                    kill(weak)
                    kill(strong)
                    if weak.weapon == 'cursed sword':
                        return f"{wk} tries using the full potential of {weak.hisher} {weak.weapon} against {str}, but" \
                            f" the influx of power is too much for {wk} to control and both of them get obliterated " \
                            f"in a proceeding explosion."
                    elif strong.weapon == 'cursed sword':
                        return f"{str} uses {strong.hisher} {strong.weapon} to summon an eldritch monstrosity from the " \
                            f"otherworld to fight for {strong.himher}, but the monstrosity was in the middle of watching " \
                            f"Gundam when it was summoned, and in its rage at being interrupted, dismembered both {str} and {wk}."

            elif strong.weapon == 'a fucking gun' or weak.weapon == 'a fucking gun':
                temp = random.randint(0, 2)
                if strong.weapon == 'a fucking gun':
                    strong.kills += 1
                    kill(weak)
                    if temp == 2:
                        strong.weapon = None
                        return f"{str} just straights up shoots {wk} in the head with {strong.hisher} gun, but runs " \
                            f"out of bullets in the process."
                    else:
                        return f"{str} just straights up shoots {wk} in the head with {strong.weapon}."
                elif weak.weapon == 'a fucking gun':
                    weak.kills += 1
                    kill(strong)
                    if temp == 2:
                        weak.weapon = None
                        return f"{wk} just straights up shoots {str} in the head with {weak.hisher} gun, but runs " \
                            f"out of bullets in the process."
                    else:
                        return f"{wk} just straights up shoots {str} in the head with {weak.weapon}."

            elif strong.weapon == 'explosives' or weak.weapon == 'explosives':
                kill(weak)
                kill(strong)
                if weak.weapon == 'explosives':
                    return f"{wk} tries to defend {weak.himher}self against {str} using {weak.weapon} but blows both of them up in " \
                        f"the process."
                elif strong.weapon == 'explosives':
                    return f"{str} tries to defend {strong.himher}self against {wk} using {strong.weapon} but blows both of them up in " \
                        f"the process."

            elif strong.weapon in cleavers:
                if even:
                    weak.inj = True
                    return f"{str} tries to cleave {wk} in two but {wk} manages to escape with {weak.hisher} life, albeit injured."
                else:
                    strong.kills += 1
                    kill(weak)
                    if scenario > 7:
                        return f"{str} savagely decapitates {wk} with {strong.hisher} {strong.weapon}."
                    else:
                        return f"{str} cuts {wk} down with {strong.hisher} {strong.weapon} in a single stroke."

            elif strong.weapon in stabbers:
                if even:
                    weak.inj = True
                    return f"{str} stabs {wk} in the gut with a {strong.weapon}, but {wk} manages to push {strong.himher} off and run away."
                else:
                    strong.kills += 1
                    kill(weak)
                    if scenario > 7:
                        return f"A well aimed stab by {str}'s {strong.weapon} ends {wk}'s miserable life."
                    else:
                        return f"After a drawn-out fight, {str} manages to catch {wk} in the throat with {strong.hisher}" \
                            f" {strong.weapon} and scores a kill."

            elif strong.weapon in clubbers:
                if even:
                    weak.inj = True
                    return f"{str} tries to club {wk} with {strong.hisher} {strong.weapon}, but {wk} blocks and dodges," \
                        f" before making a run for it the first chance {weak.heshe} gets."
                else:
                    strong.kills += 1
                    kill(weak)
                    if scenario > 7:
                        return f"{str} brutally smashes {wk}'s head in with {strong.hisher} {strong.weapon}"
                    else:
                        return f"A single swing of {str}'s {strong.weapon} is enough to take out {wk}."

            elif strong.weapon == 'bow' or strong.weapon == 'blowdart':
                if strong.weapon == 'bow':
                    weak.inj = True
                    return f"{str} stealthily shoots arrows from the cover of foliage at {wk}, but {wk} manages to " \
                        f"escape with {weak.hisher} life, albeit wounded."
                if strong.weapon == 'blowdart':
                    weak.inj = True
                    return f"{str} stealthily shoots poisoned darts from the cover of foliage at {wk}, but {wk} manages to " \
                        f"escape with {weak.hisher} life, albeit with poison flowing through {weak.hisher} veins."

            else:
                if strong.inj and weak.inj:
                    kill(weak)
                    kill(strong)
                    return  f"In a magnificent display of manliness, an injured {str} and {wk} fight it out to the " \
                        f"death, and simultaneously collapse."
                elif even:
                    strong.inj = True
                    weak.inj = True
                    return f"{str} and {wk} brawl it out, but they seem evenly matched, and they both decide to flee" \
                        f" when the chance comes."
                else:
                    strong.inj = True
                    strong.kills += 1
                    kill(weak)
                    if scenario > 7:
                        return f"{str} dismembers a weakened {wk} using {strong.hisher} bare hands, though not before getting" \
                            f" injured {strong.himher}self."
                    else:
                        return f"{str} remembers the words of {strong.hisher} old boxing coach, and on the brink of death, while the anime OP plays in" \
                            f" the background, KO's {wk} in one final punch."

    elif num == 1: # supply/weapon encounter
        scenario = random.randint(0, 10)
        if scenario == 0:
            if tribute1.inj:
                tribute1.inj = False
                return f"{t1} finds a pile of fluffy BL manga lying around, and while reading it magically recovers from {tribute1.hisher} " \
                    f"wounds due to the sheer purity of gay."
            else:
                tribute1.supplies = 'medkit'
                return f"{t1} finds a medkit lying around."
        elif scenario == 1:
            if tribute1.inj:
                tribute1.inj = False
                return f"{t1} finds a pile of fluffy yuri manga lying around, and while reading it magically recovers from {tribute1.hisher} " \
                    f"wounds due to the sheer purity of gay."
            else:
                tribute1.supplies = 'herbs'
                return f"{t1} chances upon some medicinal herbs and decides to collect some for later use."
        elif scenario == 2:
            if tribute1.inj:
                tribute1.inj = False
                return  f"{t1} finds a medkit lying around and uses it to patch {tribute1.himher}self up."
            else:
                tribute1.supplies = 'medkit'
                return f"{t1} finds a medkit lying around."
        elif scenario == 3:
            if tribute1.inj:
                tribute1.inj = False
                return  f"{t1} recieves a supply drop containing medicine from an unknown sponsor, and uses it to treat {tribute1.hisher} wounds."
            else:
                tribute1.supplies = 'medkit'
                return f"{t1} recieves a supply drop containing medicine from an unknown sponsor."
        elif scenario == 4:
            if tribute1.inj:
                tribute1.inj = False
                return f"{t1} finds a picture of {random.choice(['Yuki from Tsuritama', 'Shouko Nishimiya', 'Shouya Ishida', 'Nadeshiko from Yuru Camp', 'Naru from Barakamon', 'Prince from Kazetsuyo', 'Ushio from Clannad', 'Connor'])} smiling and all {tribute1.hisher} injuries are healed instantly."
            else:
                return f"{t1} finds a picture of {random.choice(['Yuki from Tsuritama', 'Shouko Nishimiya', 'Shouya Ishida', 'Nadeshiko from Yuru Camp', 'Naru from Barakamon', 'Prince from Kazetsuyo', 'Ushio from Clannad', 'Connor'])} smiling and all {tribute1.hisher} worries immediately dissipate."
        elif scenario == 5:
            temp = random.randint(0, 4)
            if temp == 4:
                tribute1.supplies = 'weird amulet'
                return f"While exploring a hidden grove, {t1} encounters multiple stone monuments arranged in a " \
                    f"circle, with an amulet on a podium in the center. {t1}, never having played a videogame or " \
                    f"watched a movie in {tribute1.hisher} life, grabs the amulet without a second thought."
            else:
                if tribute1.inj:
                    tribute1.inj = False
                    return f"{t1} chances upon some medicinal herbs and applies it on {tribute1.hisher} wounds."
                else:
                    tribute1.supplies = 'herbs'
                    return f"{t1} chances upon some medicinal herbs and decides to collect some for later use."
        elif scenario < 8 and tribute1.weapon is None:
            new_weapon = random.choice(weapon_list)
            tribute1.weapon = new_weapon
            return f"{t1} finds a {new_weapon} while scavenging through {random.choice(['a shed', 'a warehouse', 'some bushes'])}."
        elif scenario < 10 and tribute1.weapon is None:
            new_weapon = random.choice(weapon_list)
            tribute1.weapon = new_weapon
            return f"{t1} receives a supply drop containing a {new_weapon} from an unknown sponsor."
        elif scenario == 10:
            new_weapon = random.choice(rare_weapons_list)
            tribute1.weapon = new_weapon
            if new_weapon == 'cursed sword':
                return f"After a lengthy set of obstacles and puzzles in an ancient stone temple, {t1} finally reaps" \
                    f" the reward for {tribute1.hisher} effort; a {new_weapon}, embedded with unimaginable power."
            elif new_weapon == 'a fucking gun':
                return  f"Breaking through a hidden safe with {tribute1.hisher} 1337 technical skills " \
                    f"({tribute1.heshe} used a hammer), {t1} finds {new_weapon} stored compactly inside."
        else:
            return f"{t1} tests out {tribute1.hisher} {tribute1.weapon} against " \
                f"{random.choice(['some wild boars', 'a scarecrow', 'an odd-looking boulder', 'an effigy of Donald Trump'])}."

    elif num >= 2: # environment encounter
        scenario = random.randint(0,23)

        if scenario == 0:
            return f"{t1} picks some flowers."
        elif scenario == 1:
            return f"{t1} thinks about home."
        elif scenario == 2:
            tribute1.inj = True
            return f"{t1} tries to eat something inedible and regrets it."
        elif scenario == 3:
            tribute1.inj = True
            return f"{t1} tries some wild mushrooms hoping to get high, but all {tribute1.heshe} gets is a bad case of diarrhea."
        elif scenario == 4:
            return f"{t1} tries some wild mushrooms and lucks out; {tribute1.heshe} spends the rest of the day " \
                f"tripping on shrooms."
        elif scenario == 5:
            return f"{t1} starts talking to {tribute1.himher}self."
        elif scenario == 6:
            return f"{t1} steps in something indescribable."
        elif scenario == 7:
            temp = random.randint(0, 10)
            if temp == 10:
                kill(tribute1)
                return f"{t1} dies of dysentery after drinking unboiled river water. This is wilderness survival 101" \
                    f" folks, jeez."
            else:
                return f"{t1} finds a river and decides to stick close to it."
        elif scenario == 8:
            temp = random.randint(0, 10)
            if temp != 6:
                tribute1.inj = True
                return f"{t1} gets bit by a savage bunny with a british accent."
            else:
                kill(tribute1)
                return f"{t1} gets murdered by a savage bunny with a british accent."
        elif scenario == 9:
            kill(tribute1)
            return f"{t1} steps on a landmine and gets yeeted into the stratosphere."
        elif scenario == 10:
            kill(tribute1)
            return f"{t1} chances upon a small book simply titled 'Breaking Bad Coworker's Journal'. After reading a" \
                f" couple pages, {tribute1.heshe} promptly decides to jump off a cliff and commit suicide."
        elif scenario == 11:
            tribute1.inj = True
            return f"{t1}'s dumb ass falls into a hole and breaks {tribute1.hisher} leg."
        elif scenario == 12:
            return f"{t1} carves {tribute1.hisher} initials into a tree."
        elif scenario == 13:
            return f"{t1} ponders the human condition."
        elif scenario == 14:
            if len(dead) > 0:
                temp = random.choice(dead)
                return f"{t1} finds {temp.name}'s corpse."
            else:
                return f"{t1} dreams about the time {tribute1.heshe} wasn't stuck in some idiotic simulation of *hunger games*," \
                    f" and a bad one to boot."
        elif scenario == 15:
            return f"{t1} manages to hunt down a " \
                f"{random.choice(['squirrel', 'boar', 'rabbit', 'green amorphous blob-looking thing'])} and eats it."
        elif scenario == 16:
            return f"{t1} looks desperately around for something to eat, to no avail."
        elif scenario == 17:
            return f"{t1} does some exploring."
        elif scenario == 18:
            return f"{t1} finds a stash of Harada doujins, and upon reading one is promptly traumatized for life."
        elif scenario == 19:
            return f"{t1} finds a blu-ray collection of {random.choice(['Haikyuu!', 'K-ON!', 'Fullmetal Alchemist'])} and" \
                f" has no choice but to spend the entire day rewatching that shit."
        elif scenario == 20:
            return f"{t1} thinks about all the fun {tribute1.hesshes} had with {tribute1.hisher} frie- oh wait, {t1}" \
                f" doesn't have any. Whoops."
        elif scenario == 21:
            return f"{t1} can't find a decent source of water, and nearly gives in before remembering that one" \
                f" Bear Grylls meme, and decides to drink {tribute1.hisher} own piss. Fresh and hot."
        elif scenario == 22:
            if tribute1.inj:
                kill(tribute1)
                return f"{t1} is bit by a snake and dies, because no one ever told {tribute1.himher} how to tie" \
                    f" a tourniquet."
            else:
                tribute1.inj = True
                return f"{t1} is bit by a snake, but manages to wear off the poison."
        elif scenario == 23:
            if tribute1.inj and tribute1.weapon is None:
                kill(tribute1)
                return f"{t1} accidentally awakens a sleeping bear in a cave, and gets mauled."
            else:
                return f"{t1} accidentally awakens a sleeping bear in a cave, but {tribute1.heshe} " \
                    f"{random.choice([f'channels {tribute1.hisher} inner Takamura and KOs the beast in one strike.', 'talks it down and has a nice little tea party.', 'asserts dominance by pissing on it.'])}"


def pick_random_night_action(tribute1, tribute2):
    global tributes, dead, deadthisday
    # make their names easier to access.
    t1 = tribute1.name
    t2 = "Placeholder. If you're seeing this, premed has fucked up somewhere, that fucking idiot."

    # num picks between three overarching scenarios
    if tribute2 == None:
        scenario = random.randint(2, 25)  # skip tribute encounter scenarios
    else:
        t2 = tribute2.name
        if tribute1.partner == tribute2:
            scenario = -1  # special scenario set for partners
        else:
            scenario = random.randint(0, 25)

    # If the tribute has supplies, it overrides all other scenarios
    if tribute1.inj:  # check if tribute is injured
        injured = tribute1
    else:
        injured = None

    if tribute1.supplies is not None:  # check if tribute has supplies.
        supplier = tribute1
    else:
        supplier = None

    if tribute1.partner is not None:  # redo if tribute has a partner

        if tribute2.inj:  # check if tribute is injured
            injured = tribute2

        if tribute2.supplies is not None:  # check if tribute has supplies.
            supplier = tribute2

    if tribute1.supplies == 'weird amulet':  # weird amulet has custom outcomes
        temp = random.randint(0, 2)
        if temp == 0:
            tribute1.supplies = None
            if tribute1.partner is None:
                return f"{t1} fiddles around with {tribute1.hisher} weird amulet, but nothing happens at all."
            else:
                return f"{t1} and {t2} fiddle around with the weird amulet, but nothing happens at all."
        elif temp == 1:
            tribute1.supplies = None
            tribute1.weapon = 'cursed sword'
            if tribute1.partner is None:
                return f"{t1} fiddles around with {tribute1.hisher} weird amulet, and in a sudden puff of purple smoke, " \
                    f"it transforms into a cursed sword."
            else:
                return f"{t1} and {t2} fiddle around with the weird amulet, and in a sudden puff of purple smoke, " \
                    f"it transforms into a cursed sword."
        elif temp == 2:
            tribute1.supplies = None
            kill(tribute1)
            if tribute1.partner is None:
                return f"{t1} tries to get some sleep, when in a sudden puff of smoke, {tribute1.hisher} weird amulet" \
                    f" randomly summons a winged monstrosity that dismembers {t1} before flying off into the night sky."
            else:
                return f"{t1} and {t2} try to get some sleep, when in a sudden puff of smoke, the weird amulet" \
                    f" randomly summons a winged monstrosity that dismembers them both before flying off into the night sky."

    elif injured is not None and supplier is not None:
        if supplier.supplies == 'medkit':
            injured.inj = False
            supplier.supplies = None
            if injured.partner is None:
                return f"{t1} patches up {tribute1.hisher} injuries using a medkit {tribute1.heshe} had grabbed along the" \
                f"way."
            else:
                if supplier != injured:
                    return f"{supplier.name} tends to {injured.name}'s injuries using a medkit."
                else:
                    if tribute1 == injured:
                        return f"{t2} tends to {injured.name}'s injuries using a medkit."
                    else:
                        return f"{t1} tends to {injured.name}'s injuries using a medkit."
        elif supplier.supplies == 'herbs':
            injured.inj = False
            supplier.supplies = None
            if injured.partner is None:
                return f"{t1} patches up {tribute1.hisher} injuries using the medicinal herbs {tribute1.heshe} had " \
                f"collected along the way."
            else:
                if supplier != injured:
                    return f"{supplier.name} tends to {injured.name}'s injuries using a some herbs {supplier.heshe} had " \
                        f"grabbed along the way."
                else:
                    if tribute1 == injured:
                        return f"{t2} tends to {injured.name}'s injuries using a some herbs {tribute2.heshe} had " \
                        f"grabbed along the way."
                    else:
                        return f"{t1} tends to {injured.name}'s injuries using a some herbs {tribute1.heshe} had " \
                        f"grabbed along the way."

    tribute1.asleep = False

    #isolate scenarios where tributes have partner
    if scenario == -1:
        # REROLL!
        scenario = random.randint(0, 10)
        if scenario == 0:
            tribute1.asleep = True
            tribute2.asleep = True
            return f"{t1} and {t2} tell old tales and bond over a campfire."
        elif scenario == 1:
            return f"{t1} and {t2} sleep in shifts throughout the night."
        elif scenario == 2:
            tribute1.asleep = True
            tribute2.asleep = True
            return f"{t1} and {t2} huddle up for warmth."
        elif scenario == 3:
            tribute1.asleep = True
            tribute2.asleep = True
            return f"{t1} discreetly and implicitly confesses {tribute1.hisher} love to {t2}, but {t2} is " \
                f"{random.choice(['denser than a black hole', 'as dense as a harem mc'])}, and never realizes it."
        elif scenario == 4:
            tribute1.asleep = True
            tribute2.asleep = True
            return f"{t1} and {t2} fall asleep admiring the beauty of the star-lit sky."
        elif scenario == 5:
            return f"{t1} and {t2} set up a campfire and cheerfully sing anime OPs all night."
        elif scenario == 6:
            tribute2.asleep = True
            tribute1.asleep = True
            return f"{t1} convinces {t2} to snuggle with {tribute1.himher}."
        elif scenario == 7:
            tribute2.asleep = True
            tribute1.asleep = True
            return f"{t1} and {t2} reveal their deepest fears and insecurities to each other, and they cry themselves" \
                f" to sleep while snuggling."
        elif scenario == 8:
            if tribute1.gender.lower() == "m" and tribute2.gender.lower() == "m":
                return f"{t1} fucks {t2} in the ass all night but their balls don't touch so they both maintain" \
                    f" their heterosexuality."
            else:
                choice = random.choice(['past trauma', f'{tribute2.hisher} latent asexuality',
                                        f"{t1}'s fugly-ass face"])
                return f"{t1} tries to make a move on {t2}, but {tribute2.heshe} respectfully declines, citing" \
                    f" {choice}"
        elif scenario == 9:
            tribute1.kills += 1
            kill(tribute2)
            return f"{t1} reveals {tribute1.hisher} true colors and murders {t2} in {tribute2.hisher} sleep."
        elif scenario == 10:
            temp = random.randint(0, 4)
            if temp == 4:
                return f"As {t1} and {t2} silently stare at the flickering campfire, {t2} pipes up:\n'Hey.'\n'Yeah?'" \
                    f"\n'You ever wonder why we're here?'\n'It’s one of life’s great mysteries isn't it? Why are we here?" \
                    f" I mean, are we the product of some cosmic coincidence, or is there really a God watching" \
                    f" everything? You know, with a plan for us and stuff. I don’t know, man, but it keeps me up at night'\n" \
                    f"'...What?! I mean why are we out here, in this arena?'\n'Oh. Uh... yeah'\n'What was all that stuff " \
                    f"about God?'\n'Uh...hm? Nothing.'\n'You wanna talk about it?'\n'No'\n'You sure?'\n'Yeah.'"
            else:
                return f"{t1} and {t2} contemplate the meaning of life over a campfire."
        elif scenario == 11:
            tribute1.inj = True
            tribute2.inj = True
            return f"{t1} and {t2} are attacked by a swarm of bats."
        elif scenario == 12:
            return f"{t1} leaves cooking dinner up to {t2} and ends up having to gulp down " \
                f"**[CENSORED DUE TO GRAPHIC HORROR]**."
    # isolates scenarios where tributes encounter each other
    elif scenario == 0 or scenario == 1:
        if scenario == 0:
            tribute2.done = True
            if tribute2.asleep:
                kill(tribute2)
                tribute1.kills += 1
                return f"{t1} covetly sneaks up on and kills {t2} in {tribute1.hisher} sleep."
            else:
                if tribute2.weapon is not None:
                    tribute1.inj = True
                    return f"{t2} spots {t1} spying on {tribute2.himher}, and chases {t1} off with {tribute2.hisher} " \
                        f"{tribute2.weapon}"
                else:
                    return f"{t1} and {t2} run into eachother, and decide to truce for the night."

        if scenario == 1:
            if not tribute2.asleep:
                return f"{t1} spots {t2}, and slowly backs away."
            else:
                return f"{t1} sees a fire, but decides to stay hidden for now."
    else:
        if scenario == 2:
            tribute1.asleep = True
            return f"{t1} cries {tribute1.himher}self to sleep."
        elif scenario == 3:
            tribute1.inj = True
            return f"{t1} walks around in circles, unable to sleep."
        elif scenario == 4:
            tribute1.asleep = True
            return f"{t1} uses {tribute1.hisher} survival skills that {tribute1.heshe} learned from watching Bear Grylls " \
                f"24/7 and makes a shelter out of sticks and leaves to sleep in."

        elif scenario == 5:
            tribute1.asleep = True
            return f"{t1} falls asleep on a makeshift bed of leaves."
        elif scenario == 6:
            temp = random.randint(0, 1)
            if tribute1.inj:
                kill(tribute1)
                return f"While looking for shelter, {t1} trips and falls onto some sharp rocks and bleeds out."
            else:
                if temp == 1:
                    tribute1.inj = True
                    return f"{t1} trips on some sharp rocks and gets knocked unconscious."
                else:
                    tribute1.asleep = True
                    return f"{t1} trips on some rocks, and then decides to sleep there."
        elif scenario == 7:
            temp = random.randint(0, 15)
            if temp == 1:
                kill(tribute1)
                return f"{t1} sees a bleak future even with victory, and kills {tribute1.himher}self."
            else:
                tribute1.asleep = True
                return f"{t1} falls asleep in a flower patch."
        elif scenario == 8:
            tribute1.asleep = True
            return f"{t1} falls asleep pondering the human condition."
        elif scenario == 9:
            tribute1.asleep = False
            return f"{t1} stays awake all night as {tribute1.hisher} brain tortures {tribute1.himher} with memories of " \
                f"that one awkward moment {tribute1.heshe} had 3 years ago."
        elif scenario == 10:
            return f"{t1} practices {tribute1.hisher} " \
                f"{random.choice(['shadowboxing all night due to recently having watched Hajime no Ippo', 'spiking all night due to recently having watched Haikyuu'])}."

        elif scenario == 11:
            if tribute1.inj:
                kill(tribute1)
                return f"{t1} gets bit by a bat and dies."
            else:
                tribute1.inj = True
                return f"{t1} gets bit by a bat."
        elif scenario == 12:
            return f"{t1} makes a campfire and reminisces about the good ol' days."
        elif scenario == 13:
            return f"{t1} spots a bear sitting on a tree. It looks at {tribute1.himher}, {tribute1.heshe} looks at it," \
                f" and then {t1} skedaddles on out of there."
        elif scenario == 14:
            tribute1.asleep = True
            return f"{t1} falls asleep in a ditch."
        elif scenario == 15:
            return f"{t1} sleeps with one eye open."
        elif scenario == 16:
            tribute1.asleep = True
            return f"{t1} has nightmares about that one NTR ugly bastard doujin {tribute1.heshe} read long ago."
        elif scenario == 17:
            tribute1.asleep = True
            return f"{t1} falls asleep admiring the beauty of the star-lit sky."
        elif scenario == 18:
            tribute1.asleep = True
            return f"{t1} dreams about {tribute1.himher}self as the victor."
        elif scenario == 19:
            if tribute1.weapon is not None:
                return f"{t1} admires {tribute1.hisher} {tribute1.weapon} under the light of {tribute1.hisher} campfire."
            else:
                weapon = random.choice(['axe', 'dagger', 'cleaver'])
                tribute1.weapon = weapon
                return f"{t1} remembers that one Primitive Technology video {tribute1.heshe} saw and fastens a makeshift " \
                    f"{weapon} from a stick and a sharpened rock."
        elif scenario == 20:
            return f"{t1} prays to God, and asks Him to let {tribute1.himher} survive for another day. God tells " \
                f"{t1} to shut the FUCK UP I'M TRYIN TO WATCH SOME GUNDAM HERE"
        elif scenario == 21:
            if tribute1.gender.lower() == "m":
                return f"{t1} jacks off in a nearby bush to relieve steam and accidentally summons a demon when he moves " \
                    f"his penis in a special pattern."
            else:
                return f"{t1} draws a face on a coconut and talks to it all night."
        elif scenario == 22:
            tribute1.inj = True
            tribute1.asleep = True
            return f"{t1} eats some wild berries for dinner and regrets it."
        elif scenario == 23:
            return f"{t1} questions {tribute1.hisher} sanity."
        elif scenario == 24:
            return f"{t1} tries to cook some fish and sets the forest on fire."
        elif scenario == 25:
            tribute1.inj = True
            return f"{t1} tries to cook some meat but sets {tribute1.himher}self on fire instead."


def feast_fight(tribute1, tribute2):
    t1 = tribute1.name
    t2 = tribute2.name
    temp = random.randint(0, 9)
    if tribute1.weapon == 'explosives' or tribute2.weapon == 'explosives':
        kill(tribute1)
        kill(tribute2)
        if tribute1.weapon == 'explosives':
            return f"{t1} tries to defend {tribute1.himher}self against {t2} using {tribute1.weapon} " \
                f"but blows both of them up in the process."
        elif tribute2.weapon == 'explosives':
            return f"{t2} tries to defend {tribute2.himher}self against {t2} using {tribute2.weapon} " \
                f"but blows both of them up in the process."

    elif tribute1.weapon in cleavers:
        if temp == 0:
            tribute2.inj = True
            return f"{t1} tries to cleave {t2} in two but {t2} manages to escape with {tribute2.hisher} life, albeit" \
                f" injured."
        else:
            tribute1.kills += 1
            kill(tribute2)
            if temp > 4:
                return f"{t1} savagely decapitates {t2} with {tribute1.hisher} {tribute1.weapon}."
            else:
                return f"{t1} cuts {t2} down with {tribute1.hisher} {tribute1.weapon} in a single stroke."

    elif tribute1.weapon in stabbers:
        if temp == 0:
            tribute2.inj = True
            return f"{t1} stabs {t2} in the gut with a {tribute1.weapon}, but {t2} manages to push " \
                f"{tribute1.himher} off and run away."
        else:
            tribute1.kills += 1
            kill(tribute2)
            if temp > 4:
                return f"A well aimed stab by {t1}'s {tribute1.weapon} ends {t2}'s miserable life."
            else:
                return f"After a drawn-out fight, {t1} manages to catch {t2} in the throat with {tribute1.hisher}" \
                    f" {tribute1.weapon} and scores a kill."

    elif tribute1.weapon in clubbers:
        if temp == 0:
            tribute2.inj = True
            return f"{t1} tries to club {t2} with {tribute1.hisher} {tribute1.weapon}, but {t2} blocks and dodges," \
                f" before making a run for it the first chance {tribute2.heshe} gets."
        else:
            tribute1.kills += 1
            kill(tribute2)
            if temp > 4:
                return f"{t1} brutally smashes {t2}'s head in with {tribute1.hisher} {tribute1.weapon}"
            else:
                return f"A single swing of {t1}'s {tribute1.weapon} is enough to take out {t2}."

    elif tribute1.weapon == 'bow' or tribute1.weapon == 'blowdart':
        if tribute1.weapon == 'bow':
            tribute1.kills += 1
            kill(tribute2)
            return f"A single well-aimed arrow fired from {t1}'s bow is enough to end {t2}'s life."
        if tribute1.weapon == 'blowdart':
            tribute1.kills += 1
            kill(tribute1)
            return f"{t1} uses a dart coated with a rare vicious poison to take {t2} out."


def pick_random_feast_action(tribute1, tribute2):
    global tributes, dead, deadthisday, events
    t1 = tribute1.name
    t2 = "Placeholder. If you're seeing this, premed has fucked up somewhere, that fucking idiot."

    if tribute2 is None:
        num = 0 # skip tribute encounter scenarios
    else:
        t2 = tribute2.name
        if tribute1.weapon is not None and tribute1.supplies is not None:
            num = 1
        else:
            num = random.randint(0, 1)

        if tribute1.partner == tribute2:
            num = -1

    # Makes it so that all injured tributes will not participate
    if tribute1.partner is not None:
        if tribute1.inj or tribute2.inj:
            return f"{t1} and {tribute2.name} decide not to go to the feast."
    else:
        if tribute1.inj:
            return f"{t1} decides not to go to the feast."


    # special scenarios for tributes with guns and cursed swords
    if tribute1.weapon == 'cursed sword' and num != -1:
        if tribute1.supplies is None:
            tribute1.supplies = 'medkit'
        return f"{t1} uses the power of {tribute1.hisher} {tribute1.weapon} to open portals and grab supplies from" \
            f" miles away."
    elif tribute2 is not None:
        if (tribute1.weapon == 'cursed sword' or tribute2.weapon == 'cursed sword') and num == -1:
            if tribute1.supplies is None:
                tribute1.supplies = 'medkit'
            if tribute2.supplies is None:
                tribute2.supplies = 'medkit'

            if tribute1.weapon == 'cursed sword':
                return f"{t1} and {t2} use the power of {t1}'s {tribute1.weapon} to open portals and grab supplies from" \
                    f" miles away."
            elif tribute2.weapon == 'cursed sword':
                return f"{t1} and {t2} use the power of {t2}'s {tribute2.weapon} to open portals and grab supplies from" \
                    f" miles away."

    if tribute1.weapon == 'a fucking gun' and num != -1:
        if tribute1.supplies is None:
            tribute1.supplies = 'medkit'
        return f"A single gunshot freezes all the tributes in place as {t1} casually strolls in waving" \
            f" {tribute1.hisher} gun around, picks up some supplies, and walks away."
    elif tribute2 is not None:
        if (tribute1.weapon == 'a fucking gun' or tribute2.weapon == 'a fucking gun') and num == -1:
            if tribute1.supplies is None:
                tribute1.supplies = 'medkit'
            if tribute2.supplies is None:
                tribute2.supplies = 'medkit'

            if tribute1.weapon == 'a fucking gun':
                return f"A single gunshot freezes all the tributes in place as {t1} casually strolls in waving" \
                    f" {tribute1.hisher} gun around with {t2} behind {tribute1.himher}, as they pick up some supplies," \
                    f" and proceed walk away."
            elif tribute2.weapon == 'a fucking gun':
                return f"A single gunshot freezes all the tributes in place as {t1} casually strolls in waving" \
                    f" {tribute1.hisher} gun around with {t2} behind {tribute1.himher}, as they pick up some supplies," \
                    f" and proceed walk away."
    if num == -1:
        # if neither tribute needs supplies or weapons
        if ((tribute1.weapon is not None) and (tribute2.weapon is not None) and
                (tribute1.supplies is not None) and (tribute2.supplies is not None)):
            scenario = 1
        elif tribute1.weapon is None and tribute2.weapon is None:
            scenario = 0
        else:
            scenario = random.randint(0, 1)

        if scenario == 0:  # scavenging time
            if tribute1.weapon is None and tribute2.weapon is not None:
                tribute1.weapon = random.choice(weapon_list)
                choice = random.choice([f'wedges free a {tribute1.weapon} stuck on a podium',
                                        f'grabs a {tribute1.weapon} sticking up in the ground',
                                        f"grabs a {tribute1.weapon} lying near a decaying corpse"])
                return f"{t2} wards malevolent tributes off with {tribute2.hisher} {tribute2.weapon} while {t1} {choice}."

            elif tribute1.weapon is not None and tribute2.weapon is None:
                tribute2.weapon = random.choice(weapon_list)
                choice = random.choice([f'wedges free a {tribute1.weapon} stuck on a podium',
                                        f'grabs a {tribute1.weapon} sticking up in the ground',
                                        f"grabs a {tribute1.weapon} lying near a decaying corpse"])

                return f"{t1} wards malevolent tributes off with {tribute1.hisher} {tribute1.weapon} while {t1} {choice}."

            elif tribute1.supplies is None or tribute2.supplies is None:  # either of them doesn't have supplies
                choice = random.choice(['hidden behind a podium', "from a dead tribute's bag"])
                # check and set both of their supplies to medkits
                if tribute1.supplies is None:
                    tribute1.supplies = 'medkit'
                elif tribute2.supplies is None:
                    tribute2.supplies = 'medkit'

                if tribute1.weapon is not None:
                    return f"{t1} wards malevolent tributes off with {tribute1.hisher} {tribute1.weapon} while {t2}" \
                        f" snags a medkit {choice}."
                elif tribute2.weapon is not None:
                    return f"{t2} wards malevolent tributes off with {tribute2.hisher} {tribute2.weapon} while {t1}" \
                        f" snags a medkit {choice}."
                else:
                    temp = random.randint(0, 2)
                    if temp == 0:
                        return f"{t1} and {t2} hide in the foliage and lay low until they manage to snag a medkit {choice}."
                    else:
                        if tribute1.supplies is not None:
                            tribute1.supplies = None
                        elif tribute2.supplies is not None:
                            tribute2.supplies = None
                        return f"Another tribute manages to steal {t1} and {t2}'s supplies, and as the bloodshed" \
                            f" continues, they decide to cut their losses and retreat."
            else:  # they both have supplies but neither has weapons
                temp = random.randint(0, 2)
                if temp == 0:
                    tribute1.weapon = random.choice(weapon_list)
                    tribute2.weapon = random.choice(weapon_list)
                    return f"{t1} and {t2} work together to find weapons in the bloodshed and manage to scavenge a" \
                    f" {tribute1.weapon} and a {tribute2.weapon} respectively."
                else:
                    tribute1.inj = True
                    tribute2.inj = True
                    return f"{t1} and {t2} are both wounded while fighting through the bloodshed and decide to" \
                        f" retreat while they still can."

        elif scenario == 1:  # teaming up is basically cheating tbh
            other_tribs = [trib for trib in tributes if not trib.done]

            # Decides how many tributes the pair get to kill. Triple kill only reserved for pairs with two weapons.
            if len(other_tribs) >= 3 and (tribute1.weapon is not None and tribute2.weapon is not None):
                temp = 3
            elif len(other_tribs) >= 2:
                temp = 2
            elif len(other_tribs) >= 1:
                temp = random.randint(0, 1)
            else:
                temp = 0

            if temp == 0:
                return_output = random.choice([f"{t1} and {t2} hide it out and observe the bloodbath from a distance,"
                                               f" but after an arrow whizzes by, they decide to flee while they still"
                                               f" have a chance.",
                                               f"On the way to the Cornucopia, {t1} has a mental breakdown and {t2}"
                                               f" decides that they'd be better off not going.",
                                               f"{t1} and {t2} try and score some kills, but the other tributes put up"
                                               f" a better fight than they expected, so they decide to retreat for now.",
                                               f"{t1} and {t2} fight their way through the to the center of the"
                                               f" Cornucopia, but get bamboozled when they find nothing there."])
                return return_output

            elif temp == 1:
                tribute3 = other_tribs[0]

                trib1_kill = random.choice([True, False])
                if trib1_kill:
                    tribute1.kills += 1
                else:
                    tribute2.kills += 1
                kill(tribute3)

                return f"{t1} and {t2} fight together and skewer {tribute3.name} in the bloodshed."
            elif temp == 2:
                tribute3 = other_tribs[0]
                tribute4 = other_tribs[1]

                tribute1.kills += 1
                tribute2.kills += 1
                kill(tribute3)
                kill(tribute4)

                return f"{t1} and {t2} fight synchronously amidst the bloodbath, and together they manage to slay both" \
                    f" {tribute3.name} and {tribute4.name} with ease."
            elif temp == 3:
                tribute3 = other_tribs[0]
                tribute4 = other_tribs[1]
                tribute5 = other_tribs[2]

                trib1_kill = random.choice([True, False])
                if trib1_kill:
                    tribute1.kills += 2
                    tribute2.kills += 1
                else:
                    tribute2.kills += 2
                    tribute1.kills += 1
                kill(tribute3)
                kill(tribute4)
                kill(tribute5)

                return f"{t1} and {t2} go into a frenzy, and as they both have each other's backs, they are" \
                    f" nigh-invincible as they cut down {tribute3.name}, {tribute4.name}, and {tribute5.name}."

    elif num == 0:  # no tribute encounter scenarios
        if tribute1.weapon is None:
            tribute1.weapon = random.choice(weapon_list)
            choice = random.choice([f'wedges free a {tribute1.weapon} stuck on a podium',
                                    f'grabs a {tribute1.weapon} sticking up in the ground',
                                    f"grabs a {tribute1.weapon} lying near a decaying corpse"])
            return f"{t1} {choice} and swings it around once or twice to ward off other tributes, before running away from" \
                f" the Cornucopia as fast as {tribute1.heshe} can."
        elif tribute1.supplies is None:
            tribute1.supplies = 'medkit'
            choice = random.choice(['hidden behind a podium', "from a dead tribute's bag"])
            return f"{t1} manages to grab a medkit {choice} and runs away from the Cornucopia as fast as" \
                f" {tribute1.heshe} can."
        else:  # the rare scenario where trib2 is None but trib1 is fully equipped
            return f"{t1} fights {tribute1.hisher} way through to the Cornucopia using {tribute1.hisher}" \
                f" {tribute1.weapon}, and secures some supplies before retreating."


    elif num >= 1:  # time for a bloodbath
        tribute2.done = True

        # if tribute2 has a gun or a cursed sword, RIP tribute1
        if tribute2.weapon == 'a fucking gun':
            tribute2.kills += 1
            kill(tribute1)
            return f"{t1} tries to kill {t2} but {t2} pulls out {tribute2.hisher} gun and shoots {t1} in the head."
        elif tribute2.weapon == 'cursed sword':
            tribute2.kills += 1
            kill(tribute1)
            return f"{t1} tries to kill {t2} but {t2} decides to unsheathe {tribute2.hisher} cursed sword, and a" \
                f" single swipe in the air is enough to atomize {t1}."

        # if both of them have weapons or if t1 has weapons, t1 always wins out (because fuck you, it's easier this way)
        # well, expect for when it explodes
        if (tribute1.weapon is not None and tribute2.weapon is not None) or (tribute1.weapon is not None):
            return feast_fight(tribute1, tribute2)
        elif tribute2.weapon is not None:
            return feast_fight(tribute2, tribute1)
        else:
            tribute1.weapon = random.choice(weapon_list)  # it's christmas, boys
            if tribute1.weapon == 'explosives':
                kill(tribute1)
                kill(tribute2)
                random_trib_list = [trib for trib in tributes if not trib.done]
                if len(random_trib_list) > 0:
                    random_trib = random.choice(random_trib_list)
                    kill(random_trib)
                    return f"{t1} sets some explosives off to blow {t2} to smithereens but" \
                        f" ends up blowing both of them up instead, along with {random_trib.name}, who was unlucky enough " \
                        f"to be in the blast range."
                else:
                    return f"{t1} sets some explosives off to blow {t2} to smithereens but" \
                        f" ends up blowing both of them up instead."
            elif tribute1.weapon in cleavers:
                tribute1.kills += 1
                kill(tribute2)
                return f"{t1} wedges free a {tribute1.weapon} stuck on a podium and uses it to cut down {t2} in a" \
                    f" single stroke."
            elif tribute1.weapon in stabbers:
                tribute1.kills += 1
                kill(tribute2)
                return f"{t1} picks up a {tribute1.weapon} sticking up in the ground and slits {t2}'s throat."
            elif tribute1.weapon in clubbers:
                tribute1.kills += 1
                kill(tribute2)
                if len(deadthisday) > 0:
                    temp = random.choice(deadthisday)
                    return f"{t1} grabs a {tribute1.weapon} lying near {temp.name}'s corpse and bashes {t2}'s skull" \
                        f" in with it."
                else:
                    return f"{t1} grabs a {tribute1.weapon} lying near a dead tribute's corpse and bashes {t2}'s" \
                        f" skull in with it."

            elif tribute1.weapon == 'bow' or tribute1.weapon == 'blowdart':
                tribute2.kills += 1
                tribute2.weapon = tribute1.weapon
                kill(tribute1)
                return f"{t1} grabs a backpack and finds a {tribute1.weapon}, but before {tribute1.heshe} can react," \
                    f" {t2} punches {tribute1.himher} down and strangles {tribute1.himher} to death, before stealing" \
                    f" the {tribute1.weapon}."


# ============================================================================


def do_things(tributes_list, pick_action_function):
    global events, tributes

    # So, since we modify the list during the iterations it gets all fucky if I don't iterate through the original
    # state of the list, which is why I make a shallow copy at the start and iterate through that
    tributes_list_copy = tributes_list.copy()
    for tribute in tributes_list_copy:
        # Check if the tribute has been yeeted out from the original list
        if tribute not in tributes_list:
            continue

        # Check if a tribute has a partner, and they're alive: if so, pair em up, else choose a random one
        if tribute.partner is not None and tribute.partner in tributes:
            rTrib = tribute.partner
            rTrib.done = True
        else:
            tribute.partner = None  # just for when the partner has died
            othertribs = [trib for trib in tributes_list if (trib != tribute and not trib.done and trib.partner is None)]  # yay for list comprehension

            if len(othertribs) == 0:  # if there isn't anyone suitable, set it to none
                rTrib = None
            else:  # otherwise, pick a random tribute
                rTrib = random.choice(othertribs)

        if tribute.done:  # check if the tribute has already participated in an event
            continue

        tribute.done = True
        events.append(pick_action_function(tribute, rTrib))

        # If there is only 1 tribute left, yeet out
        if len(tributes) <= 1:
            return False

    return True


def Feast():
    global tributes, events, day
    for tribute in tributes:
        tribute.done = False
    events.append("**The Feast**")
    events.append("The cornucopia is replenished with food, supplies, weapons.")
    return do_things(tributes, pick_random_feast_action)


def Day():
    global tributes, events, day
    for tribute in tributes:
        tribute.done = False
    events.append(f"**Day {day}**\n")  # say what day it is
    return do_things(tributes, pick_random_action)


def Night():
    global tributes, events, day
    for tribute in tributes:
        tribute.done = False
    events.append(f"**Night {day}**\n")
    return do_things(tributes, pick_random_night_action)


def Cannons():
    global deadthisday, events
    events.append(f"\n**{len(deadthisday)} cannon shots go off in the distance.**")
    for i in range(len(deadthisday)):
        events.append(f"{deadthisday[i].name} - District {deadthisday[i].district}\n")
    deadthisday = []


# ===========================================================================

def game(message):
    global events, day, tributes
    if initializing:
        return initialize(message)
    if message.content == 'next!':
        random.shuffle(tributes)  # makes it more fair
        events = []

        if (day + 1) % 5 == 1 and day != 1:
            if not Feast():
                event_copy = events
                final_stats = finish()
                return event_copy + final_stats
        # checks if game is finished
        if not Day():
            for count, event in enumerate(events):
                events[count] = correct_grammar(event)
            event_copy = events
            final_stats = finish()
            return event_copy + final_stats
        if not Night():
            for count, event in enumerate(events):
                events[count] = correct_grammar(event)
            event_copy = events
            final_stats = finish()
            return event_copy + final_stats

        Cannons()  # List all the tributes who died
        day += 1
        for count, event in enumerate(events):
            events[count] = correct_grammar(event)
        return events

    elif message.content == 'reset!':
        reset()
        return ['Game reset. Use ``hunger games start!`` to start again', 'Finished!']

def reset():
    global numOfDistricts, initializing, numOfTributes, events, tributes, dead, deadthisday, day
    numOfDistricts = 0
    initializing = True
    numOfTributes = 1
    events = []
    tributes = []
    dead = []
    deadthisday = []
    day = 1


def finish():
    global numOfDistricts, events, tributes, dead
    the_end = []
    if len(tributes) > 0:
        the_end.append(f"**{tributes[0].name} from District {tributes[0].district} survived the Hunger Games!**")
    else:
        the_end.append("**Everyone died! YAY!**")
    the_end.append("**Order of death**")
    for i in range(len(dead)):  # For each dead tribute
        the_end.append(f"{(numOfDistricts * 2) - i}: {dead[i].name}")  # List the name and time of death of the tribute.
    # Explanation of (numOfDistricts*2)-i
    # numOfDistricts is the number of districts in the game.
    # Since this is player defined we need a formula to find last place. It isn't necessarily 12.
    # So The total number of districts is last place. Then it multiplies it by 2 to get the number of tributes.
    # i is the current position of this function in the array. The farther along it is, the higher the position of the
    # tribute, so the position and ranking have an inverse relationship.

    the_end.append("**Kills**")
    for i in range(len(dead)):  # For each dead tribute
        tributes.append(dead[i])

    # Sort the tributes by number of kills
    killorder = []
    while len(killorder) < (numOfDistricts * 2):
        highest = 0
        nextHighest = None
        for i in range(len(tributes)):
            if tributes[i].kills > highest:
                highest = tributes[i].kills
                nextHighest = tributes[i]
            if nextHighest == None:
                nextHighest = tributes[0]
        tributes.remove(nextHighest)
        killorder.append(nextHighest)

    for i in range(len(killorder)):
        the_end.append(f"{killorder[i].kills} - {killorder[i].name}")
    the_end.append('Finished!')

    reset()

    return the_end