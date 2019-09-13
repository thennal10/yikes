# The Hunger Games
from math import ceil
import random
import time

numOfDistricts = 0  # set the number of districts
initializing = True
numOfTributes = 1
# initialize some more stuff
events = []
tributes = []
dead = []
deadthisday = []
day = 1
weapon_list = ['axe', 'cleaver', 'naked waifu figurine', 'pickaxe', 'broadsword', 'bow', 'blowdart', 'anime DVD',
               'dagger', 'giant screwdriver', 'wooden club', "peach's lost phone", 'explosives']
rare_weapons_list = ['cursed sword', 'a fucking gun']

class Tribute:

    def __init__(self, nme, dist):
        self.name = nme[:-2]  # Set the name to whatever the player entered MINUS the gender and space at the end
        self.district = dist  # set the district to whatever it was assigned to.
        self.inj = False  # set inj to false by default
        self.supplies = 'None'
        self.weapon = 'None'
        self.partner = 'None'
        self.asleep = False
        self.kills = 0
        self.gender = nme[(len(nme) - 1):]  # get the gender the player entered. the last letter of the input

        if self.gender.lower() == "m":  # if the player is male
            # give him male pronouns
            self.hisher = "his"
            self.himher = "him"
            self.heshe = "he"
        elif self.gender.lower() == "f":
            # give her female pronouns
            self.hisher = "her"
            self.himher = "her"
            self.heshe = "she"
        else:
            # give them nonbinary pronouns
            # you friggin sjw ree
            self.hisher = "their"
            self.himher = "them"
            self.heshe = "they"


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
            return  f"Name tribute #{numOfTributes}\n"
        else:
            tributes.append(Tribute(message.content, ceil(numOfTributes / 2)))
            return_string = ""
            for j in range(len(tributes)):
                # Print their name, district, and gender. This is mainly for debugging purposes.
                return_string += (f"{tributes[j].name}, district {tributes[j].district}, {tributes[j].gender}\n")
            initializing = False
            return return_string



# ===============================================================================

