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
               'giant screwdriver', 'wooden club', 'scimitar', 'trident', 'mace', 'katana', 'rapier',
               'morning star', 'warhammer', 'halberd', 'spear', 'scythe', 'hatchet']
cleavers = ['axe', 'broadsword', 'cleaver', 'scimitar', 'katana', 'halberd', 'scythe', 'hatchet']
stabbers = ['dagger', 'giant screwdriver', 'trident', 'naked waifu figurine', 'rapier', 'spear']
clubbers = ['wooden club', 'anime DVD', 'mace', 'morning star', 'warhammer']
ranged = ['bow', 'blowdart']
rare_weapons_list = ['cursed sword', 'gun']


class Tribute:

    def __init__(self, nme, dist):
        self.name = nme[:-2]  # Set the name to whatever the player entered MINUS the gender and space at the end
        self.district = dist  # set the district to whatever it was assigned to.
        self.inj = False  # set inj to false by default
        self.supplies = None
        self.weapon = None
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

    def calculate_strength(self):
        score = 1
        if self.weapon is not None:
            score += 1
        if not self.inj:
            score += 1
        return score

    # Time for some long ass methods
    def pick_random_action(self):
        global tributes, dead, deadthisday

        t1 = self.name
        # num picks between three overarching scenarios
        other_tributes = [trib for trib in tributes if not trib.done]
        if len(other_tributes) == 0:
            tribute2 = None
            num = random.randint(1, 3)# skip tribute encounter scenarios
        else:
            num = random.randint(0, 3)
            tribute2 = random.choice(other_tributes)

        if num == 0:  # tribute encounter
            return sorting_hat(self, tribute2)
        elif num == 1: # supply/weapon encounter
            scenario = random.randint(0, 10)
            if scenario == 0:
                if self.inj:
                    self.inj = False
                    return f"{t1} finds a pile of fluffy BL manga lying around, and while reading it magically recovers from {self.hisher} " \
                        f"wounds due to the sheer purity of gay."
                else:
                    self.supplies = 'medkit'
                    return f"{t1} finds a medkit lying around."
            elif scenario == 1:
                if self.inj:
                    self.inj = False
                    return f"{t1} finds a pile of fluffy yuri manga lying around, and while reading it magically recovers from {self.hisher} " \
                        f"wounds due to the sheer purity of gay."
                else:
                    self.supplies = 'herbs'
                    return f"{t1} chances upon some medicinal herbs and decides to collect some for later use."
            elif scenario == 2:
                if self.inj:
                    self.inj = False
                    return  f"{t1} finds a medkit lying around and uses it to patch {self.himher}self up."
                else:
                    self.supplies = 'medkit'
                    return f"{t1} finds a medkit lying around."
            elif scenario == 3:
                if self.inj:
                    self.inj = False
                    return  f"{t1} recieves a supply drop containing medicine from an unknown sponsor, and uses it to treat {self.hisher} wounds."
                else:
                    self.supplies = 'medkit'
                    return f"{t1} recieves a supply drop containing medicine from an unknown sponsor."
            elif scenario == 4:
                if self.inj:
                    self.inj = False
                    return f"{t1} finds a picture of {random.choice(['Yuki from Tsuritama', 'Shouko Nishimiya', 'Shouya Ishida', 'Nadeshiko from Yuru Camp', 'Naru from Barakamon', 'Prince from Kazetsuyo', 'Ushio from Clannad', 'Connor'])} smiling and all {self.hisher} injuries are healed instantly."
                else:
                    return f"{t1} finds a picture of {random.choice(['Yuki from Tsuritama', 'Shouko Nishimiya', 'Shouya Ishida', 'Nadeshiko from Yuru Camp', 'Naru from Barakamon', 'Prince from Kazetsuyo', 'Ushio from Clannad', 'Connor'])} smiling and all {self.hisher} worries immediately dissipate."
            elif scenario == 5:
                temp = random.randint(0, 4)
                if temp == 4:
                    self.supplies = 'weird amulet'
                    return f"While exploring a hidden grove, {t1} encounters multiple stone monuments arranged in a " \
                        f"circle, with an amulet on a podium in the center. {t1}, never having played a videogame or " \
                        f"watched a movie in {self.hisher} life, grabs the amulet without a second thought."
                else:
                    if self.inj:
                        self.inj = False
                        return f"{t1} chances upon some medicinal herbs and applies it on {self.hisher} wounds."
                    else:
                        self.supplies = 'herbs'
                        return f"{t1} chances upon some medicinal herbs and decides to collect some for later use."
            elif scenario < 8 and self.weapon is None:
                new_weapon = random.choice(weapon_list)
                self.weapon = new_weapon
                return f"{t1} finds a {new_weapon} while scavenging through {random.choice(['a shed', 'a warehouse', 'some bushes'])}."
            elif scenario < 10 and self.weapon is None:
                new_weapon = random.choice(weapon_list)
                self.weapon = new_weapon
                return f"{t1} receives a supply drop containing a {new_weapon} from an unknown sponsor."
            elif scenario == 10:
                new_weapon = random.choice(rare_weapons_list)
                self.weapon = new_weapon
                if new_weapon == 'cursed sword':
                    return f"After a lengthy set of obstacles and puzzles in an ancient stone temple, {t1} finally reaps" \
                        f" the reward for {self.hisher} effort; a {new_weapon}, embedded with unimaginable power."
                elif new_weapon == 'gun':
                    return  f"Breaking through a hidden safe with {self.hisher} 1337 technical skills " \
                        f"({self.heshe} used a hammer), {t1} finds a {new_weapon} stored compactly inside."
            else:
                return f"{t1} tests out {self.hisher} {self.weapon} against " \
                    f"{random.choice(['some wild boars', 'a scarecrow', 'an odd-looking boulder', 'an effigy of Donald Trump'])}."

        elif num >= 2: # environment encounter
            scenario = random.randint(0,24)

            if scenario == 0:
                return f"{t1} picks some flowers."
            elif scenario == 1:
                return f"{t1} thinks about home."
            elif scenario == 2:
                self.inj = True
                return f"{t1} tries to eat something inedible and regrets it."
            elif scenario == 3:
                self.inj = True
                return f"{t1} tries some wild mushrooms hoping to get high, but all {self.heshe} gets is a bad case of diarrhea."
            elif scenario == 4:
                return f"{t1} tries some wild mushrooms and lucks out; {self.heshe} spends the rest of the day " \
                    f"tripping on shrooms."
            elif scenario == 5:
                return f"{t1} starts talking to {self.himher}self."
            elif scenario == 6:
                return f"{t1} steps in something indescribable."
            elif scenario == 7:
                temp = random.randint(0, 10)
                if temp == 10:
                    kill(self)
                    return f"{t1} dies of dysentery after drinking unboiled river water. This is wilderness survival 101" \
                        f" folks, jeez."
                else:
                    return f"{t1} finds a river and decides to stick close to it."
            elif scenario == 8:
                temp = random.randint(0, 10)
                if temp != 6:
                    self.inj = True
                    return f"{t1} gets bit by a savage bunny with a british accent."
                else:
                    kill(self)
                    return f"{t1} gets murdered by a savage bunny with a british accent."
            elif scenario == 9:
                kill(self)
                return f"{t1} steps on a landmine and gets yeeted into the stratosphere."
            elif scenario == 10:
                kill(self)
                return f"{t1} chances upon a small book simply titled 'Breaking Bad Coworker's Journal'. After reading a" \
                    f" couple pages, {self.heshe} promptly decides to jump off a cliff and commit suicide."
            elif scenario == 11:
                self.inj = True
                return f"{t1}'s dumb ass falls into a hole and breaks {self.hisher} leg."
            elif scenario == 12:
                return f"{t1} carves {self.hisher} initials into a tree."
            elif scenario == 13:
                return f"{t1} ponders the human condition."
            elif scenario == 14:
                if len(dead) > 0:
                    temp = random.choice(dead)
                    return f"{t1} finds {temp.name}'s corpse."
                else:
                    return f"{t1} dreams about the time {self.heshe} wasn't stuck in some idiotic simulation of *hunger games*," \
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
                return f"{t1} thinks about all the fun {self.hesshes} had with {self.hisher} frie- oh wait, {t1}" \
                    f" doesn't have any. Whoops."
            elif scenario == 21:
                return f"{t1} can't find a decent source of water, and nearly gives in before remembering that one" \
                    f" Bear Grylls meme, and decides to drink {self.hisher} own piss. Fresh and hot."
            elif scenario == 22:
                if self.inj:
                    kill(self)
                    return f"{t1} is bit by a snake and dies, because no one ever told {self.himher} how to tie" \
                        f" a tourniquet."
                else:
                    self.inj = True
                    return f"{t1} is bit by a snake, but manages to wear off the poison."
            elif scenario == 23:
                if self.inj and self.weapon is None:
                    kill(self)
                    return f"{t1} accidentally awakens a sleeping bear in a cave, and gets mauled."
                else:
                    return f"{t1} accidentally awakens a sleeping bear in a cave, but {self.heshe} " \
                        f"{random.choice([f'channels {self.hisher} inner Takamura and KOs the beast in one strike.', 'talks it down and has a nice little tea party.', 'asserts dominance by pissing on it.'])}"
            elif scenario == 24:
                kill(self)
                return f"{t1} tries to take a bath in a lake but gets eaten by a stealthy crocodile instead."
    def pick_random_night_action(self):
        global tributes, dead, deadthisday

        t1 = self.name

        # no party scenarios because fuck you
        other_tributes = [trib for trib in tributes if not trib.done and type(trib) != Party]
        if len(other_tributes) == 0:
            tribute2 = None
            scenario = random.randint(2, 25)  # skip tribute encounter scenarios
        else:
            scenario = random.randint(0, 25)
            tribute2 = random.choice(other_tributes)
            t2 = tribute2.name

        if self.supplies == 'weird amulet':  # weird amulet has custom outcomes
            temp = random.randint(0, 2)
            if temp == 0:  # continue onward as if nothing happened at all
                pass
            elif temp == 1:
                self.supplies = None
                self.weapon = 'cursed sword'
                return f"{t1} fiddles around with {self.hisher} weird amulet, and in a sudden puff of purple smoke, " \
                    f"it transforms into a cursed sword."
            elif temp == 2:
                self.supplies = None
                kill(self)
                return f"{t1} tries to get some sleep, when in a sudden puff of smoke, {self.hisher} weird amulet" \
                    f" randomly summons a winged monstrosity that dismembers {t1} before flying off into the night sky."

        elif self.inj and self.supplies is not None:
            if self.supplies == 'medkit':
                self.inj = False
                self.supplies = None
                return f"{t1} patches up {self.hisher} injuries using a medkit {self.heshe} had grabbed along the" \
                    f"way."
            elif self.supplies == 'herbs':
                self.inj = False
                self.supplies = None
                return f"{t1} patches up {self.hisher} injuries using the medicinal herbs {self.heshe} had " \
                    f"collected along the way."

        # Isolate trib encounter scenarios
        if scenario == 0 or scenario == 1:
            if scenario == 0:
                tribute2.done = True
                if tribute2.asleep:
                    kill(tribute2)
                    self.kills += 1
                    return f"{t1} covetly sneaks up on and kills {t2} in {self.hisher} sleep."
                else:
                    if tribute2.weapon is not None:
                        self.inj = True
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
                self.asleep = True
                return f"{t1} cries {self.himher}self to sleep."
            elif scenario == 3:
                self.inj = True
                return f"{t1} walks around in circles, unable to sleep."
            elif scenario == 4:
                self.asleep = True
                return f"{t1} uses {self.hisher} survival skills that {self.heshe} learned from watching Bear Grylls " \
                    f"24/7 and makes a shelter out of sticks and leaves to sleep in."

            elif scenario == 5:
                self.asleep = True
                return f"{t1} falls asleep on a makeshift bed of leaves."
            elif scenario == 6:
                temp = random.randint(0, 1)
                if self.inj:
                    kill(self)
                    return f"While looking for shelter, {t1} trips and falls onto some sharp rocks and bleeds out."
                else:
                    if temp == 1:
                        self.inj = True
                        return f"{t1} trips on some sharp rocks and gets knocked unconscious."
                    else:
                        self.asleep = True
                        return f"{t1} trips on some rocks, and then decides to sleep there."
            elif scenario == 7:
                temp = random.randint(0, 15)
                if temp == 1:
                    kill(self)
                    return f"{t1} sees a bleak future even with victory, and kills {self.himher}self."
                else:
                    self.asleep = True
                    return f"{t1} falls asleep in a flower patch."
            elif scenario == 8:
                self.asleep = True
                return f"{t1} falls asleep pondering the human condition."
            elif scenario == 9:
                self.asleep = False
                return f"{t1} stays awake all night as {self.hisher} brain tortures {self.himher} with memories of " \
                    f"that one awkward moment {self.heshe} had 3 years ago."
            elif scenario == 10:
                choice = random.choice(['shadowboxing all night due to recently having watched Hajime no Ippo',
                                        'spiking all night due to recently having watched Haikyuu'])
                return f"{t1} practices {self.hisher} {choice}."
            elif scenario == 11:
                if self.inj:
                    kill(self)
                    return f"{t1} gets bit by a bat and dies."
                else:
                    self.inj = True
                    return f"{t1} gets bit by a bat."
            elif scenario == 12:
                return f"{t1} makes a campfire and reminisces about the good ol' days."
            elif scenario == 13:
                return f"{t1} spots a bear sitting on a tree. It looks at {self.himher}, {self.heshe} looks at it," \
                    f" and then {t1} skedaddles on out of there."
            elif scenario == 14:
                self.asleep = True
                return f"{t1} falls asleep in a ditch."
            elif scenario == 15:
                return f"{t1} sleeps with one eye open."
            elif scenario == 16:
                self.asleep = True
                return f"{t1} has nightmares about that one NTR ugly bastard doujin {self.heshe} read long ago."
            elif scenario == 17:
                self.asleep = True
                return f"{t1} falls asleep admiring the beauty of the star-lit sky."
            elif scenario == 18:
                self.asleep = True
                return f"{t1} dreams about {self.himher}self as the victor."
            elif scenario == 19:
                if self.weapon is not None:
                    return f"{t1} admires {self.hisher} {self.weapon} under the light of {self.hisher} campfire."
                else:
                    weapon = random.choice(['axe', 'dagger', 'cleaver'])
                    self.weapon = weapon
                    return f"{t1} remembers that one Primitive Technology video {self.heshe} saw and fastens a makeshift " \
                        f"{weapon} from a stick and a sharpened rock."
            elif scenario == 20:
                return f"{t1} prays to God, and asks Him to let {self.himher} survive for another day. God tells " \
                    f"{t1} to shut the FUCK UP I'M TRYIN TO WATCH SOME GUNDAM HERE"
            elif scenario == 21:
                if self.gender.lower() == "m":
                    return f"{t1} jacks off in a nearby bush to relieve steam and accidentally summons a demon when he moves " \
                        f"his penis in a special pattern."
                else:
                    return f"{t1} draws a face on a coconut and talks to it all night."
            elif scenario == 22:
                self.inj = True
                self.asleep = True
                return f"{t1} eats some wild berries for dinner and regrets it."
            elif scenario == 23:
                return f"{t1} questions {self.hisher} sanity."
            elif scenario == 24:
                return f"{t1} tries to cook some fish and sets the forest on fire."
            elif scenario == 25:
                self.inj = True
                return f"{t1} tries to cook some meat but sets {self.himher}self on fire instead."

    def pick_random_bloodbath_action(self):
        global tributes, dead, deadthisday

        t1 = self.name

        other_tributes = [trib for trib in tributes if not trib.done]
        if len(other_tributes) == 0:
            tribute2 = None
            num = 1  # skip tribute encounter scenarios
        else:
            num = random.randint(0, 1)
            tribute2 = random.choice(other_tributes)
            t2 = tribute2.name

        if num == 0:  # tribute encounter
            scenario = random.randint(0, 7)

            if scenario == 0:
                self.kills += 1
                self.inj = True
                kill(tribute2)
                return f"{t1} strangles {t2} after engaging in a fist fight, though {self.heshe} walks out with" \
                    f" substantial injuries {self.himher}self."

            elif scenario == 1:
                self.kills += 1
                kill(tribute2)
                return f"{t1} sets {t2} on fire with a molotov before running away."

            elif scenario == 2:
                self.kills += 1
                kill(tribute2)
                self.weapon = random.choice(weapon_list)
                return f"{t2} grabs a {self.weapon} and tries to take out {t1}, but {t1} displays {self.hisher}" \
                    f" god-level taijustsu skills and kicks the {self.weapon} out of {t2}'s hands, before killing" \
                    f" {t2} with {tribute2.hisher} own weapon."

            elif scenario == 3:
                other = [trib for trib in tributes if not trib.done and trib != tribute2]
                if len(other) >= 2:
                    trib3 = other[0]
                    t3 = trib3.name
                    trib4 = other[1]
                    t4 = trib4.name
                    temp = random.randint(1, 2)
                elif len(other) == 1:
                    trib3 = other[0]
                    t3 = trib3.name
                    temp = 1
                else:
                    temp = 0

                if temp == 2:
                    kill(trib3)
                    trib4.kills += 1
                    kill(trib4)
                    tribute2.kills += 1
                    kill(tribute2)
                    self.kills += 1
                    return f"{t1}, {t2}, {t3}, and {t4} get into a massive fight. {t2} skewers {t3} with a tree" \
                        f" branch, {t1} bashes {t4}'s head in with a rock, and after a vicious fight, {t1} triumphantly" \
                        f" dismembers {t2}."
                elif temp == 1:
                    kill(trib3)
                    kill(tribute2)
                    self.kills += 2
                    return f"{t1}, {t2}, and {t3} get into a fight. {t1} triumphantly kills them both."
                elif temp == 0:
                    return f"{t1} and {t2} for a bag. {t1} strangles {t2} with the straps and runs."

            elif scenario == 4:  # team up
                party = Party(self, tribute2)
                party.done = True
                choice = [f"{t1} grabs a jar of fishing bait, while {t2} gets fishing gear. They decide that it's fate,"
                          f" and team up.",
                          f"{t1} and {t2} decide to team up to increase their odds.",
                          f"{t1} and {t2}, while running away from the Cornucopia, accidentally jump into the same"
                          f" cave. Neither of them wants to fight, and so they decide to team up."]
                return random.choice(choice)
            elif scenario > 4:  # grab + kill
                self.weapon = random.choice(weapon_list)  # it's christmas, boys
                if self.weapon in cleavers:
                    self.kills += 1
                    kill(tribute2)
                    return f"{t1} wedges free a {self.weapon} stuck on a podium and uses it to cut down {t2} in a" \
                        f" single stroke."
                elif self.weapon in stabbers:
                    self.kills += 1
                    kill(tribute2)
                    return f"{t1} picks up a {self.weapon} sticking up in the ground and slits {t2}'s throat."
                elif self.weapon in clubbers:
                    self.kills += 1
                    kill(tribute2)
                    if len(deadthisday) > 0:
                        temp = random.choice(deadthisday)
                        return f"{t1} grabs a {self.weapon} lying near {temp.name}'s corpse and bashes {t2}'s skull" \
                            f" in with it."
                    else:
                        return f"{t1} grabs a {self.weapon} lying near a dead tribute's corpse and bashes {t2}'s" \
                            f" skull in with it."

                elif self.weapon == 'bow' or self.weapon == 'blowdart':
                    tribute2.kills += 1
                    tribute2.weapon = self.weapon
                    kill(self)
                    return f"{t1} grabs a backpack and finds a {self.weapon}, but before {self.heshe} can react," \
                        f" {t2} punches {self.himher} down and strangles {self.himher} to death, before stealing" \
                        f" the {self.weapon}."

        elif num == 1:  # supply/weapon encounter
            scenario = random.randint(0, 3)
            if scenario == 0:
                self.weapon = random.choice(weapon_list)
                choice = random.choice([f'wedges free a {self.weapon} stuck on a podium',
                                        f'grabs a {self.weapon} sticking up in the ground',
                                        f"grabs a {self.weapon} safely enclosed in a backpack"])
                return f"{t1} {choice} and swings it around once or twice to ward off other tributes, before" \
                    f" running away from the Cornucopia as fast as {self.heshe} can."
            elif scenario == 2:
                self.supplies = 'medkit'
                choice = random.choice(['hidden behind a podium', "lying on the ground"])
                return f"{t1} manages to grab a medkit {choice} and runs away from the Cornucopia as fast as" \
                    f" {self.heshe} can."
            else:
                subchoice = random.choice(['K-ON', 'Haikyuu', 'Hyouka', 'TTGL', 'Eromanga Sensei', 'Penguindrum',
                                           'Made in Abyss', 'Highschool DxD', 'Ouran Koukou Host Club'])
                choices = [f"{t1}, fearing for {self.hisher} life, doesn't stop to grab any supplies and instead"
                           f" simply runs into a nearby forest as fast as {self.heshe}.",
                           f"{t1} grabs some food and a canteen of water, before running away from the Cornucopia as"
                           f" fast as {self.heshe} can.",
                           f"{t1} spots a {subchoice} Premium Box Set, and {self.hisher} degeneracy compels"
                           f" {self.himher} to grab it the first chance {self.heshe} gets.",
                           f"{t1} grabs a backpack and runs for it, not realizing the backpack is empty."]
                return random.choice(choices)


class Party:

    def __init__(self, tribute1, tribute2, tribute3=None):
        global tributes
        self.trib1 = tribute1
        self.trib2 = tribute2
        self.trib3 = tribute3

        tributes.remove(self.trib1)
        tributes.remove(self.trib2)
        tributes.insert(0, self)

        self.t1 = tribute1.name
        self.t2 = tribute2.name

        if tribute3 is not None:
            tributes.remove(self.trib3)
            self.t3 = tribute3.name
            self.type = 3
        else:
            self.type = 2

        self.done = False

    def split(self):
        global tributes
        tributes.insert(0, self.trib1)
        tributes.insert(0, self.trib2)
        if self.type == 3:
            tributes.insert(0, self.trib3)
        tributes.remove(self)

    def calculate_strength(self):
        score = self.trib1.calculate_strength()
        score += self.trib2.calculate_strength()
        if self.type == 3:
            score += self.trib3.calculate_strength()
        return score

    def add_tribute(self, tribute3):
        self.trib3 = tribute3
        tributes.remove(self.trib3)
        self.t3 = tribute3.name
        self.type = 3

    def pick_random_action(self):
        trib1 = self.trib1
        trib2 = self.trib2
        t1 = self.trib1.name
        t2 = self.trib2.name

        other_tributes = [trib for trib in tributes if not trib.done]
        if len(other_tributes) == 0:
            othertrib= None
            num = random.randint(1, 5)
        else:
            num = random.randint(0, 5)
            othertrib = random.choice(other_tributes)

        if self.type == 2:
            # check if these two chucklefucks are the only tributes alive
            if len(tributes) == 1:
                scenario = random.randint(0, 2)
                if scenario == 0:
                    kill(trib1, self)
                    kill(trib2)
                    return f"As the game comes down to it's final day, {t1} and {t2} contemplate on what they should do." \
                        f" In the end, their bond is too strong; They try and pull the good ol' berry trick but " \
                        f"the producers ain't having it and the game ends a tragedy."
                else:
                    output = f"As the game comes down to it's final day, {t1} and {t2} both know what must be done. " \
                        f"They make their way to the Cornucopia, and get ready for the final showdown.\n"

                    strong, weak, even = compare_strength(trib1, trib2)

                    str = strong.name
                    wk = weak.name

                    if strong.weapon == 'cursed sword':
                        kill(strong, self)
                        output += f"As the fight starts, a purple light fills the sky as {str}'s cursed sword shatters and reveals it's " \
                            f"final form: A giant fucking Gundam emerges from the blinding light. Because of course it does.\n" \
                            f" As {str} prepares to become one with the robot, {strong.heshe} bids {wk} a final farewell" \
                            f" before flying off to the stars. {wk} just stands there amazed."
                        strong.name = 'Ascended ' + strong.name
                    elif weak.weapon == 'cursed sword':
                        kill(weak, self)
                        output += f"As the fight starts, a purple light fills the sky as {wk}'s cursed sword shatters and reveals it's " \
                            f"final form; A giant fucking Gundam emerges from the blinding light. Because of course it does.\n" \
                            f" As {wk} prepares to become one with the robot, {weak.heshe} bids {str} a final farewell" \
                            f" before flying off to the stars. {str} just stands there amazed."
                        strong.name = 'Ascended ' + weak.name

                    elif strong.weapon == 'gun' or weak.weapon == 'gun':
                        if strong.weapon == 'gun':
                            strong.kills += 1
                            kill(weak, self)
                            output += f"{str} just straights up shoots {wk} in the head with {strong.hisher} gun." \
                                f" Kind of anticlimactic really."
                        elif weak.weapon == 'gun':
                            weak.kills += 1
                            kill(strong, self)
                            output += f"{wk} just straights up shoots {str} in the head with {weak.hisher} gun." \
                                f" Kind of anticlimactic really."

                    elif strong.weapon in cleavers:
                        strong.kills += 1
                        kill(weak, self)
                        if scenario > 7:
                            output += f"After a long battle, {str} savagely decapitates {wk} with {strong.hisher} {strong.weapon}."
                        else:
                            output += f"{str}, without hesitation, cuts {wk} down with {strong.hisher} {strong.weapon} in a single stroke."

                    elif strong.weapon in stabbers:
                        strong.kills += 1
                        kill(weak, self)
                        if scenario > 7:
                            output += f"A final, well aimed stab by {str}'s {strong.weapon} ends {wk}'s life."
                        else:
                            output += f"After a drawn-out fight, {str} manages to catch {wk} in the throat with {strong.hisher}" \
                                f" {strong.weapon} and ends {wk}'s life."

                    elif strong.weapon in clubbers:
                        strong.kills += 1
                        kill(weak, self)
                        output += f"A ferocious battle commences, and {str} eventually smashes {wk}'s head in with " \
                            f"{strong.hisher} {strong.weapon}."

                    elif strong.weapon == 'bow' or strong.weapon == 'blowdart':
                        if strong.weapon == 'bow':
                            strong.kills += 1
                            kill(weak, self)
                            output += f"After a tactical battle of wits fully utilizing their surroundings, {str} finally " \
                                f"figures out where {wk} is hiding and manages to catch {weak.himher} in the throat with" \
                                f"an arrow."
                        if strong.weapon == 'blowdart':
                            strong.kills += 1
                            kill(weak, self)
                            output += f"After a tactical battle of wits fully utilizing their surroundings, {str} finally " \
                                f"figures out where {wk} is hiding and shoots out a poisoned dart. It barely pricks {wk}'s" \
                                f"skin, but it's enough: {weak.heshe} collapses soon after."
                    else:
                        kill(weak, self)
                        kill(strong)
                        output += f"In a magnificent display of manliness, {str} and {wk} fight it out to the death with " \
                            f"their fists, and in the end simultaneously collapse."
                    return output

            # 2v1 is always going to be unfair
            if num == 0:
                return sorting_hat(self, othertrib)

            # Time for us to follow our own paths, Kenny
            elif num == 1:
                scenario = random.randint(0, 2)

                self.split()

                if scenario == 0:
                    return f"{t1} and {t2} decide to split up and go their own ways in amicable terms while they still can."
                elif scenario == 1:
                    return f"{t1} and {t2} decide to split up to hunt for food. {t2} manages to snag a wild boar and " \
                        f"makes {trib2.hisher} way towards the rendezvous point, but {t1} is nowhere to be found.\n" \
                        f"{t1}, while chasing a rabbit, goes a little bit too far into the forest and finds " \
                        f"{trib1.himher}self lost in a labyrinth of trees."
                elif scenario == 2:
                    choice = random.choice([f'It contains simple words of farewell, fitting for {t2}.',
                                            'It contains a single word scrawled out with fresh ink - Goodbye.',
                                            f"It contains a heartfelt message thanking {t1} for their friendship.",
                                            f"Oh wait, it isn't a note, just the tissue that {t2} used for "
                                            f"{trib2.hisher} 'stress relief session' last night. Yikes."])
                    return f"{t1} wakes up at dawn to find {t2} missing, and a note left behind; {choice}"

            # This God *does* play dice
            else:
                scenario = random.randint(0, 19)

                if scenario == 0:
                    return f"{t1} and {t2} hunt {random.choice(['boars', 'deers', 'rabbits'])} together."
                elif scenario == 1:
                    return f"{t1} and {t2} hunt for other tributes."
                elif scenario == 2:
                    trib1.inj = True
                    return f"{t1} falls in a ditch and {t2} laughs {trib2.hisher} ass off while helping {t1} up."
                elif scenario == 3:
                    if trib1.inj and trib2.inj:
                        kill(trib1, self)
                        kill(trib2)
                        return f"{t1} and {t2} both get killed by a giant bat while exploring a dark cave."
                    else:
                        return f"{t1} and {t2} take down a giant bat while exploring a dark cave."
                elif scenario == 4:
                    trib1.inj = False
                    trib2.inj = False
                    return f"{t1} and {t2} chance upon a magical hot springs, and a quick bath rejuvenates them both."
                elif scenario == 5:
                    return f"{t1} and {t2} pool their shroom knowledge together and manage to isolate and collect the ones " \
                        f"that actually get you high; They spend the rest of the day tripping on shrooms."
                elif scenario == 6:
                    return f"{t1} and {t2} split up to look for supplies."
                elif scenario == 7:
                    if trib1.weapon is not None or trib2.weapon is not None:
                        return f"{t1} and {t2} fend off a sudden attack by a savage bunny with a british accent."
                    else:
                        injured = random.choice([trib1, trib2])
                        injured.inj = True
                        return f"{t1} and {t2} fend off a sudden attack by a savage bunny with a british accent, but" \
                            f" {injured.name} is wounded in the process."
                elif scenario == 8:
                    return f"{t2} almost steps on a landmine before {t1} pulls {trib2.himher} out of the way."
                elif scenario == 9:
                    weapon = random.choice(weapon_list)
                    if trib1.weapon is None and trib2.weapon is None:
                        temp = random.randint(0, 5)
                        if temp == 0:
                            trib1.weapon = weapon
                            trib2.weapon = weapon
                            return f"{t1} and {t2} find a chest with a {weapon} inside, and bicker over who gets to keep it," \
                                f" before finding another one hidden behind the chest."
                        elif temp < 5:
                            if temp < 3:
                                trib1.weapon = weapon
                                return f"{t1} and {t2} find a {weapon} lying around, and bicker over who gets to keep it," \
                                    f" before {t2} gives in and lets {t1} hold on to it."
                            else:
                                trib2.weapon = weapon
                                return f"{t1} and {t2} find a {weapon} lying around, and bicker over who gets to keep it," \
                                    f" before {t1} gives in and lets {t2} hold on to it."
                        elif temp == 5:
                            if trib1.inj:
                                trib1.kills += 1
                                trib1.weapon = weapon
                                kill(trib2, self)
                                return f"{t1} and {t2} find a {weapon} lying around, and an argument over who gets to keep" \
                                    f" it heats up into a fight; {t1} ends up bashing {t2}'s skull in."
                            else:
                                trib2.kills += 1
                                trib2.weapon = weapon
                                kill(trib1, self)
                                return f"{t1} and {t2} find a {weapon} lying around, and an argument over who gets to keep" \
                                    f" it heats up into a fight; {t2} ends up bashing {t1}'s skull in."
                    elif trib1.weapon is None:
                        trib1.weapon = weapon
                        choice = random.choice(['scavenging in a shed', 'exploring a derelict mansion',
                                                'looting an oddly-placed chest'])
                        return f"{t1} and {t2} find a {weapon} while {choice}, and {t1} takes a liking to it."
                    elif trib2.weapon is None:
                        trib2.weapon = weapon
                        choice = random.choice(['scavenging in a shed', 'exploring a derelict mansion',
                                                'looting an oddly-placed chest'])
                        return f"{t1} and {t2} find a {weapon} while {choice} and {t2} takes a liking to it."
                    else:
                        choice = random.choice(['a derelict mansion', 'a bamboo forest',
                                                'a dark cave'])
                        return f"{t1} and {t2} spend the day exploring {choice} but finds nothing of interest."
                elif scenario == 10:
                    if len(dead) > 0:
                        temp = random.choice(dead)
                        return f"{t1} and {t2} find {temp.name}'s corpse while exploring."
                    else:
                        return f"{t1} tries to catch a rabbit by chasing it while {t2} lays a trap for it; neither are" \
                            f"successful in their endeavours."
                elif scenario == 11:
                    if trib1.supplies is None:
                        trib1.supplies = 'medkit'
                    if trib2.supplies is None:
                        trib2.supplies = 'medkit'
                    trib1.inj = False
                    trib2.inj = False
                    return f"{t1} and {t2} chance upon a warehouse full of medical supplies."
                elif scenario == 12:
                    return f"{t1} and {t2} can't find a decent source of water before they remember that one Bear Grylls meme," \
                        f" and they decide that watersports isn't all that degenerate of a kink anyway."
                elif scenario == 13:
                    return f"{t1} and {t2} find a river and decide to do some fishing; {t1} stumbles around without catching anything" \
                        f" at all while {t2} catches buttloads with {trib2.hisher} secret fishing technique passed down the" \
                        f" generations."
                elif scenario == 14:
                    return f"{t1} and {t2} find a mysterious book simply labeled 'Breaking Bad Coworker's Journal'. {t1} goes to" \
                        f" read it but {t2} senses something very wrong and stops {t1} before {trib1.heshe} opens it."
                elif scenario == 15:
                    choice = random.choice(['Darling in the Franxx', 'Eromanga Sensei', 'Sword Art Online', 'Shobitch',
                                            'Sakurasou'])
                    return f"{t1} throws a rock at {t2}'s head when {trib2.heshe} reveals that {trib2.heshe} gave" \
                        f" {choice} a 10 on MAL."
                elif scenario == 16:
                    trib1.inj = True
                    trib2.inj = True
                    return f"{t2} stands in the rain for 0.2 nanoseconds and catches a bad cold; {trib2.heshe} spreads " \
                        f"it to {t1} too."
                elif scenario == 17:
                    if trib1.weapon is not None or trib2.weapon is not None:
                        trib1.inj = True
                        trib2.inj = True
                        return f"{t1} and {t2} accidentally awaken a sleeping bear in a cave, but they manage to fight it off."
                    elif trib1.inj or trib2.inj:
                        kill(trib1, self)
                        kill(trib2)
                        return f"{t1} and {t2} accidentally awaken a sleeping bear in a cave, and they both get mauled."
                    else:
                        return f"{t1} and {t2} accidentally awaken a sleeping bear in a cave, but they both manage to escape."
                elif scenario == 18:
                    if trib1.inj:
                        kill(trib1, self)
                        return f"{t1} accidentally steps on a snake and gets bitten. Despite {t2}'s best efforts," \
                            f" {trib1.heshe} dies of venom a few hours later."
                    else:
                        trib1.inj = True
                        return f"{t1} accidentally steps on a snake and gets bitten. {t2} helps {trib1.himher} through" \
                            f" the ordeal and {t1} manages to mostly wear the venom off."
                elif scenario == 19:
                    choice = random.choice(['an enraged bull', 'a territorial rhino', 'a pack of wolves'])
                    if trib2.inj:
                        kill(trib2, self)
                        return f"{t1} and {t2} accidentally end up walking right in front of {choice}, and while" \
                            f" {t1} manages to escape unscathed, {t2} isn't quite as lucky."
                    else:
                        trib2.inj = True
                        return f"{t1} and {t2} accidentally end up walking right in front of {choice}, and while they" \
                            f" both manage to escape in one piece, {t2}'s {random.choice(['right', 'left'])}" \
                            f" {random.choice(['leg', 'arm'])} ain't lookin' that hot."

        elif self.type == 3:
            trib3 = self.trib3
            t3 = trib3.name
            # check if these three chucklefucks are the only tributes alive
            if len(tributes) == 1:
                self.split()
                return f"All three having realized what predicament they are in, {t1}, {t2}, and {t3} silently split" \
                    f" up and head out their own way at the break of dawn. They promises to meet again soon, though" \
                    f" not as friends."

            # FIGHT! FIGHT! FIGHT!
            if num == 0:
                return sorting_hat(self, othertrib)

            # Time for us to follow our own paths, Kenny
            elif num == 1:
                scenario = random.randint(0, 2)
                self.split()

                if scenario == 0:
                    return f"{t1}, {t2} and {t3} decide to split up and go their own ways in amicable terms while they" \
                        f" still can."
                elif scenario == 1:
                    return f"{t1}, {t2} and {t3} decide to split up to hunt for food. {t2} manages to snag a wild" \
                        f" boar and makes {trib2.hisher} way towards the rendezvous point, but {t1} and {t3} are" \
                        f" nowhere to be found.\n{t1}, while chasing a rabbit, goes a little bit too far into the" \
                        f" forest and finds {trib1.himher}self lost in a labyrinth of trees.\n{t3} jumps into a dark" \
                        f" cave and gets caught up in an epic fight with a giant spider."
                elif scenario == 2:
                    Party(trib1, trib2)
                    choice = random.choice([f'It contains simple words of farewell, fitting for {t3}.',
                                            'It contains a single word scrawled out with fresh ink - Goodbye.',
                                            f"It contains a heartfelt message thanking {t1} and {t2} for their"
                                            f" friendship and support.",
                                            f"Oh wait, it isn't a note, just the tissue that {t3} used for "
                                            f"{trib3.hisher} 'stress relief session' last night. Yikes."])
                    return f"{t1} and {t2} wake up at dawn to find {t3} missing, and a note left behind; {choice}"

            # This God *does* play dice
            else:
                scenario = random.randint(0, 20)

                if scenario == 0:
                    return f"{t1}, {t2} and {t3} hunt {random.choice(['boars', 'deers', 'rabbits'])} together."
                elif scenario == 1:
                    return f"{t1}, {t2} and {t3} hunt for other tributes."
                elif scenario == 2:
                    trib1.inj = True
                    return f"{t1} falls in a ditch while {t2} and {t3} laughs their asses off."
                elif scenario == 3:
                    if trib1.inj and trib2.inj and trib3.inj:
                        kill(trib1, self)
                        kill(trib2)
                        kill(trib3)
                        return f"{t1}, {t2} and {t3} all get killed by a giant bat while exploring a dark cave."
                    else:
                        return f"{t1}, {t2} and {t3} take down a giant bat while exploring a dark cave."
                elif scenario == 4:
                    trib1.inj = False
                    trib2.inj = False
                    trib3.inj = False
                    return f"{t1}, {t2} and {t3} chance upon a magical hot springs, and a quick bath rejuvenates all" \
                        f" three."
                elif scenario == 5:
                    return f"{t1}, {t2} and {t3} pool their shroom knowledge together and manage to isolate and" \
                        f" collect the ones that actually get you high; They spend the rest of the day tripping on" \
                        f" shrooms."
                elif scenario == 6:
                    return f"{t1}, {t2} and {t3} split up to look for supplies."
                elif scenario == 7:
                    if self.calculate_strength() > 5:
                        return f"{t1} and {t2} fend off a sudden attack by a savage bunny with a british accent."
                    else:
                        injured = random.choice([trib1, trib2, trib3])
                        injured.inj = True
                        return f"{t1}, {t2} and {t3} fend off a sudden attack by a savage bunny with a british" \
                            f" accent, but {injured.name} is wounded in the process."
                elif scenario == 8:
                    return f"{t2} almost steps on a landmine before {t1} and {t3} pull {trib2.himher} out of the way."
                elif scenario == 9:
                    weapon = random.choice(weapon_list)
                    if trib1.weapon is None and trib2.weapon is None and trib3.weapon is None:
                        temp = random.randint(0, 5)
                        if temp == 0:
                            trib1.weapon = weapon
                            trib2.weapon = weapon
                            return f"{t1}, {t2} and {t3} find a chest with a {weapon} inside, and bicker over who gets" \
                                f" to keep it, before finding two more ones hidden behind the chest."
                        elif temp < 5:
                            temp = random.randint(0, 2)
                            if temp == 0:
                                trib1.weapon = weapon
                                return f"{t1}, {t2} and {t3} find a {weapon} lying around, and they play" \
                                    f" rock-paper-scissors to decide who gets to keep it. {t1} pulls out his inner" \
                                    f" Tokuchi, and obliterates {t2} and {t3}, earning the {weapon} in the process."
                            elif temp == 1:
                                trib2.weapon = weapon
                                return f"{t1}, {t2} and {t3} find a {weapon} lying around, and they play" \
                                    f" rock-paper-scissors to decide who gets to keep it. {t2} pulls out his inner" \
                                    f" Tokuchi, and obliterates {t1} and {t3}, earning the {weapon} in the process."
                            elif temp == 2:
                                trib3.weapon = weapon
                                return f"{t1}, {t2} and {t3} find a {weapon} lying around, and they play" \
                                    f" rock-paper-scissors to decide who gets to keep it. {t3} pulls out his inner" \
                                    f" Tokuchi, and obliterates {t1} and {t2}, earning the {weapon} in the process."

                        elif temp == 5:
                            if not trib1.inj:
                                trib1.kills += 2
                                trib1.weapon = weapon
                                kill(trib2, self)
                                kill(trib3)
                                return f"{t1}, {t2} and {t3} find a {weapon} lying around, and an argument over who" \
                                    f" gets to keep it heats up into a fight; {t1} ends up bashing {t2}'s skull in," \
                                    f" and leaves a wounded {t3} to die."
                            elif not trib2.inj:
                                trib2.kills += 2
                                trib2.weapon = weapon
                                kill(trib1, self)
                                kill(trib3)
                                return f"{t1}, {t2} and {t3} find a {weapon} lying around, and an argument over who" \
                                    f" gets to keep it heats up into a fight; {t2} ends up bashing {t1}'s skull in," \
                                    f" and leaves a wounded {t3} to die."
                            else:
                                trib3.kills += 2
                                trib3.weapon = weapon
                                kill(trib1, self)
                                kill(trib2)
                                return f"{t1}, {t2} and {t3} find a {weapon} lying around, and an argument over who" \
                                    f" gets to keep it heats up into a fight; {t3} ends up bashing {t1}'s skull in," \
                                    f" and leaves a wounded {t2} to die."
                    elif trib1.weapon is None:
                        trib1.weapon = weapon
                        choice = random.choice(['scavenging in a shed', 'exploring a derelict mansion',
                                                'looting an oddly-placed chest'])
                        return f"{t1}, {t2} and {t3} find a {weapon} while {choice}, and {t1} takes a liking to it."
                    elif trib2.weapon is None:
                        trib2.weapon = weapon
                        choice = random.choice(['scavenging in a shed', 'exploring a derelict mansion',
                                                'looting an oddly-placed chest'])
                        return f"{t1}, {t2} and {t3} find a {weapon} while {choice} and {t2} takes a liking to it."
                    elif trib3.weapon is None:
                        trib3.weapon = weapon
                        choice = random.choice(['scavenging in a shed', 'exploring a derelict mansion',
                                                'looting an oddly-placed chest'])
                        return f"{t1}, {t2} and {t3} find a {weapon} while {choice} and {t3} takes a liking to it."
                    else:
                        choice = random.choice(['a derelict mansion', 'a bamboo forest',
                                                'a dark cave'])
                        return f"{t1}, {t2} and {t3} spend the day exploring {choice} but finds nothing of interest."
                elif scenario == 10:
                    if len(dead) > 0:
                        temp = random.choice(dead)
                        return f"{t1}, {t2} and {t3} find {temp.name}'s corpse while exploring."
                    else:
                        return f"{t1} tries to catch a rabbit by chasing it while {t2} lays a trap for it, and {t3}" \
                            f" just hides in a tree hopping to get the drop on it; all three are unsuccessful in" \
                            f" their endeavours."
                elif scenario == 11:
                    if trib1.supplies is None:
                        trib1.supplies = 'medkit'
                    if trib2.supplies is None:
                        trib2.supplies = 'medkit'
                    if trib3.supplies is None:
                        trib3.supplies = 'medkit'
                    trib1.inj = False
                    trib2.inj = False
                    trib3.inj = False
                    return f"{t1}, {t2} and {t3} chance upon a warehouse full of medical supplies."
                elif scenario == 12:
                    return f"{t1}, {t2} and {t3} can't find a decent source of water before they remember that one" \
                        f" Bear Grylls meme, and they decide that watersports isn't all that degenerate of a kink" \
                        f" anyway."
                elif scenario == 13:
                    return f"{t1}, {t2} and {t3} find a river and decide to do some fishing. {t1} stumbles around" \
                        f" without catching anything at all. {t2} catches buttloads with {trib2.hisher} secret" \
                        f" fishing technique passed down the generations. {t3} becomes one with the water, and ends" \
                        f" up catching even more fish than {t2}, but ends up tripping over the bucket and sets all" \
                        f" {trib3.hisher} catches free."
                elif scenario == 14:
                    return f"{t1}, {t2} and {t3} find a mysterious book simply labeled 'Breaking Bad Coworker's" \
                        f" Journal'. {t1} goes to read it but {t3} senses something very wrong and stops {t1} before" \
                        f" {trib1.heshe} opens it."
                elif scenario == 15:
                    choice = random.choice(['Darling in the Franxx', 'Eromanga Sensei', 'Sword Art Online', 'Shobitch',
                                            'Sakurasou'])
                    return f"{t1} and {t3} throw rocks at {t2}'s head when {trib2.heshe} reveals that {trib2.heshe} gave" \
                        f" {choice} a 10 on MAL."
                elif scenario == 16:
                    trib1.inj = True
                    trib2.inj = True
                    trib3.inj = True
                    return f"{t2} stands in the rain for 0.2 nanoseconds and catches a bad cold; {trib2.heshe} spreads " \
                        f"it to {t1} and {t3} too."
                elif scenario == 17:
                    strength = self.calculate_strength()
                    if strength > 6:
                        return f"{t1}, {t2} and {t3} accidentally awaken a sleeping bear in a cave, but they" \
                            f" manage to escape unharmed."
                    elif strength > 4:
                        trib1.inj = True
                        trib2.inj = True
                        trib3.inj = True
                        return f"{t1}, {t2} and {t3} accidentally awaken a sleeping bear in a cave, but they manage" \
                            f" to fight it off."
                    else:
                        kill(trib1, self)
                        kill(trib2)
                        kill(trib3)
                        return f"{t1}, {t2} and {t3} accidentally awaken a sleeping bear in a cave, and they all" \
                            f" get mauled."
                elif scenario == 18:
                    if trib1.inj:
                        kill(trib1, self)
                        party = Party(trib2, trib3)
                        return f"{t1} accidentally steps on a snake and gets bitten. Despite {t2} and {t3}'s best" \
                            f" efforts, {t1} dies of venom a few hours later."
                    else:
                        trib1.inj = True
                        return f"{t1} accidentally steps on a snake and gets bitten. {t3} manages to find some" \
                            f" antivenom while {t2} helps {t1} through the ordeal and {t1} manages to mostly wear" \
                            f" the venom off."
                elif scenario == 19:
                    choice = random.choice(['an enraged bull', 'a territorial rhino', 'a pack of wolves'])
                    if trib2.inj:
                        kill(trib2, self)
                        party = Party(trib1, trib3)
                        return f"{t1}, {t2} and {t3} accidentally end up walking right in front of {choice}, and while" \
                            f" {t1} and {t2} manage to escape unscathed, {t2} isn't quite as lucky."
                    else:
                        trib2.inj = True
                        return f"{t1}, {t2} and {t3} accidentally end up walking right in front of {choice}, and while they" \
                            f" manage to escape in one piece, {t2}'s {random.choice(['right', 'left'])}" \
                            f" {random.choice(['leg', 'arm'])} ain't lookin' that hot."
                elif scenario == 20:
                    choice = random.choice(['gets caught by a bear trap',
                                            'accidentally steps on a hidden landmine',
                                            'is suddenly struck by lighting'])
                    if trib3.inj:
                        kill(trib3, self)
                        party = Party(trib1, trib2)
                        return f"{t3} {choice}. At death's door, and with no hope of survival, {t3} begs {t1} and" \
                            f" {t2} to end his suffering. {t1} looks away while {t2} puts {t3} out of" \
                            f" {trib3.hisher} misery."
                    else:
                        trib3.inj = True
                        return f"{t3} {choice}, but with the help of {t1} and {t2}, {trib3.heshe} amanges to survive"

    def pick_random_night_action(self):

        trib1 = self.trib1
        trib2 = self.trib2
        trib3 = self.trib3
        t1 = self.trib1.name
        t2 = self.trib2.name


        if self.type == 2:
            if trib1.supplies == 'weird amulet' or trib2.supplies == 'weird amulet':  # weird amulet has custom outcomes
                temp = random.randint(0, 2)
                if temp == 0: # continue onward as if nothing happened
                    pass
                elif temp == 1:
                    if trib1.supplies == 'weird amulet':
                        sworded = trib1
                    elif trib2.supplies == 'weird amulet':
                        sworded = trib2
                    sworded.supplies = None
                    sworded.weapon = 'cursed sword'
                    return f"{t1} and {t2} fiddle around with the weird amulet, and in a sudden puff of purple smoke, " \
                        f"it transforms into a cursed sword."
                elif temp == 2:
                    trib1.supplies = None
                    kill(trib1, self)
                    kill(trib2)
                    return f"{t1} and {t2} try to get some sleep, when in a sudden puff of smoke, the weird amulet" \
                        f" randomly summons a winged monstrosity that dismembers them both before flying off into the night sky."

            if trib1.inj:
                injured = trib1
                if trib1.supplies is not None:
                    supplier = trib1
                    helper = trib2
                elif trib2.supplies is not None:
                    supplier = trib2
                    helper = trib2
                else:
                    supplier = None
            elif trib2.inj:
                injured = trib2
                if trib1.supplies is not None:
                    supplier = trib1
                    helper = trib1
                elif trib2.supplies is not None:
                    supplier = trib2
                    helper = trib1
                else:
                    supplier = None
            else:
                injured = None
                supplier = None

            if injured is not None and supplier is not None:
                if supplier.supplies == 'medkit':
                    injured.inj = False
                    supplier.supplies = None
                    return f"{helper.name} tends to {injured.name}'s injuries using a medkit."
                elif supplier.supplies == 'herbs':
                    injured.inj = False
                    supplier.supplies = None
                    return f"{helper.name} tends to {injured.name}'s injuries using a some herbs {helper.heshe} had " \
                        f"grabbed along the way."

            scenario = random.randint(0, 12)
            if scenario == 0:
                trib1.asleep = True
                trib2.asleep = True
                return f"{t1} and {t2} tell old tales and bond over a campfire."
            elif scenario == 1:
                return f"{t1} and {t2} sleep in shifts throughout the night."
            elif scenario == 2:
                trib1.asleep = True
                trib2.asleep = True
                return f"{t1} and {t2} huddle up for warmth."
            elif scenario == 3:
                trib1.asleep = True
                trib2.asleep = True
                return f"{t1} discreetly and implicitly confesses {trib1.hisher} love to {t2}, but {t2} is " \
                    f"{random.choice(['denser than a black hole', 'as dense as a harem mc'])}, and never realizes it."
            elif scenario == 4:
                trib1.asleep = True
                trib2.asleep = True
                return f"{t1} and {t2} fall asleep admiring the beauty of the star-lit sky."
            elif scenario == 5:
                return f"{t1} and {t2} set up a campfire and cheerfully sing anime OPs all night."
            elif scenario == 6:
                trib2.asleep = True
                trib1.asleep = True
                return f"{t1} convinces {t2} to snuggle with {trib1.himher}."
            elif scenario == 7:
                trib2.asleep = True
                trib1.asleep = True
                return f"{t1} and {t2} reveal their deepest fears and insecurities to each other, and they cry themselves" \
                    f" to sleep while snuggling."
            elif scenario == 8:
                if trib1.gender.lower() == "m" and trib2.gender.lower() == "m":
                    return f"{t1} fucks {t2} in the ass all night but their balls don't touch so they both maintain" \
                        f" their heterosexuality."
                else:
                    choice = random.choice(['past trauma', f'{trib2.hisher} latent asexuality',
                                            f"{t1}'s fugly-ass face"])
                    return f"{t1} tries to make a move on {t2}, but {trib2.heshe} respectfully declines, citing" \
                        f" {choice}"
            elif scenario == 9:
                trib1.kills += 1
                kill(trib2, self)
                return f"{t1} reveals {trib1.hisher} true colors and murders {t2} in {trib2.hisher} sleep."
            elif scenario == 10:
                temp = random.randint(0, 2)
                if temp == 0:
                    return f"As {t1} and {t2} silently stare at the flickering campfire, {t2} pipes up:\n'Hey.'\n'Yeah?'" \
                        f"\n'You ever wonder why we're here?'\n'It’s one of life’s great mysteries isn't it? Why are we here?" \
                        f" I mean, are we the product of some cosmic coincidence, or is there really a God watching" \
                        f" everything? You know, with a plan for us and stuff. I don’t know, man, but it keeps me up at night'\n" \
                        f"'...What?! I mean why are we out here, in this arena?'\n'Oh. Uh... yeah'\n'What was all that stuff " \
                        f"about God?'\n'Uh...hm? Nothing.'\n'You wanna talk about it?'\n'No'\n'You sure?'\n'Yeah.'"
                else:
                    return f"{t1} and {t2} contemplate the meaning of life over a campfire."
            elif scenario == 11:
                trib1.inj = True
                trib2.inj = True
                return f"{t1} and {t2} are attacked by a swarm of bats."
            elif scenario == 12:
                return f"{t1} leaves cooking dinner up to {t2} and ends up having to gulp down " \
                    f"**[CENSORED DUE TO GRAPHIC HORROR]**."

        elif self.type == 3:
            t3 = trib3.name

            weird_amulet = (trib1.supplies == 'weird amulet' or trib2.supplies == 'weird amulet' or
                            trib3.supplies == 'weird amulet')
            if weird_amulet:  # weird amulet has custom outcomes
                temp = random.randint(0, 2)
                if temp == 0: # continue onward as if nothing happened
                    pass
                elif temp == 1:
                    if trib1.supplies == 'weird amulet':
                        sworded = trib1
                    elif trib2.supplies == 'weird amulet':
                        sworded = trib2
                    elif trib3.supplies == 'weird amulet':
                        sworded = trib3
                    sworded.supplies = None
                    sworded.weapon = 'cursed sword'
                    return f"{t1}, {t2} and {t3} fiddle around with the weird amulet, and in a sudden puff of purple smoke, " \
                        f"it transforms into a cursed sword."
                elif temp == 2:
                    kill(trib1, self)
                    kill(trib2)
                    kill(trib3)
                    return f"{t1}, {t2} and {t3} try to get some sleep, when in a sudden puff of smoke, the weird amulet" \
                        f" randomly summons a winged monstrosity that dismembers them both before flying off into the night sky."

            # figure out who's injured
            if trib1.inj:
                injured = trib1
                if trib1.supplies is not None:
                    supplier = trib1
                    shuffled = [trib2, trib3]
                    random.shuffle(shuffled)
                    helper = shuffled[0]
                    gaurd = shuffled[1]
                elif trib2.supplies is not None:
                    supplier = trib2
                    helper = trib2
                    gaurd = trib3
                elif trib3.supplies is not None:
                    supplier = trib3
                    helper = trib3
                    gaurd = trib2
                else:
                    supplier = None
            elif trib2.inj:
                injured = trib2
                if trib1.supplies is not None:
                    supplier = trib1
                    helper = trib1
                    gaurd = trib3
                elif trib2.supplies is not None:
                    supplier = trib2
                    shuffled = [trib1, trib3]
                    random.shuffle(shuffled)
                    helper = shuffled[0]
                    gaurd = shuffled[1]
                elif trib3.supplies is not None:
                    supplier = trib3
                    helper = trib3
                    gaurd = trib1
                else:
                    supplier = None
            elif trib3.inj:
                injured = trib3
                if trib1.supplies is not None:
                    supplier = trib1
                    helper = trib1
                    gaurd = trib2
                elif trib2.supplies is not None:
                    supplier = trib2
                    helper = trib2
                    gaurd = trib1
                elif trib3.supplies is not None:
                    supplier = trib3
                    shuffled = [trib1, trib2]
                    random.shuffle(shuffled)
                    helper = shuffled[0]
                    gaurd = shuffled[1]
                else:
                    supplier = None
            else:
                injured = None
                supplier = None

            # If the either tribute has supplies and is injured, it overrides all other scenarios
            if injured is not None and supplier is not None:
                if supplier.supplies == 'medkit':
                    supplier.supplies = None
                    injured.inj = False
                    return f"{helper.name} tends to {injured.name}'s injuries using a medkit, while {gaurd.name}" \
                        f" stands gaurd."
                elif supplier.supplies == 'herbs':
                    injured.inj = False
                    supplier.supplies = None
                    return f"{helper.name} tends to {injured.name}'s injuries using a some herbs {gaurd.name} had" \
                        f" grabbed along the way."

            scenario = random.randint(0, 13)
            if scenario == 0:
                trib1.asleep = True
                trib2.asleep = True
                return f"{t1}, {t2} and {t3} tell old tales and bond over a campfire."
            elif scenario == 1:
                return f"{t1}, {t2} and {t3} sleep in shifts throughout the night."
            elif scenario == 2:
                trib1.asleep = True
                trib2.asleep = True
                return f"{t1}, {t2} and {t3} huddle up for warmth."
            elif scenario == 3:
                trib1.asleep = True
                trib2.asleep = True
                return f"{t1} discreetly and implicitly confesses {trib1.hisher} love to {t2}, but {t2} is " \
                    f"{random.choice(['denser than a black hole', 'as dense as a harem mc'])}, and never realizes" \
                    f" it, while {t3} just facepalms."
            elif scenario == 4:
                trib1.asleep = True
                trib2.asleep = True
                return f"{t1}, {t2} and {t3} fall asleep admiring the beauty of the star-lit sky."
            elif scenario == 5:
                return f"{t1}, {t2} and {t3} set up a campfire and cheerfully sing anime OPs all night."
            elif scenario == 6:
                trib2.asleep = True
                trib1.asleep = True
                return f"{t1} tries to convince {t2} to snuggle with {trib1.himher}, but {t2} refuses, and {t1} has" \
                    f" to make do with {t3}."
            elif scenario == 7:
                trib2.asleep = True
                trib1.asleep = True
                return f"{t1} and {t2} snuggle up while {t3} stoically keeps gaurd."
            elif scenario == 8:
                if trib1.gender.lower() == "m" and trib2.gender.lower() == "m" and trib3.gender.lower() == "m":
                    return f"{t1}, {t2}, and {t3} fuck eachother in the ass all night but their balls don't touch so" \
                        f" they all maintain their heterosexuality."
                else:
                    return f"After {t3} goes to sleep, {t1} tries to make a move on {t2}, but {trib2.heshe}" \
                        f" respectfully declines, simply saying 'I love {t3}'."
            elif scenario == 9:
                trib3.kills += 2
                kill(trib2, self)
                kill(trib1)
                return f"{t3} reveals {trib3.hisher} true colors and murders both {t1} and {t2} in their sleep."
            elif scenario == 10:
                trib2.kills += 1
                kill(trib1, self)
                score1 = trib3.calculate_strength()
                score2 = trib2.calculate_strength()
                if score1 > score2:
                    trib3.kills += 1
                    kill(trib2)
                    return f"{t2} reveals {trib2.hisher} true colors and murder {t1} in {trib1.hisher} sleep, but" \
                        f" {t3} wakes up sensing something wrong, and pins {t2} down before exacting revenge for" \
                        f" {trib2.hisher} betrayal."
                else:
                    return f"{t2} reveals {trib2.hisher} true colors and murder {t1} in {trib1.hisher} sleep, but" \
                        f" {t3} wakes up sensing something wrong, and quietly runs away before {trib3.heshe} gets" \
                        f" {trib3.himher}self gutted too."
            elif scenario == 11:
                trib1.inj = True
                trib2.inj = True
                trib3.inj = True
                return f"{t1}, {t2} and {t3} are attacked by a swarm of bats."
            elif scenario == 12:
                return f"{t1} and {t2} leave cooking dinner up to {t3} and end up having to gulp down " \
                    f"||[CENSORED DUE TO GRAPHIC HORROR]||."
            elif scenario == 13:
                return f"{t1} and {t2} make out all night while {t3} vainly tries to get some sleep."

    def error(self):
        raise Exception("Party Error: Uncallable function used. Check do_things and Bloodbath, likely cause due to a"
                        " party forming up and not setting itself as done, thereby freeing it to be used as trib2 for"
                        " other tributes.")


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