def pickRandomAction(tribute1, tribute2):
    global tributes, dead, deadthisday
    # make their names easier to access.
    t1 = tribute1.name
    t2 = tribute2.name

    # Picks between three overarching scenarios
    num = random.randint(0, 3)

    if num == 0: # tribute encounter

        aggro_multiplier = 1
        # checks if either tribute has weapons
        if tribute1.weapon != 'None' is not tribute2.weapon != 'None':
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
            tribute1.partner = t2
            tribute2.partner = t1
            return f"{t1} and {t2} decide to stick together for the day and go hunting for supplies."
        elif scenario == 4:
            temp = random.randint(0, 9)
            if temp == 9:
                return f"{t1} and {t2} have hot, steamy, sweaty sex, then go about their separate ways."
            else:
                tribute1.partner = t2
                tribute2.partner = t1
                return f"{t1} and {t2} decide to team up and hunt other tributes."
        elif scenario == 5:
            tribute1.partner = t2
            tribute2.partner = t1
            return f"{t1} and {t2} remember an anime-watching contract that they forged long ago, and in its honour, decide to team up."
        # 6+ violent scenarios
        elif scenario > 5:
            # figure out who's stronger
            even = False
            if tribute1.weapon != 'None' and tribute2.weapon == 'None':
                if not tribute1.inj or tribute2.inj:
                    strong = tribute1
                    weak = tribute2
                strong = tribute1
                weak = tribute2
                even = True
            elif tribute2.weapon != 'None' and tribute1.weapon == 'None':
                if not tribute2.inj or tribute1.inj:
                    strong = tribute2
                    weak = tribute1
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
                        tributes.remove(strong)
                        dead.append(strong)
                        deadthisday.append(strong)
                        return f"{wk} uses the ancient power of {weak.hisher} {weak.weapon} to banish {str} into oblivion."
                    if strong.weapon == 'cursed sword':
                        strong.kills += 1
                        tributes.remove(weak)
                        dead.append(weak)
                        deadthisday.append(weak)
                        return f"{str} uses the ancient power of {strong.hisher} {strong.weapon} to banish {wk} into oblivion."
                elif temp == 1:
                    if weak.weapon == 'cursed sword':
                        weak.inj = True
                        weak.kills += 1
                        tributes.remove(strong)
                        dead.append(strong)
                        deadthisday.append(strong)
                        return f"{wk} scorches {str} to dust using the overwhelming power of {weak.hisher} " \
                            f"{weak.weapon}, but injures {weak.himher}self in the process."
                    if strong.weapon == 'cursed sword':
                        strong.inj = True
                        strong.kills += 1
                        tributes.remove(weak)
                        dead.append(weak)
                        deadthisday.append(weak)
                        return f"{str} scorches {wk} to dust using the overwhelming power of {strong.hisher} " \
                            f"{strong.weapon}, but injures {strong.himher}self in the process."
                elif temp == 2:
                    tributes.remove(weak)
                    tributes.remove(strong)
                    dead.append(weak)
                    dead.append(strong)
                    deadthisday.append(weak)
                    deadthisday.append(strong)
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
                    tributes.remove(weak)
                    dead.append(weak)
                    deadthisday.append(weak)
                    if temp == 2:
                        strong.weapon = 'None'
                        return f"{str} just straights up shoots {wk} in the head with {strong.hisher} gun, but runs " \
                            f"out of bullets in the process."
                    else:
                        return f"{str} just straights up shoots {wk} in the head with {strong.weapon}."
                elif weak.weapon == 'a fucking gun':
                    weak.kills += 1
                    tributes.remove(strong)
                    dead.append(strong)
                    deadthisday.append(strong)
                    if temp == 2:
                        weak.weapon = 'None'
                        return f"{wk} just straights up shoots {str} in the head with {weak.weapon}, but runs " \
                            f"out of bullets in the process."
                    else:
                        return f"{wk} just straights up shoots {str} in the head with {weak.weapon}."

            elif strong.weapon == 'explosives' or weak.weapon == 'explosives':
                tributes.remove(weak)
                tributes.remove(strong)
                dead.append(weak)
                dead.append(strong)
                deadthisday.append(weak)
                deadthisday.append(strong)
                if weak.weapon == 'explosives':
                    return f"{wk} tries to defend {weak.himher}self using {weak.weapon} but blows both of them up in " \
                        f"the process."
                elif strong.weapon == 'explosives':
                    return f"{str} tries to defend {strong.himher}self using {strong.weapon} but blows both of them up in " \
                        f"the process."

            elif strong.weapon == 'axe' or strong.weapon == 'cleaver' or strong.weapon == 'broadsword':
                if even:
                    weak.inj = True
                    return f"{str} tries to cleave {wk} in two but {wk} manages to escape with {weak.hisher} life, albeit injured."
                else:
                    strong.kills += 1
                    tributes.remove(weak)
                    dead.append(weak)
                    deadthisday.append(weak)
                    if scenario > 7:
                        return f"{str} savagely decapitates {wk} with {strong.hisher} {strong.weapon}."
                    else:
                        return f"{str} cuts {wk} down with {strong.hisher} {strong.weapon} in a single stroke."

            elif strong.weapon == 'dagger' or strong.weapon == 'giant screwdriver' or strong.weapon == 'naked waifu figurine':
                if even:
                    weak.inj = True
                    return f"{str} stabs {wk} in the gut with a {strong.weapon}, but {wk} manages to push {strong.himher} off and run away."
                else:
                    strong.kills += 1
                    tributes.remove(weak)
                    dead.append(weak)
                    deadthisday.append(weak)
                    if scenario > 7:
                        return f"A well aimed stab by {str}'s {strong.weapon} ends {wk}'s miserable life."
                    else:
                        return f"After a drawn-out fight, {str} manages to catch {wk} in the throat with {strong.hisher}" \
                            f" {strong.weapon} and scores a kill."

            elif strong.weapon == 'wooden club' or strong.weapon == 'anime DVD' or strong.weapon == "peach's lost phone":
                if even:
                    weak.inj = True
                    return f"{str} tries to club {wk} with {strong.hisher} {strong.weapon}, but {wk} blocks and dodges," \
                        f"before making a run for it the first chance {weak.heshe} got."
                else:
                    strong.kills += 1
                    tributes.remove(weak)
                    dead.append(weak)
                    deadthisday.append(weak)
                    if scenario > 7:
                        return f"{str} brutally smashes {wk}'s head in with {strong.hisher} {strong.weapon}"
                    else:
                        return f"A single swing of {str}'s {strong.weapon} is enough to take out {wk}."

            elif strong.weapon == 'bow' or strong.weapon == 'blowdart':
                if strong.weapon == 'bow':
                    weak.inj = True
                    return f"{str} stealthily shoots arrows from the cover of foliage at {wk}, but {wk} manages to " \
                        f"escape with {weak.hisher} life, albeit wounded"
                if strong.weapon == 'blowdart':
                    weak.inj = True
                    return f"{str} stealthily shoots poisoned darts from the cover of foliage at {wk}, but {wk} manages to " \
                        f"escape with {weak.hisher} life, albeit with poison flowing through {weak.hisher} veins."

            else:
                if strong.inj and weak.inj:
                    tributes.remove(weak)
                    tributes.remove(strong)
                    dead.append(weak)
                    dead.append(strong)
                    deadthisday.append(weak)
                    deadthisday.append(strong)
                    return  f"In a magnificent display of manliness, an injured {str} and {wk} fight it out to the " \
                        f"death, and simultaneously collapse with smiles on their faces."
                elif even:
                    strong.inj = True
                    weak.inj = True
                    return f"{str} and {wk} brawl it out, but they seem evenly matched, and they both decide to flee" \
                        f" when the chance came"
                else:
                    strong.inj = True
                    strong.kills += 1
                    tributes.remove(weak)
                    dead.append(weak)
                    deadthisday.append(weak)
                    if scenario > 7:
                        return f"{str} dismembers a weakened {wk} using {strong.hisher} bare hands, though not before getting" \
                            f" injured {strong.himher}self."
                    else:
                        return f"{str} remembers the words of {strong.hisher} old boxing coach, and on the brink of death, while the anime OP plays in" \
                            f"the background, KO's {wk} in one final punch."

    elif num == 1: # supply/weapon encounter
        temp = random.randint(0, 10)
        if temp == 0:
            if tribute1.inj:
                tribute1.inj = False
                return f"{t1} finds a pile of fluffy BL manga lying around, and while reading it magically recovers from {tribute1.hisher} " \
                    f"wounds due to the sheer purity of gay."
            else:
                tribute1.supplies = 'BL'
                return f"{t1} finds a pile of fluffy BL manga lying around, and {tribute1.heshe} decides to bring it along with {tribute1.himher}" \
                    f" on {tribute1.hisher} journeys."
        elif temp == 1:
            if tribute1.inj:
                tribute1.inj = False
                return f"{t1} finds a pile of fluffy yuri manga lying around, and while reading it magically recovers from {tribute1.hisher} " \
                    f"wounds due to the sheer purity of gay."
            else:
                tribute1.supplies = 'yuri'
                return f"{t1} finds a pile of fluffy yuri manga lying around, and {tribute1.heshe} decides to bring it along with {tribute1.himher}" \
                    f" on {tribute1.hisher} journeys."
        elif temp == 2:
            if tribute1.inj:
                tribute1.inj = False
                return  f"{t1} finds a medkit lying around and uses it to patch {tribute1.himher}self up."
            else:
                tribute1.supplies = 'medkit'
                return f"{t1} finds a medkit lying around."
        elif temp == 3:
            if tribute1.inj:
                tribute1.inj = False
                return  f"{t1} recieves a supply drop containing medicine from an unknown sponsor, and uses it to treat {tribute1.hisher} wounds."
            else:
                tribute1.supplies = 'medkit'
                return f"{t1} recieves a supply drop containing medicine from an unknown sponsor."
        elif temp == 4:
            if tribute1.inj:
                tribute1.inj = False
                return f"{t1} finds a picture of {random.choice(['Yuki from Tsuritama', 'Shouko Nishimiya', 'Shouya Ishida', 'Nadeshiko from Yuru Camp', 'Naru from Barakamon', 'Prince from Kazetsuyo', 'Ushio from Clannad', 'Connor'])} smiling and all {tribute1.hisher} injuries are healed instantly."
            else:
                return f"{t1} finds a picture of {random.choice(['Yuki from Tsuritama', 'Shouko Nishimiya', 'Shouya Ishida', 'Nadeshiko from Yuru Camp', 'Naru from Barakamon', 'Prince from Kazetsuyo', 'Ushio from Clannad', 'Connor'])} smiling and all {tribute1.hisher} worries immediately dissipate."
        elif temp == 5:
            n_temp = random.randint(0, 4)
            if n_temp == 4:
                tribute1.supplies = 'weird amulet'
                return f"While exploring a hidden grove, {t1} encounters multiple stone monuments arranged in a " \
                    f"circle, with an amulet on a podium in the center. {t1}, never having played a videogame or " \
                    f"watched a movie, grabs the amulet without a second thought."
            else:
                if tribute1.inj:
                    tribute1.inj = False
                    return f"{t1} chances upon some medicinal herbs and applies it on {tribute1.hisher} wounds."
                else:
                    tribute1.supplies = 'herbs'
                    return f"{t1} chances upon some medicinal herbs and decides to collect some for later use."
        elif temp < 8 and tribute1.weapon == 'None':
            new_weapon = random.choice(weapon_list)
            tribute1.weapon = new_weapon
            return f"{t1} finds a {new_weapon} while scavenging through {random.choice(['a shed', 'a warehouse', 'some bushes'])}."
        elif temp < 10 and tribute1.weapon == 'None':
            new_weapon = random.choice(weapon_list)
            tribute1.weapon = new_weapon
            return f"{t1} receives a supply drop containing a {new_weapon} from an unknown sponsor."
        elif temp == 10:
            n_temp = random.randint(0, 4)
            if n_temp == 4:
                new_weapon = random.choice(rare_weapons_list)
                tribute1.weapon = new_weapon
                if new_weapon == 'cursed sword':
                    return f"After a lengthy set of obstacles and puzzles in an ancient stone temple, {t1} finally reaps" \
                        f" the reward for {tribute1.hisher} effort; a {new_weapon}, embedded with unimaginable power."
                elif new_weapon == 'a fucking gun':
                    return  f"Breaking through a hidden safe with {tribute1.hisher} 1337 technical skills " \
                        f"({tribute1.heshe} used a hammer), {t1} finds {new_weapon} stored compactly inside."
            else:
                new_weapon = random.choice(weapon_list)
                tribute1.weapon = new_weapon
                return f"{t1} recieves a supply drop containing a {new_weapon} from an unknown sponsor."
        else:
            return f"{t1} tests out {tribute1.hisher} {tribute1.weapon} against " \
                f"{random.choice(['some wild boars', 'a scarecrow', 'an odd-looking boulder', 'an effigy of Donald Trump'])}"

    elif num >= 2: # environment encounter
        temp = random.randint(0,22)

        if temp == 0:
            return f"{t1} picks some flowers."
        elif temp == 1:
            return f"{t1} thinks about home."
        elif temp == 2:
            tribute1.inj = True
            return f"{t1} tries to eat something inedible and regrets it."
        elif temp == 3:
            tribute1.inj = True
            return f"{t1} tries some wild mushrooms hoping to get high, but all {tribute1.heshe} gets is a bad case of diarrhea."
        elif temp == 4:
            return f"{t1} tries some wild mushrooms and lucks out; {tribute1.heshe} spends the rest of the day " \
                f"tripping on shrooms."
        elif temp == 5:
            return f"{t1} starts talking to {tribute1.himher}self."
        elif temp == 6:
            return f"{t1} steps in something indescribable."
        elif temp == 7:
            n_temp = random.randint(0, 10)
            if n_temp == 10:
                tributes.remove(tribute1)
                dead.append(tribute1)
                deadthisday.append(tribute1)
                return f"{t1} dies of dysentery after drinking unboiled river water. This is wilderness survival 101" \
                    f" folks, jeez."
            else:
                return f"{t1} finds a river and decides to stick close to it."
        elif temp == 8:
            n_temp = random.randint(0, 10)
            if n_temp != 6:
                tribute1.inj = True
                return f"{t1} gets bit by a savage bunny with a british accent."
            else:
                tributes.remove(tribute1)
                dead.append(tribute1)
                deadthisday.append(tribute1)
                return f"{t1} gets murdered by a savage bunny with a british accent."
        elif temp == 9:
            tributes.remove(tribute1)
            dead.append(tribute1)
            deadthisday.append(tribute1)
            return f"{t1} steps on a landmine and gets yeeted into the stratosphere."
        elif temp == 10:
            tributes.remove(tribute1)
            dead.append(tribute1)
            deadthisday.append(tribute1)
            return f"{t1} chances upon a small book simply titled 'Breaking Bad Coworker's Journal'. After reading a" \
                f" couple pages, {tribute1.heshe} promptly decides to jump off a cliff and commit suicide."
        elif temp == 11:
            tribute1.inj = True
            return f"{t1}'s dumb ass falls into a hole and breaks {tribute1.hisher} leg."
        elif temp == 12:
            return f"{t1} carves {tribute1.hisher} initials into a tree."
        elif temp == 13:
            return f"{t1} ponders the human condition."
        elif temp == 14:
            if len(dead) > 0:
                n_temp = random.randint(0, len(dead) - 1)
                return f"{t1} finds {dead[n_temp].name}'s corpse."
            else:
                return f"{t1} dreams about the time {tribute1.heshe} wasn't stuck in some idiotic simulation of *hunger games*," \
                    f" and a bad one to boot."
        elif temp == 15:
            return f"{t1} manages to hunt down a " \
                f"{random.choice(['squirrel', 'boar', 'rabbit', 'green amorphous blob-looking thing'])} and eats it."
        elif temp == 16:
            return f"{t1} looks desperately around for something to eat, to no avail."
        elif temp == 17:
            return f"{t1} does some exploring."
        elif temp == 18:
            return f"{t1} finds a stash of Harada doujins, and upon reading one is promptly traumatized for life."
        elif temp == 19:
            return f"{t1} finds a blu-ray collection of {random.choice(['Haikyuu!', 'K-ON!', 'Fullmetal Alchemist'])} and" \
                f" has no choice but to spend the entire day rewatching that shit."
        elif temp == 20:
            return f"{t1} thinks about all the fun {tribute1.heshe}'s had with {tribute1.hisher} frie- oh wait, {t1}" \
                f" doesn't have any. Whoops."
        elif temp == 21:
            return f"{t1} can't find a decent source of water, and nearly gives in before remembering that one" \
                f" Bear Grylls meme, and decides to drink {tribute1.hisher} own piss. Fresh and hot."
        elif temp == 22:
            if tribute1.inj:
                tributes.remove(tribute1)
                dead.append(tribute1)
                deadthisday.append(tribute1)
                return f"{t1} is bit by a snake and dies, because no one ever told {tribute1.himher} how to tie" \
                    f" a tourniquet."
            else:
                tribute1.inj = True
                return f"{t1} is bit by a snake, but manages to wear off the poison."