# sorts encounters to their respective functions
def sorting_hat(tribute1, tribute2):
    if type(tribute1) == Tribute:
        if type(tribute2) == Tribute:
            return one_v_one(tribute1, tribute2)
        elif type(tribute2) == Party:
            return two_v_one(tribute2, tribute1)
    elif type(tribute1) == Party:
        if tribute1.type == 2:
            if type(tribute2) == Tribute:
                return two_v_one(tribute1, tribute2)
            elif type(tribute2) == Party:
                if tribute2.type == 2:
                    return two_v_two(tribute1, tribute2)
                elif tribute2.type == 3:
                    return three_v_two(tribute2, tribute1)
        elif tribute1.type == 3:
            if type(tribute2) == Tribute:
                return three_v_one(tribute1, tribute2)
            elif type(tribute2) == Party:
                if tribute2.type == 2:
                    return three_v_two(tribute1, tribute2)
                elif tribute2.type == 3:
                    return three_v_three(tribute1, tribute2)


def one_v_one(tribute1, tribute2):
    t1 = tribute1.name
    t2 = tribute2.name

    aggro_multiplier = 1
    # checks if either tribute has weapons
    if (tribute1.weapon is None) is not (tribute2.weapon is None):
        if tribute1.inj != tribute2.inj:
            aggro_multiplier = 2
        else:
            aggro_multiplier = 1.5

    scenario = int(random.randint(0, 10) * aggro_multiplier)
    # 0-3 neutral scenarios, 3-5 teaming up scenarios
    if scenario == 0:
        return f"{t1} sees {t2} in the distance, but ignores {tribute2.himher} for now."
    elif scenario == 1:
        return f"{t1} and {t2} both spot each other, but both of them slowly back off and run into the distance."
    elif scenario == 2:
        return f"{t1} covertly stalks {t2} through the bushes."
    elif scenario == 3:
        party = Party(tribute1, tribute2)
        party.done = True
        return f"{party.t1} and {party.t2} decide to stick together for the day and go hunting for supplies."
    elif scenario == 4:
        temp = random.randint(0, 9)
        if temp == 9:
            tribute2.done = True
            return f"{t1} and {t2} have hot, steamy, sweaty sex, then go about their separate ways."
        else:
            party = Party(tribute1, tribute2)
            party.done = True
            return f"{party.t1} and {party.t2} decide to team up and hunt other tributes."
    elif scenario == 5:
        party = Party(tribute1, tribute2)
        party.done = True
        return f"{party.t1} and {party.t2} remember an anime-watching contract that they forged long ago, and in its honour, decide to team up."
    # 6+ violent scenarios
    elif scenario > 5:
        tribute2.done = True
        # figure out who's stronger
        strong, weak, even = compare_strength(tribute1, tribute2)

        str = strong.name
        wk = weak.name

        if strong.weapon == 'cursed sword' or weak.weapon == 'cursed sword':
            temp = random.randint(0, 2)
            if temp == 0:
                if weak.weapon == 'cursed sword':
                    weak.kills += 1
                    kill(strong)
                    return f"{wk} uses the ancient power of {weak.hisher} {weak.weapon} to banish" \
                        f" {str} into oblivion."
                if strong.weapon == 'cursed sword':
                    strong.kills += 1
                    kill(weak)
                    return f"{str} uses the ancient power of {strong.hisher} {strong.weapon} to banish" \
                        f" {wk} into oblivion."
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

        elif strong.weapon == 'gun' or weak.weapon == 'gun':
            temp = random.randint(0, 2)
            if strong.weapon == 'gun':
                strong.kills += 1
                kill(weak)
                if temp == 2:
                    strong.weapon = None
                    return f"{str} just straights up shoots {wk} in the head with {strong.hisher} gun, but runs " \
                        f"out of bullets in the process."
                else:
                    return f"{str} just straights up shoots {wk} in the head with {strong.weapon}."
            elif weak.weapon == 'gun':
                weak.kills += 1
                kill(strong)
                if temp == 2:
                    weak.weapon = None
                    return f"{wk} just straights up shoots {str} in the head with {weak.hisher} gun, but runs " \
                        f"out of bullets in the process."
                else:
                    return f"{wk} just straights up shoots {str} in the head with {weak.weapon}."


        elif strong.weapon in cleavers:
            if even:
                weak.inj = True
                return f"{str} tries to cleave {wk} in two but {wk} manages to escape with {weak.hisher}" \
                    f" life, albeit injured."
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
                return f"{str} stabs {wk} in the gut with a {strong.weapon}, but {wk} manages to push" \
                    f" {strong.himher} off and run away."
            else:
                strong.kills += 1
                kill(weak)
                if scenario > 7:
                    return f"A well aimed stab by {str}'s {strong.weapon} ends {wk}'s miserable life."
                else:
                    return f"After a drawn-out fight, {str} manages to catch {wk} in the throat with" \
                        f" {strong.hisher} {strong.weapon} and scores a kill."

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
                return f"In a magnificent display of manliness, an injured {str} and {wk} fight it out to the " \
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
                    return f"{str} remembers the words of {strong.hisher} old boxing coach, and on the" \
                        f" brink of death, while the anime OP plays in the background, KO's {wk} in one final punch."


def two_v_one(party, tribute3):
    trib1 = party.trib1
    trib2 = party.trib2
    t1 = trib1.name
    t2 = trib2.name
    t3 = tribute3.name

    party.done = True
    tribute3.done = True
    num = random.randint(0, 1)  # decides if it's a fight or if they're joining up
    scenario = random.randint(0, 2)
    if num == 0:
        party.add_tribute(tribute3)
        choose = random.choice(['k-pop', 'back muscles', 'catboys', 'catgirls', 'traumatic harada doujins',
                                'The Big Gay', 'Haikyuu', 'ecchi trash', 'furry bl', 'giant titties'])
        return f"{t1} and {t2} run into {t3}, and after they realize their mutual love for {choose}, {t1} and" \
            f" {t2} decide to let {t3} join their team."
    else:
        if tribute3.weapon == 'cursed sword':
            temp = random.randint(0, 2)

            if temp == 0:
                tribute3.kills += 2
                kill(trib1, party)
                kill(trib2)
                return f"{t1} and {t2} spot {t3} in the distance and tries to hunt {tribute3.himher} down, but {t3}" \
                    f" uses the mystical power of {tribute3.hisher} {tribute3.weapon} and banishes both {t1} and" \
                    f" {t2} into the void."

            elif temp == 1:
                tribute3.kills += 2
                tribute3.inj = True
                kill(trib1, party)
                kill(trib2)
                return f"{t1} and {t2} spot {t3} in the distance and tries to hunt {tribute3.himher} down, but " \
                    f"{t3} scorches both of them to dust using the overwhelming power of {tribute3.hisher} " \
                    f"{tribute3.weapon}. However, the flames are fierce and {t3} injures {tribute3.himher}self in " \
                    f"the inferno."

            elif temp == 2:
                kill(trib1, party)
                kill(trib2)
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
        elif tribute3.weapon == 'gun':
            tribute3.kills += 2
            kill(trib1, party)
            kill(trib2)
            if scenario == 0:
                tribute3.weapon = None
                return f"{t3} spots {t1} and {t2} nearby, and before they even have time to react, {t3} mows em " \
                    f"down with {tribute3.hisher} gun - though {tribute3.heshe} runs out of bullets in the process."
            else:
                return f"{t3} spots {t1} and {t2} nearby, and before they even have time to react, {t3} mows em " \
                    f"down with {tribute3.hisher} gun."

        elif ((tribute3.weapon is not None) and (trib2.weapon is None) and (trib1.weapon is None)) or (
                trib1.inj and trib2.inj):
            if trib1.inj:
                kill(trib1, party)
                trib2.inj = True
                return f"{t3} covetly stalks {t1} and {t2} as they stumble around the arena, and when " \
                    f"{tribute3.heshe} feels the time is right, {t3} strikes; {tribute3.heshe} smashes {t1}'s face" \
                    f" in, but {t2} manages to escape, wounded."
            elif trib2.inj:
                kill(trib2, party)
                trib1.inj = True
                return f"{t3} covetly stalks {t1} and {t2} as they stumble around the arena, and when " \
                    f"{tribute3.heshe} feels the time is right, {t3} strikes; {tribute3.heshe} smashes {t2}'s face" \
                    f" in, but {t1} manages to escape, wounded."
            else:
                trib1.inj = True
                trib2.inj = True
                return f"{t3} covetly stalks {t1} and {t2} as they stumble around the arena, and when" \
                    f"{tribute3.heshe} feels the time is right, {t3} stikes; both {t1} and {t2} take quite" \
                    f" the beating, but they manage to escape, wounded."
        else:
            if scenario == 0:
                trib1.kills += 1
                trib2.kills += 1
                kill(tribute3)
                return f"{t1} and {t2} spot {t3} from afar and hunts {tribute3.himher} down before " \
                    f"{tribute3.heshe} can escape."
            elif scenario == 1:
                if trib1.inj:
                    trib2.kills += 1
                    tribute3.kills += 1
                    kill(trib1, party)
                    kill(tribute3)
                    return f"{t1} and {t2} spot {t3} from afar and hunts {tribute3.himher} down, but {t3} puts up" \
                        f" quite a fight, and manages to take out a weakened {t1}."
                else:
                    trib1.inj = True
                    trib1.kills += 1
                    trib2.kills += 1
                    kill(tribute3)
                    return f"{t1} and {t2} spot {t3} from afar and hunts {tribute3.himher} down, but {t3} puts up" \
                        f" quite a fight and leaves {t1} injured."
            elif scenario == 2:
                if trib2.inj:
                    trib1.kills += 1
                    tribute3.kills += 1
                    kill(trib2, party)
                    kill(tribute3)
                    return f"{t1} and {t2} spot {t3} from afar and hunts {tribute3.himher} down, but {t3} puts up" \
                        f" quite a fight, and manages to take out a weakened {t2}."
                else:
                    trib2.inj = True
                    trib1.kills += 1
                    trib2.kills += 1
                    kill(tribute3)
                    return f"{t1} and {t2} spot {t3} from afar and hunts {tribute3.himher} down, but {t3} puts up" \
                        f" quite a fight and leaves {t2} injured."