def pickRandomNightAction(tribute1, tribute2):
    # This is the same as pickRandomAction(), just with a different scenario set.
    global tributes, dead, deadthisday
    t1 = tribute1.name
    t2 = tribute2.name
    num = random.randint(0, 21)
    tribute1.asleep = False

    if tribute1.supplies == 'weird amulet':
        temp = random.randint(0, 2)
        if temp == 0:
            tribute1.supplies == 'None'
            return f"{t1} fiddles around with {tribute1.hisher} weird amulet, but nothing happens at all."
        elif temp == 1:
            tribute1.supplies == 'None'
            tribute1.weapon = 'cursed sword'
            return f"{t1} fiddles around with {tribute1.hisher} weird amulet, and in a sudden puff of purple smoke, " \
                f"it transforms into a cursed sword."
        elif temp == 2:
            tribute1.supplies == 'None'
            tributes.remove(tribute1)
            dead.append(tribute1)
            deadthisday.append(tribute1)
            return f"{t1} tries to get some sleep, when in a sudden puff of smoke, {tribute1.hisher} weird amulet" \
                f"randomly summons a winged monstrosity that dismembers {t1} before flying off into the night sky"

    if tribute1.supplies != 'None' and tribute1.inj:
        if tribute1.supplies == 'medkit':
            tribute1.inj = False
            tribute1.supplies = 'None'
            return f"{t1} patches up {tribute1.hisher} injuries using a medkit {tribute1.heshe} had grabbed along the" \
                f"way."
        elif tribute1.supplies == 'BL':
            tribute1.inj = False
            tribute1.supplies = 'None'
            return f"{t1} reads a random fluffy oneshot from the BL collection {tribute1.heshe} picked up and" \
                f" {tribute1.hisher} injuries are immediately healed from the power of gay."
        elif tribute1.supplies == 'yuri':
            tribute1.inj = False
            tribute1.supplies = 'None'
            return f"{t1} reads a random fluffy oneshot from the yuri collection {tribute1.heshe} picked up and" \
                f" {tribute1.hisher} injuries are immediately healed from the power of gay."
        elif tribute1.supplies == 'herbs':
            tribute1.inj = False
            tribute1.supplies = 'None'
            return f"{t1} patches up {tribute1.hisher} injuries using the medicinal herbs {tribute1.heshe} had " \
                f"collected along the way."

    if num == 0:
        tribute1.asleep = True
        return f"{t1} cries {tribute1.himher}self to sleep."
    elif num == 1:
        tribute1.inj = True
        return f"{t1} walks around in circles, unable to sleep."
    elif num == 2:
        tribute1.asleep = True
        return f"{t1} uses {tribute1.hisher} survival skills that {tribute1.heshe} learned from watching Bear Grylls " \
            f"24/7 and makes a shelter out of sticks and leaves to sleep in."
    elif num == 3:
        if tribute2.asleep == True:
            tributes.remove(tribute2)
            dead.append(tribute2)
            deadthisday.append(tribute2)
            tribute1.kills += 1
            return f"{t1} covetly sneaks up on and kills {t2} in {tribute1.hisher} sleep."
        else:
            if tribute2.weapon != 'None':
                tribute1.inj = True
                return f"{t2} spots {t1} spying on {tribute2.himher}, and chases {t1} off with {tribute2.hisher} " \
                    f"{tribute2.weapon}"
            else:
                return f"{t2} spots {t1} spying on {tribute2.himher}, and chases {t1} off."
    elif num == 4:
        tribute1.asleep = True
        return f"{t1} falls asleep on a makeshift bed of leaves."
    elif num == 5:
        temp = random.randint(0, 1)
        if tribute1.inj == True:
            tributes.remove(tribute1)
            dead.append(tribute1)
            deadthisday.append(tribute1)
            return f"While looking for shelter, {t1} trips and falls onto some sharp rocks and bleeds out."
        else:
            if temp == 1:
                tribute1.inj = True
                return f"{t1} trips on some sharp rocks and gets knocked unconscious."
            else:
                tribute1.asleep = True
                return f"{t1} trips on some rocks, and then decides to sleep there."
    elif num == 6:
        temp = random.randint(0, 15)
        if temp == 1:
            tributes.remove(tribute1)
            dead.append(tribute1)
            deadthisday.append(tribute1)
            return f"{t1} sees a bleak future even with victory, and kills {tribute1.himher}self"
        else:
            tribute1.asleep = True
            return f"{t1} falls asleep in a flower patch."
    elif num == 7:
        tribute1.asleep = True
        return f"{t1} falls asleep pondering the human condition."
    elif num == 8:
        tribute1.asleep = False
        return f"{t1} stays awake all night as {tribute1.hisher} brain tortures {tribute1.himher} with memories of " \
            f"that one awkward moment {tribute1.heshe} had " \
            f"{random.choice(['in highschool', 'in a starbucks', f'while talking to {tribute1.hisher} crush'])}."
    elif num == 9:
        return f"{t1} practices {tribute1.hisher} " \
            f"{random.choice(['shadowboxing all night due to recently having watched Hajime no Ippo', 'spiking all night due to recently having watched Haikyuu'])}."
    elif num == 10:
        if tribute2.asleep == False:
            return f"{t1} spots {t2}, and slowly backs away."
        else:
            tribute1.inj = True
            return f"{t1} eats some wild berries for dinner and regrets it."
    elif num == 11:
        if tribute1.inj:
            tributes.remove(tribute1)
            dead.append(tribute1)
            deadthisday.append(tribute1)
            return f"{t1} gets bit by a bat and dies."
        else:
            tribute1.inj = True
            return f"{t1} gets bit by a bat."
    elif num == 12:
        return f"{t1} makes a campfire and reminisces about the good ol' days."
    elif num == 13:
        return f"{t1} spots a bear sitting on a tree. It looks at {tribute1.himher}, {tribute1.heshe} looks at it," \
            f" and then {t1} skedaddles on out of there."
    elif num == 14:
        tribute1.asleep = True
        return f"{t1} falls asleep in a ditch."
    elif num == 15:
        return f"{t1} sleeps with one eye open."
    elif num == 16:
        tribute1.asleep = True
        return f"{t1} has nightmares about that one NTR ugly bastard doujin {tribute1.heshe} read long ago."
    elif num == 17:
        tribute1.asleep = True
        return f"{t1} falls asleep admiring the beauty of the star-lit sky."
    elif num == 18:
        tribute1.asleep = True
        return f"{t1} dreams about {tribute1.himher}self as the victor."
    elif num == 19:
        if tribute1.weapon != 'None':
            return f"{t1} admires {tribute1.hisher} {tribute1.weapon} under the light of {tribute1.hisher} campfire."
        else:
            weapon = random.choice(['axe', 'dagger', 'cleaver'])
            tribute1.weapon = weapon
            return f"{t1} remembers that one Primitive Technology video {tribute1.heshe} saw and fastens a makeshift " \
                f"{weapon} from a stick and a sharpened rock."
    elif num == 20:
        return f"{t1} prays to God to let {tribute1.himher} survive this brutal ritual that they call the hunger " \
            f"games. God tells {t1} to shut the fuck up I'm trying to watch some Gundam here."
    elif num == 21:
        if tribute1.gender.lower() == "m":
            return f"{t1} jacks off in a nearby bush to relieve steam and accidentally summons a demon when he moved " \
                f"his penis in a special pattern."
        else:
            return f"{t1} draws a face on a coconut and talks to it all night."