def three_v_one(party, tribute4):
    trib1 = party.trib1
    trib2 = party.trib2
    trib3 = party.trib3

    t1 = trib1.name
    t2 = trib2.name
    t3 = trib3.name
    t4 = tribute4.name

    party.done = True
    tribute4.done = True

    choice = random.choice(['setting up a bear trap', 'punching a tree', 'tripping on shrooms'])

    if tribute4.weapon == 'cursed sword':
        temp = random.randint(0, 2)

        if temp == 0:
            tribute4.kills += 3
            kill(trib1, party)
            kill(trib2)
            kill(trib3)
            return f"{t1}, {t2} and {t3} spot {t4} in the distance and tries to hunt {tribute4.himher} down, but" \
                f" {t4} uses the mystical power of {tribute4.hisher} {tribute4.weapon} and banishes all three of" \
                f" {tribute4.hisher} opponents into the void."

        elif temp == 1:
            tribute4.kills += 3
            tribute4.inj = True
            kill(trib1, party)
            kill(trib2)
            kill(trib3)
            return f"{t1}, {t2} and {t3} spot {t4} in the distance and tries to hunt {tribute4.himher} down, but " \
                f"{t4} scorches both of them to dust using the overwhelming power of {tribute4.hisher} " \
                f"{tribute4.weapon}. However, the flames are fierce and {t4} injures {tribute4.himher}self in " \
                f"the inferno."

        elif temp == 2:
            kill(trib1, party)
            kill(trib2)
            kill(trib3)
            kill(tribute4)
            choice = random.choice([f"After getting ganged on by {t1}, {t2}, and {t3}, {t4} tries using the full "
                                    f"potential of {tribute4.hisher} {tribute4.weapon}, but the influx of "
                                    f"power is too much for {tribute4.himher} to control and all three get "
                                    f"obliterated in a proceeding explosion.",
                                    f"After getting ganged on by {t1}, {t2}, and {t3}, {t4} uses {tribute4.hisher}"
                                    f" {tribute4.weapon} to summon an eldritch monstrosity from the otherworld "
                                    f"to fight for {tribute4.himher}. However, the monstrosity was in the "
                                    f"middle of watching Gundam when it was summoned, and in its rage at being"
                                    f" interrupted, dismembered everyone in the vicinity."])
            return choice
    elif tribute4.weapon == 'gun':
        tribute4.kills += 3
        kill(trib1, party)
        kill(trib2)
        kill(trib3)
        ran_out_of_ammo = random.choice([True, False])
        if ran_out_of_ammo:
            tribute4.weapon = None
            return f"{t4} spots {t1}, {t2} and {t3} nearby, and before they even have time to react, {t4} mows em " \
                f"down with {tribute4.hisher} gun - though {tribute4.heshe} runs out of bullets in the process."
        else:
            return f"{t4} spots {t1}, {t2} and {t3} nearby, and before they even have time to react, {t4} mows em " \
                f"down with {tribute4.hisher} gun."

    if party.calculate_strength() <= tribute4.calculate_strength():
        tribute4.inj = True
        return f"{t1}, {t2} and {t3} chance upon {t4} {choice}. They chase {tribute4.himher} through" \
            f" the wounds, but {t4} jumps down a tall cliff and manages to lose them, though {tribute4.heshe}" \
            f" injures {tribute4.himher} leg in the process."
    else:
        if trib1.weapon is not None:
            trib1.kills += 1
            kill(tribute4)
            if trib1.weapon in cleavers or trib1.weapon == 'cursed sword':
                verb = "skewers"
            elif trib1.weapon in stabbers:
                verb = "guts"
            elif trib1.weapon in clubbers:
                verb = "pulverizes"
            elif trib1.weapon in ranged or trib1.weapon == 'gun':
                verb = "executes"
            return f"{t1}, {t2} and {t3} chance upon {t4} {choice}. While {t4} tries to escape, {t2} and {t3} manage" \
                f" to catch {tribute4.himher} and holds {tribute4.himher} down while {t1} {verb} {t4} with" \
                f" {trib1.hisher} {trib1.weapon}"
        elif trib2.weapon is not None:
            trib2.kills += 1
            kill(tribute4)
            if trib2.weapon in cleavers or trib2.weapon == 'cursed sword':
                verb = "skewers"
            elif trib2.weapon in stabbers:
                verb = "guts"
            elif trib2.weapon in clubbers:
                verb = "pulverizes"
            elif trib2.weapon in ranged or trib2.weapon == 'gun':
                verb = "executes"
            return f"{t1}, {t2} and {t3} chance upon {t4} {choice}. While {t4} tries to escape, {t1} and {t3} manage" \
                f" to catch {tribute4.himher} and holds {tribute4.himher} down while {t2} {verb} {t4} with" \
                f" {trib2.hisher} {trib2.weapon}"
        elif trib3.weapon is not None:
            trib3.kills += 1
            kill(tribute4)
            if trib3.weapon in cleavers or trib3.weapon == 'cursed sword':
                verb = "skewers"
            elif trib3.weapon in stabbers:
                verb = "guts"
            elif trib3.weapon in clubbers:
                verb = "pulverizes"
            elif trib3.weapon in ranged or trib3.weapon == 'gun':
                verb = "executes"
            return f"{t1}, {t2} and {t3} chance upon {t4} {choice}. While {t4} tries to escape, {t1} and {t2} manage" \
                f" to catch {tribute4.himher} and holds {tribute4.himher} down while {t3} {verb} {t4} with" \
                f" {trib3.hisher} {trib3.weapon}"
        else:
            trib1.kills += 1
            kill(tribute4)
            return f"{t1}, {t2} and {t3} chance upon {t4} {choice}. While {t4} tries to escape, {t3} and {t2} manage" \
                f" to catch {tribute4.himher} and holds {tribute4.himher} down while {t1} drops a large rock on" \
                f" {t4}'s head, killing {tribute4.himher} instantly."


def two_v_two(party1, party2):

    strong, weak, even = compare_strength(party1, party2)
    strong1 = strong.trib1
    strong2 = strong.trib2
    weak1 = weak.trib1
    weak2 = weak.trib2

    st1 = strong1.name
    st2 = strong2.name
    wk1 = weak1.name
    wk2 = weak2.name

    party1.done = True
    party2.done = True

    score_st = strong.calculate_strength()
    score_wk = weak.calculate_strength()

    cs_boi = None
    g_boi = None
    for boi in [strong1, strong2, weak1, weak2]:
        if boi.weapon == "cursed sword":
            cs_boi = boi
            cb = boi.name
            break
        elif boi.weapon == "gun":
            g_boi = boi
            gb = boi.name
            break

    if cs_boi is not None:
        temp = random.randint(0, 2)
        choice = random.choice(['traversing a desert', 'walking through the woods' , 'hunting for supplies'])
        if temp == 0:
            cs_boi.kills += 2
            if cs_boi in [strong1, strong2]:
                kill(weak1, weak)
                kill(weak2)
            else:
                kill(strong1, strong)
                kill(strong2)
            return f"{st1} and {st2} encounter {wk1} and {wk2} while {choice}. A fight ensues, but it doesn't last" \
                f" long - {cb} uses the mystical power of {cs_boi.hisher} {cs_boi.weapon} and banishes his opponents" \
                f" into the void."

        elif temp == 1:
            cs_boi.kills += 2
            cs_boi.inj = True
            if cs_boi in [strong1, strong2]:
                kill(weak1, weak)
                kill(weak2)
            else:
                kill(strong1, strong)
                kill(strong2)
            return f"{st1} and {st2} encounter {wk1} and {wk2} while {choice}. {cb} tells {cs_boi.hisher} buddy to" \
                f" step back, before using the overwhelming power of {cs_boi.hisher} {cs_boi.weapon} to" \
                f" summon a blazing inferno and scorch {cs_boi.hisher} enemies. However, the flames are fierce and" \
                f" {cb} injures {cs_boi.himher}self in blaze."

        elif temp == 2:
            kill(strong1, strong)
            kill(strong2)
            kill(weak1, weak)
            kill(weak2)
            choice = random.choice([f"{st1} and {st2} encounter {wk1} and {wk2} while {choice}. {cb} tries unleashing"
                                    f" the full potential of {cs_boi.hisher} {cs_boi.weapon}, but the influx of"
                                    f" power is too much for {cs_boi.himher} to control and everyone in the vicinity"
                                    f" gets obliterated in a massive explosion.",
                                    f"{st1} and {st2} encounter {wk1} and {wk2} while {choice}. {cb} uses"
                                    f" {cs_boi.hisher} {cs_boi.weapon} to summon an eldritch monstrosity from the"
                                    f" otherworld to fight for {cs_boi.himher}. However, the monstrosity was in the"
                                    f" middle of watching Gundam when it was summoned, and in its rage at being"
                                    f" interrupted, dismembered everyone in the vicinity."])
            return choice
    elif g_boi is not None:
        g_boi.kills += 2
        if g_boi in [strong1, strong2]:
            kill(weak1, weak)
            kill(weak2)
        else:
            kill(strong1, strong)
            kill(strong2)
        if random.choice([True, False]):
            g_boi.weapon = None
            return f"{st1} and {st2} chance into {wk1} and {wk2}. What follows is less of a fight and more of a" \
                f" massacre, as {gb} mows down {g_boi.hisher} enemies using {g_boi.hisher} gun - though" \
                f" {g_boi.heshe} runs out of bullets in the process."
        else:
            return f"{st1} and {st2} chance into {wk1} and {wk2}. What follows is less of a fight and more of a" \
                f" massacre, as {gb} mows down {g_boi.hisher} enemies using {g_boi.hisher} gun."

    if (score_st - score_wk) > 1:  # big difference between their abilities
        kill(weak1, weak)
        kill(weak2)

        if strong1.weapon in ranged:
            strong1.kills += 2
            return f"{st1} and {st2} while traversing a plain encounter {wk2} and {wk2}. They try to run away, but" \
                f" {st1}'s {strong1.weapon} picks both of them off from the distance."
        elif strong2.weapon in ranged:
            strong2.kills += 2
            return f"{st1} and {st2} while traversing a plain encounter {wk2} and {wk2}. They try to run away, but" \
                    f" {st2}'s {strong2.weapon} picks both of them off from the distance."
        else:
            strong1.kills += 1
            strong2.kills += 1
            choice = random.choice([f"{st1} and {st2} encounter {wk1} and {wk2} while traversing a desert. After a"
                                    f" duel in the searing heat, {st1} gains the upper hand over {wk1} and manages to"
                                    f" skewer {weak1.himher}. {st1} and {st2} proceed to make quick work of {wk2}, both"
                                    f" coming out the exchange with barely a scrape",
                                    f"{st1} and {st2} spot {wk1} and {wk2} in the thick of a jungle. {st1} manages"
                                    f" to get the drop on {wk2} and cuts {weak2.himher} down before {weak2.heshe} can"
                                    f" even react. {wk1} tries to escape, but a hidden {st2} makes quick work of"
                                    f" {weak2.himher} as well.",
                                    f"{wk1} and {wk2} spot {st1} and {st2} traveling through a forest. They plan a"
                                    f" stealth attack, but it fails due to {st2}'s perceptive sense of smell, and"
                                    f" together with {st1} {strong2.heshe} makes quick work of {wk1} and {wk2}."])
            return choice
    elif not even:  # close but no cigar
        kill(weak1, weak)
        kill(weak2)
        strong1.kills += 1
        strong2.kills += 1
        injured = random.choice([strong1, strong2])
        if injured == strong1:
            not_injured = strong2
        elif injured == strong2:
            not_injured = strong1
        choice = random.choice([f"{st1} and {st2} encounter {wk1} and {wk2} while traversing a desert. After a"
                                f" duel in the searing heat, {injured.name} manages to skewer {wk1}, though"
                                f" {injured.heshe} gets wounded in the process. {st1} and {st2} proceed to make quick"
                                f" work of {wk2}.",
                                f"{st1} and {st2} spot {wk1} and {wk2} in the thick of a jungle. {injured.name} manages"
                                f" to get the drop on {wk2} and cuts {weak2.himher} down before {weak2.heshe} can"
                                f" even react. However, {wk1} lashes out and manages to wound {injured.name}, before"
                                f" {not_injured.name} comes from behind and takes {wk1} out.",
                                f"{wk1} and {wk2} spot {st1} and {st2} traveling through a forest. They plan a"
                                f" stealth attack, but it fails due to {st2}'s perceptive sense of smell, and"
                                f" together with {st1} {strong2.heshe} makes quick work of {wk1} and {wk2}, though"
                                f" {injured.name} gets injured in the process."])
        return choice
    elif even:
        kill(weak1, weak)
        kill(weak2)
        if strong1.inj:
            strong2.kills += 2
            weak1.kills += 1
            kill(strong1, strong)
            strong2.inj = True

            choice = random.choice(['traversing a desert', 'walking through the woods' , 'hunting for supplies'])
            return f"{st1} and {st2} encounter {wk1} and {wk2} while {choice}. After a long, drawn out fight, {st2}" \
                f" manages to gut {wk2}, but turns around to see the corpse of {st1} lying on the ground and {wk1}" \
                f" at death's door. {st2} puts {wk1} out of {weak1.hisher} misery and trudges forward."
        elif strong2.inj:
            strong1.kills += 2
            weak2.kills += 1
            kill(strong2, strong)
            strong1.inj = True

            choice = random.choice(['traversing a desert', 'walking through the woods' , 'hunting for supplies'])
            return f"{st1} and {st2} encounter {wk1} and {wk2} while {choice}. After a long, drawn out fight, {st1}" \
                f" manages to gut {wk1}, but turns around to see the corpse of {st2} lying on the ground and {wk2}" \
                f" at death's door. {st1} puts {wk2} out of {weak2.hisher} misery and trudges forward."
        else:
            strong1.kills += 1
            strong2.kills += 1
            strong1.inj = True
            strong2.inj = True

            choice = random.choice(['traversing a desert', 'walking through the woods' , 'hunting for supplies'])
            return f"{st1} and {st2} encounter {wk1} and {wk2} while {choice}. After a long, drawn out fight, {st1}" \
                f" and {st2} manage to somehow emerge victorious, but they both suffer from heavy wounds."
    else:
        raise Exception("Line 991, function two_vs_two")