# ============================================================================

def Day():
    global day, tributes, events

    events.append(f"**Day {day}**\n")  # say what day it is
    i = 0
    while i < len(tributes):  # for each living tribute...
        othertribs = []
        j = 0
        while j < len(tributes):
            if tributes[j] != tributes[i]:
                othertribs.append(tributes[j])
            j += 1
        rTrib = random.randint(0, len(othertribs) - 1)  # pick a random target tribute

        tribute = tributes[i]
        events.append(pickRandomAction(tributes[i], othertribs[rTrib]))
        if tribute in tributes:
            i += 1


def Night():
    global tributes, events
    events.append(f"**Night {day}**\n")
    i = 0
    while i < len(tributes):  # for each living tribute...
        othertribs = []
        for j in range(len(tributes)):
            if tributes[j] != tributes[i]:
                othertribs.append(tributes[j])

        rTrib = random.randint(0, len(othertribs) - 1)  # pick a random target tribute

        tribute = tributes[i]
        events.append(pickRandomNightAction(tributes[i], othertribs[rTrib]))
        if tribute in tributes:
            i += 1


def Cannons():
    global deadthisday, events
    events.append(f"\n**{len(deadthisday)} cannon shots go off in the distance.**")
    for i in range(len(deadthisday)):
        events.append(f"{deadthisday[i].name} - District {deadthisday[i].district}\n")
    deadthisday = []