def three_v_two(party1, party2):
    trib1 = party1.trib1
    trib2 = party1.trib2
    trib3 = party1.trib3
    trib4 = party2.trib1
    trib5 = party2.trib2

    t1 = trib1.name
    t2 = trib2.name
    t3 = trib3.name
    t4 = trib4.name
    t5 = trib5.name

    party1.done = True
    party2.done = True

    score1 = party1.calculate_strength()
    score2 = party2.calculate_strength()

    cs_boi = None
    g_boi = None
    for boi in [trib1, trib2, trib3, trib4, trib5]:
        if boi.weapon == "cursed sword":
            cs_boi = boi
            cb = boi.name
            break
        elif boi.weapon == "gun":
            g_boi = boi
            gb = boi.name
            break

    if cs_boi is not None:
        temp = random.randint(0, 2)
        choice = random.choice(['traversing a desert', 'walking through the woods', 'hunting for supplies'])
        if temp == 0:
            cs_boi.kills += 2
            if cs_boi in [trib1, trib2, trib3]:
                kill(trib4, party2)
                kill(trib5)
            else:
                cs_boi.kills += 1
                kill(trib1, party1)
                kill(trib2)
                kill(trib3)
            return f"{t1}, {t2} and {t3} encounter {t4} and {t5} while {choice}. A fight ensues, but it doesn't last" \
                f" long - {cb} uses the mystical power of {cs_boi.hisher} {cs_boi.weapon} and banishes his opponents" \
                f" into the void."

        elif temp == 1:
            cs_boi.kills += 2
            cs_boi.inj = True
            if cs_boi in [trib1, trib2, trib3]:
                kill(trib4, party2)
                kill(trib5)
            else:
                cs_boi.kills += 1
                kill(trib1, party1)
                kill(trib2)
                kill(trib3)
            return f"{t1}, {t2} and {t3} encounter {t4} and {t5} while {choice}. {cb} tells {cs_boi.hisher} buddies to" \
                f" step back, before using the overwhelming power of {cs_boi.hisher} {cs_boi.weapon} to" \
                f" summon a blazing inferno and scorch {cs_boi.hisher} enemies. However, the flames are fierce and" \
                f" {cb} injures {cs_boi.himher}self in blaze."

        elif temp == 2:
            kill(trib1, party1)
            kill(trib2)
            kill(trib3)
            kill(trib4, party2)
            kill(trib5)
            choice = random.choice([f"{t1}, {t2} and {t3} encounter {t4} and {t5} while {choice}. {cb} tries unleashing"
                                    f" the full potential of {cs_boi.hisher} {cs_boi.weapon}, but the influx of"
                                    f" power is too much for {cs_boi.himher} to control and everyone in the vicinity"
                                    f" gets obliterated in a massive explosion.",
                                    f"{t1}, {t2} and {t3} encounter {t4} and {t5} while {choice}. {cb} uses"
                                    f" {cs_boi.hisher} {cs_boi.weapon} to summon an eldritch monstrosity from the"
                                    f" otherworld to fight for {cs_boi.himher}. However, the monstrosity was in the"
                                    f" middle of watching Gundam when it was summoned, and in its rage at being"
                                    f" interrupted, dismembered everyone in the vicinity."])
            return choice
    elif g_boi is not None:
        g_boi.kills += 2
        if g_boi in [trib1, trib2, trib3]:
            kill(trib4, party2)
            kill(trib5)
        else:
            g_boi.kills += 1
            kill(trib1, party1)
            kill(trib2)
            kill(trib3)
        if random.choice([True, False]):
            g_boi.weapon = None
            return f"{t1}, {t2} and {t3} chance into {t4} and {t5}. What follows is less of a fight and more of a" \
                f" massacre, as {gb} mows down {g_boi.hisher} enemies using {g_boi.hisher} gun - though" \
                f" {g_boi.heshe} runs out of bullets in the process."
        else:
            return f"{t1}, {t2} and {t3} chance into {t4} and {t5}. What follows is less of a fight and more of a" \
                f" massacre, as {gb} mows down {g_boi.hisher} enemies using {g_boi.hisher} gun."

    if score1 < score2:
        kill(trib1, party1)
        kill(trib2)
        kill(trib3)
        trib4.kills += 2
        trib5.kills += 1
        if trib4.weapon in cleavers:
            verb = f"single swing of {trib4.hisher} {trib4.weapon}"
        elif trib4.weapon in stabbers:
            verb = f"couple well-aimed stabs using {trib4.hisher} {trib4.weapon}"
        elif trib4.weapon in clubbers:
            verb = f"single swing of {trib4.hisher} {trib4.weapon}"
        elif trib4.weapon in ranged:
            verb = f"single shot from {trib4.hisher} {trib4.weapon}"
        else:
            verb = "couple good punches"
        return f"{t1}, {t2} and {t3} spot {t4} and {t5} sharpening their weapons in the distance. Injured and" \
            f" exhausted, they try to stealthily escape without alerting {t4} and {t5}, but {t2} steps on a branch" \
            f" and they end up having to fight it out. {t4} takes out {t2} and {t3} with a {verb}, and {t5} does not" \
            f" heed {t1}'s plead to spare {trib1.hisher} life."
    if score1 == score2:
        trib4.inj = True
        trib5.inj = True
        trib1.inj = True
        trib2.inj = True
        trib3.inj = True
        return f"{t1}, {t2} and {t3} encounter {t4} and {t5}, and decide to fight it out. While outnumbered and" \
            f" suffering injuries themselves, {t4} and {t5} still manage to inflict heavy wounds on their opponents," \
            f" and {t1} ends up calling for a retreat."
    else:
        kill(trib4, party2)
        kill(trib5)
        num = random.randint(0, 2)
        if num == 0:
            trib1.kills += 1
            trib2.kills += 1
            trib1.inj = True
            return f"{t1}, {t2} and {t3} encounter {t4} and {t5} while exploring a derelict mansion. {t2} and" \
                f" {t3} corner {t4} into a closed-off room and makes quick work of {trib4.himher}, while {t1}" \
                f" handles {t5} by {trib1.himher}self, though {trib1.heshe} gets injured in the process."
        elif num == 1:
            trib3.kills += 1
            trib2.kills += 1
            trib2.inj = True
            return f"{t1}, {t2} and {t3} encounter {t4} and {t5} while exploring a labyrinthine sytem of caves." \
                f" {t1} and {t3} corner {t4} into a dark enclave and makes quick work of {trib4.himher}, while {t2}" \
                f" handles {t5} by {trib2.himher}self, though {trib2.heshe} gets injured in the process."
        elif num == 2:
            trib1.kills += 1
            trib3.kills += 1
            trib3.inj = True
            return f"{t1}, {t2} and {t3} encounter {t4} and {t5} while walking through a forest." \
                f" {t1} and {t3} corner {t4} into a hidden grove and makes quick work of {trib4.himher}, while {t3}" \
                f" handles {t5} by {trib3.himher}self, though {trib3.heshe} gets injured in the process."