# ===========================================================================

def game(message):
    global events, day
    if initializing:
        return initialize(message)
    if message.content == 'next!':
        events = []
        if len(tributes) <= 1:  # If there is only 1 tribute left
            final_stats = finish()
            return final_stats
        Day()  # Start a new day
        if len(tributes) <= 1:  # If there is only 1 tribute left
            final_stats = finish()
            return events + final_stats
        Night()  # Go on to night
        Cannons()  # List all the tributes who died
        day += 1
        return events

def finish():
    global numOfDistricts, initializing, numOfTributes, events, tributes, dead, deadthisday, day
    the_end = []
    if len(tributes) > 0:
        the_end.append(f"{tributes[0].name} from District {tributes[0].district} survived the Hunger Games!")
    else:
        the_end.append("Everyone died! YAY!")
    the_end.append("Order of death\n")
    for i in range(len(dead)):  # For each dead tribute
        the_end.append(f"{(numOfDistricts * 2) - i}: {dead[i].name}")  # List the name and time of death of the tribute.
    # Explanation of (numOfDistricts*2)-i
    # numOfDistricts is the number of districts in the game.
    # Since this is player defined we need a formula to find last place. It isn't necessarily 12.
    # So The total number of districts is last place. Then it multiplies it by 2 to get the number of tributes.
    # i is the current position of this function in the array. The farther along it is, the higher the position of the tribute, so the position and ranking have an inverse relationship.

    the_end.append("Kills\n")
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
    the_end.append('finish')

    # reset variables
    numOfDistricts = 0
    initializing = True
    numOfTributes = 1
    events = []
    tributes = []
    dead = []
    deadthisday = []
    day = 1

    return the_end