def three_v_three(party1, party2):
    strong, weak, even = compare_strength(party1, party2)
    strong1 = strong.trib1
    strong2 = strong.trib2
    strong3 = strong.trib3

    weak1 = weak.trib1
    weak2 = weak.trib2
    weak3 = weak.trib3

    st1 = strong1.name
    st2 = strong2.name
    st3 = strong3.name
    wk1 = weak1.name
    wk2 = weak2.name
    wk3 = weak3.name

    party1.done = True
    party2.done = True

    score1 = strong.calculate_strength()
    score2 = weak.calculate_strength()

    cs_boi = None
    g_boi = None
    for boi in [strong1, strong2, strong3, weak1, weak2, weak3]:
        if boi.weapon == "cursed sword":
            cs_boi = boi
            cb = boi.name
            break
        elif boi.weapon == "gun":
            g_boi = boi
            gb = boi.name
            break

    if cs_boi is not None:
        temp = random.randint(0, 2)
        choice = random.choice(['traversing a desert', 'walking through the woods', 'hunting for supplies'])
        if temp == 0:
            cs_boi.kills += 3
            if cs_boi in [strong1, strong2, strong3]:
                kill(weak1, weak)
                kill(weak2)
                kill(weak3)
            else:
                kill(strong1, strong)
                kill(strong2)
                kill(strong3)
            return f"{st1}, {st2} and {st3} encounter {wk1}, {wk2} and {wk3} while {choice}. A fight ensues, but it doesn't last" \
                f" long - {cb} uses the mystical power of {cs_boi.hisher} {cs_boi.weapon} and banishes his opponents" \
                f" into the void."

        elif temp == 1:
            cs_boi.inj = True
            cs_boi.kills += 3
            if cs_boi in [strong1, strong2, strong3]:
                kill(weak1, weak)
                kill(weak2)
                kill(weak3)
            else:
                kill(strong1, strong)
                kill(strong2)
                kill(strong3)
            return f"{st1}, {st2} and {st3} encounter {wk1}, {wk2} and {wk3} while {choice}. {cb} tells {cs_boi.hisher} buddies to" \
                f" step back, before using the overwhelming power of {cs_boi.hisher} {cs_boi.weapon} to" \
                f" summon a blazing inferno and scorch {cs_boi.hisher} enemies. However, the flames are fierce and" \
                f" {cb} injures {cs_boi.himher}self in blaze."

        elif temp == 2:
            kill(weak1, weak)
            kill(weak2)
            kill(weak3)
            kill(strong1, strong)
            kill(strong2)
            kill(strong3)
            choice = random.choice([f"{st1}, {st2} and {st3} encounter {wk1}, {wk2} and {wk3} while {choice}. {cb} tries unleashing"
                                    f" the full potential of {cs_boi.hisher} {cs_boi.weapon}, but the influx of"
                                    f" power is too much for {cs_boi.himher} to control and everyone in the vicinity"
                                    f" gets obliterated in a massive explosion.",
                                    f"{st1}, {st2} and {st3} encounter {wk1}, {wk2} and {wk3} while {choice}. {cb} uses"
                                    f" {cs_boi.hisher} {cs_boi.weapon} to summon an eldritch monstrosity from the"
                                    f" otherworld to fight for {cs_boi.himher}. However, the monstrosity was in the"
                                    f" middle of watching Gundam when it was summoned, and in its rage at being"
                                    f" interrupted, dismembered everyone in the vicinity."])
            return choice
    elif g_boi is not None:
        g_boi.kills += 3
        if g_boi in [strong1, strong2, strong3]:
            kill(weak1, weak)
            kill(weak2)
            kill(weak3)
        else:
            kill(strong1, strong)
            kill(strong2)
            kill(strong3)
        if random.choice([True, False]):
            g_boi.weapon = None
            return f"{st1}, {st2} and {st3} chance into {wk1}, {wk2} and {wk3}. What follows is less of a fight and more of a" \
                f" massacre, as {gb} mows down {g_boi.hisher} enemies using {g_boi.hisher} gun - though" \
                f" {g_boi.heshe} runs out of bullets in the process."
        else:
            return f"{st1}, {st2} and {st3} chance into {wk1}, {wk2} and {wk3}. What follows is less of a fight and more of a" \
                f" massacre, as {gb} mows down {g_boi.hisher} enemies using {g_boi.hisher} gun."


    choose = random.choice(['frolicking in the woods', 'fishing by the riverside',
                            'loudly debating the efficacy of alternate medicine'])
    if even:
        strong1.inj = True
        strong2.inj = True
        strong3.inj = True
        weak1.inj = True
        weak2.inj = True
        weak2.inj = True
        return f"{st1}, {st2} and {st3} encounter {wk1}, {wk2}, and {wk3} {choose}. A long, drawn out fight ensues," \
            f" and neither party seem to be able to break the equilibrium. Both eventually decide to retreat, but" \
            f" wounds are aplenty."

    elif (score1 - score2) > 1:
        strong1.kills += 1
        strong2.kills += 1
        strong3.kills += 1
        kill(weak1, weak)
        kill(weak2)
        kill(weak3)
        return f"{st1}, {st2} and {st3} encounter {wk1}, {wk2}, and {wk3} {choose}. After a quick, decisive fight," \
            f" {st1} and {strong1.hisher} allies come out victorious, with barely a scratch."
    else:
        strong1.kills += 1
        strong2.kills += 1
        strong3.kills += 1
        kill(weak1, weak)
        kill(weak2)
        kill(weak3)
        injured = random.choice([strong1, strong2, strong3])
        injured.inj = True
        return f"{st1}, {st2} and {st3} encounter {wk1}, {wk2}, and {wk3} {choose}. After a long, drawn out fight," \
            f" {st1} and {strong1.hisher} allies manage to come out victorious, though sacrifices are inevitable:" \
            f" {injured} is left wounded."


def kill(tribute, party=None):
    global tributes, dead, deadthisday
    if party is not None:  # kill automatically splits the party, so make sure to regenerate it if need be
        party.split()
        if party.trib1 == tribute:
            tributes.remove(tribute)
            dead.append(tribute)
            deadthisday.append(tribute)
        if party.trib2 == tribute:
            tributes.remove(tribute)
            dead.append(tribute)
            deadthisday.append(tribute)

    else:
        tributes.remove(tribute)
        dead.append(tribute)
        deadthisday.append(tribute)


def compare_strength(trib1, trib2):
    score_1 = trib1.calculate_strength()
    score_2 = trib2.calculate_strength()

    even = False
    if score_1 > score_2:
        strong = trib1
        weak = trib2
    elif score_2 > score_1:
        strong = trib2
        weak = trib1
    elif score_2 == score_1:
        strong = trib1
        weak = trib2
        even = True

    return strong, weak, even

#FIX THE FEAST
def feast_fight(tribute1, tribute2):
    t1 = tribute1.name
    t2 = tribute2.name
    temp = random.randint(0, 9)

    if tribute1.weapon in cleavers:
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




# ============================================================================


def do_things(tributes_list, trib_pick_action_function, party_pick_action_function):
    global events, tributes

    # So, since we modify the list during the iterations it gets all fucky if I don't iterate through the original
    # state of the list, which is why I make a shallow copy at the start and iterate through that
    tributes_list_copy = tributes_list.copy()
    for tribute in tributes_list_copy:
        # Check if the tribute has been yeeted out from the original list and whether the tribute has already
        # participated in an event
        if tribute not in tributes_list or tribute.done:
            continue

        tribute.done = True
        if type(tribute) == Party:
            events.append(party_pick_action_function(tribute))
        else:
            events.append(trib_pick_action_function(tribute))
        #events.append(pick_action_function(tribute))

        # If there is only 1 tribute left, yeet out
        if len(tributes) == 0:
            return False
        elif len(tributes) == 1 and type(tributes[0]) != Party:
            return False

    return True


def Feast():
    global tributes, events, day
    for tribute in tributes:
        tribute.done = False
    events.append("**The Feast**")
    events.append("The cornucopia is replenished with food, supplies, weapons.")

    return do_things(tributes)


def Bloodbath():
    global tributes, events
    events.append(f"**As the tributes stand on their podiums, the horn sounds.**\n")
    return do_things(tributes, Tribute.pick_random_bloodbath_action, Party.error)


def Day():
    global tributes, events, day
    for tribute in tributes:
        tribute.done = False
        tribute.asleep = False
    events.append(f"**Day {day}**\n")  # say what day it is
    return do_things(tributes, Tribute.pick_random_action, Party.pick_random_action)


def Night():
    global tributes, events, day
    for tribute in tributes:
        tribute.done = False
    events.append(f"**Night {day}**\n")
    return do_things(tributes, Tribute.pick_random_night_action, Party.pick_random_night_action)


def Cannons():
    global deadthisday, events
    cannon_shots = len(deadthisday)
    if cannon_shots == 0:
        events.append(f"\n**No cannon shots are heard.**")
    elif cannon_shots == 1:
        events.append(f"\n**1 cannon shot goes off in the distance.**")
    else:
        events.append(f"\n**{cannon_shots} cannon shots go off in the distance.**")
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

        # Day, Night, Feast and Bloodbath return False (check do_things) if they detect a winner or if everyone dies

        # if day % 7 == 0:
        #     if not Feast():
        #         event_copy = events
        #         final_stats = finish()
        #         return event_copy + final_stats

        # Yes, technically the game could be over before even the first day. Deal with it.
        if day == 1 and not Bloodbath():
            for count, event in enumerate(events):
                events[count] = correct_grammar(event)
            event_copy = events
            final_stats = finish()
            return event_copy + final_stats

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
    global numOfTributes, events, tributes, dead
    the_end = []
    if len(tributes) > 0:
        the_end.append(f"**{tributes[0].name} from District {tributes[0].district} survived the Hunger Games!**")
    else:
        the_end.append("**Everyone died! YAY!**")
    the_end.append("**Order of death**")
    for cont, tribute in enumerate(dead):  # For each dead tribute
        the_end.append(f"{((numOfTributes) - cont) - 1}: {tribute.name}")  # List the name and time of death of the tribute.

    the_end.append("**Kills**")
    dead.sort(key=lambda trib: trib.kills, reverse=True)
    for tribute in dead:
        the_end.append(f"{tribute.name} - {tribute.kills}")

    the_end.append("Finished!")
    reset()

    return the_end