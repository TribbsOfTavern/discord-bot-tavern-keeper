''' ------------------------------------------- IMPORTS ------------------------------------------- '''
from random import randrange as rand_randrange
from random import seed as rand_seed
from random import shuffle as rand_shuffle
from re import match as re_match

''' ------------------------------------------- CONSTANTS ------------------------------------------- '''
# TODO -- This is all going to be moved over to a MongoDB table.
# TODO -- Figure out a way to implement ALT options
PHB_RACES = {
    "human": {
        "stats":{ "STR": 0, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 0}
    },
    "elf": {
        "stats":{ "STR": 0, "DEX": 2, "CON": 0, "INT": 0, "WIS": 0, "CHA": 0}
    },
    "half-elf": {
        "stats": {"STR": 0, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 2, "ALT": "+1 in two seperate stats of choice"}
    },
    "gnome": {
        "stats":{ "STR": 0, "DEX": 0, "CON": 0, "INT": 2, "WIS": 0, "CHA": 0}
    }, 
    "halfling": {
        "stats":{ "STR": 0, "DEX": 2, "CON": 0, "INT": 0, "WIS": 0, "CHA": 0}
    },
    "dwarf": {
        "stats":{ "STR": 0, "DEX": 0, "CON": 2, "INT": 0, "WIS": 0, "CHA": 0}
    },
    "dragonborn": {
        "stats":{ "STR": 2, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 1}
    },
    "half-orc": {
        "stats":{ "STR": 2, "DEX": 0, "CON": 1, "INT": 0, "WIS": 0, "CHA": 0}
    },
    "tiefling": {
        "stats":{ "STR": 0, "DEX": 0, "CON": 0, "INT": 1, "WIS": 0, "CHA": 2
        }
    }
}

PHB_CLASSES = {
    "barbarian": {
        "hit_die": "1d12",
        "start_gold": "2d4",
        "multiplier": 10
    },
    "bard": {
        "hit_die": "1d8",
        "start_gold": "1d8",
        "multiplier": 10
    },
    "cleric": {
        "hit_die": "1d8",
        "start_gold": "1d8",
        "multiplier": 10
    },
    "druid": {
        "hit_die": "1d8",
        "start_gold": "1d8",
        "multiplier": 10
    },
    "fighter": {
        "hit_die": "1d10",
        "start_gold": "5d4",
        "multiplier": 10
    },
    "monk": {
        "hit_die": "1d8",
        "start_gold": "5d4",
        "multiplier": 1
    },
    "paladin": {
        "hit_die": "1d10",
        "start_gold": "5d4",
        "multiplier": 10
    },
    "ranger": {
        "hit_die": "1d10",
        "start_gold": "5d4",
        "multiplier": 10
    },
    "rogue": {
        "hit_die": "1d8",
        "start_gold": "4d4",
        "multiplier": 10
    },
    "sorcerer": {
        "hit_die": "1d6",
        "start_gold": "3d4",
        "multiplier": 10
    },
    "warlock": {
        "hit_die": "1d8",
        "start_gold": "4d4",
        "multiplier": 10
    },
    "wizard": {
        "hit_die": "1d6",
        "start_gold": "4d4",
        "multiplier": 10
    }
}

PHB_BACKGROUNDS = [
    "acolyte",
    "charlatan",
    "criminal",
    "entertainer",
    "folk hero",
    "guild artisan",
    "hermit",
    "noble",
    "outlander",
    "sage",
    "sailor",
    "soldier",
    "urchin"
]

DECK_OF_MANY_THINGS = [
    {
        "name": "Vizier",
        "card": "Ace of Diamonds",
        "text": "At any time you choose within one year of drawing this card, you can ask a question in meditation and mentally receive a truthful answer to that question. Besides information, the answer helps you solve a puzzling problem or other dilemma. In other words, the knowledge comes with wisdom on how to apply it."
    },{
        "name": "Sun",
        "card": "King of Diamonds", 
        "text": "You gain 50,000 XP, and a wondrous item (which the DM determines randomly) appears in your hands."
    },{
        "name": "Moon",
        "card": "Queen of Diamonds",
        "text": "You are granted the ability to cast the wish spell 1d3 times."
    },{
        "name": "Star",
        "card": "Jack of Diamonds",
        "text": "Increase one of your ability scores by 2. The score can exceed 20 but can't exceed 24."
    },{
        "name": "Comet",
        "card": "Two of Diamonds",
        "text": "If you single-handedly defeat the next hostile monster or group of monsters you encounter, you gain experience points enough to gain one level. Otherwise, this card has no effect."
    },{
        "name": "The Fates",
        "card": "Ace of Hearts",
        "text": "Reality's fabric unravels and spins anew, allowing you to avoid or erase one event as if it never happened. You can use the card's magic as soon as you draw the card or at any other time before you die."
    },{
        "name": "Throne",
        "card": "King of Hearts",
        "text": "You gain proficiency in the Persuasion skill, and you double your proficiency bonus on checks made with that skill. In addition, you gain rightful ownership of a small keep somewhere in the world. However, the keep is currently in the hands of monsters, which you must clear out before you can claim the keep as. yours."
    },{
        "name": "Key",
        "card": "Queen of Hearts",
        "text": "A rare or rarer magic weapon with which you are proficient appears in your hands. The DM chooses the weapon."
    },{
        "name": "Knight",
        "card": "Jack of Hearts",
        "text": "You gain the service of a 4th-level fighter who appears in a space you choose within 30 feet of you. The fighter is of the same race as you and serves you loyally until death, believing the fates have drawn him or her to you. You control this character."
    },{
        "name": "Gem",
        "card": "Two of Hearts",
        "text": "Twenty-five pieces of jewelry worth 2,000 gp each or fifty gems worth 1,000 gp each appear at your feet."
    },{
        "name": "Talons",
        "card": "Ace of Clubs",
        "text": "You gain proficiency in the Persuasion skill, and you double your proficiency bonus on checks made with that skill. In addition, you gain rightful ownership of a small keep somewhere in the world. However, the keep is currently in the hands of monsters, which you must clear out before you can claim the keep as. yours."
    },{
        "name": "The Void",
        "card": "King of Clubs",
        "text": "This black card spells disaster. Your soul is drawn from your body and contained in an object in a place of the DM's choice. One or more powerful beings guard the place. While your soul is trapped in this way, your body is incapacitated. A wish spell can't restore your soul, but the spell reveals the location of the object that holds it. You draw no more cards."
    },{
        "name": "Flames",
        "card": "Queen of Clubs",
        "text": "A powerful devil becomes your enemy. The devil seeks your ruin and plagues your life, savoring your suffering before attempting to slay you. This enmity lasts until either you or the devil dies."
    },{
        "name": "Skull",
        "card": "Jack of Clubs",
        "text": "You summon an avatar of death-a ghostly humanoid skeleton clad in a tattered black robe and carrying a spectral scythe. It appears in a space of the DM's choice within 10 feet of you and attacks you, warning all others that you must win the battle alone. The avatar fights until you die or it drops to 0 hit points, whereupon it disappears. If anyone tries to help you, the helper summons its own avatar of death. A creature slain by an avatar of death can't be restored to life."
    },{
        "name": "Idiot",
        "card": "Two of Clubs",
        "text": ""
    },{
        "name": "Donjon",
        "card": "Ace of Spades",
        "text": "You disappear and become entombed in a state of suspended animation in an extradimensional sphere. Everything you were wearing and carrying stays behind in the space you occupied when you disappeared. You remain imprisoned until you are found and removed from the sphere. You can't be located by any divination magic, but a wish spell can reveal the location of your prison. You draw no more cards."
    },{
        "name": "Ruin",
        "card": "King of Spades",
        "text": "Permanently reduce your Intelligence by 1d4 + 1 (to a minimum score of 1). You can draw one additional card beyond your declared draws."
    },{
        "name": "Euryale",
        "card": "Queen of Spades",
        "text": "The card's medusa-like visage curses you. You take a -2 penalty on saving throws while cursed in this way. Only a god or the magic of The Fates card can end this curse."
    },{
        "name": "Rogue",
        "card": "Jack of Spades",
        "text": "A nonplayer character of the DM's choice becomes hostile toward you. The identity of your new enemy isn't known until the NPC or someone else reveals it. Nothing less than a wish spell or divine intervention can end the NPC's hostility toward you."
    },{
        "name": "Balance",
        "card": "Two of Spades",
        "text": "Your mind suffers a wrenching alteration, causing your alignment to change. Lawful becomes chaotic, good becomes evil, and vice versa. If you are true neutral or unaligned, this card has no effect on you."
    },{
        "name": "Fool",
        "card": "Joker with Trademark",
        "text": "You lose 10,000 XP, discard this card, and draw from the deck again, counting both draws as one of your declared draws. If losing that much XP would cause you to lose a level, you instead lose an amount that leaves you with just enough XP to keep your level."
    },{
        "name": "Jester",
        "card": "Joker without Trademark",
        "text": "You gain 10,000 XP, or you can draw two additional cards beyond your declared draws."
    }
]

rand_seed()
''' ------------------------------------------- UTILITY FUNCTIONS ------------------------------------------- '''
def roll_dn(roll:str) -> dict:
    dice = None
    side = None
    kept = None
    high = False
    res = {'rolls': [], "kept": None, 'dropped': None}
    
    # if s = '4d6kh3' then s[0:d] is dice | s[d:k] is side | s[h or l:] is kept
    if 'k' in roll:
        dice = int(roll[:roll.find('d')])
        side = int(roll[roll.find('d')+1:roll.find('k')])
        kept = int(roll[roll.find('k')+2:])
        high = True if 'kh' in roll else False
    else:
        dice = int(roll[:roll.find('d')])
        side = int(roll[roll.find('d')+1:])
    
    # Roll the dice
    for i in range(dice):
        res['rolls'].append(rand_randrange(1, side+1))
    # if we are keeping certain ones
    if 'k' in roll:
        # are we keeping high
        if high:
            res['kept'] = sorted(res['rolls'])[:len(res['rolls'])-(1+kept):-1]
            res['dropped'] = sorted(res['rolls'])[(len(res['rolls'])-1-kept)::-1]
        # or low
        else:
            res['kept'] = sorted(res['rolls'])[:kept]
            res['dropped'] = sorted(res['rolls'])[:-(len(res['rolls'])-kept+1):-1]
    else:
        res['kept'] = res['rolls']

    return res

def is_valid_roll(roll:str) -> bool:
    pattern = '^\d+d\d+kh\d+$|^\d+d\d+kl\d+$|^\d+d\d+$'
    if re_match(pattern, roll) != None: return True
    else: return False

def get_abs_modifier(i:int) -> int:
    if i == 30: return 10
    elif i >= 28: return 9
    elif i >= 26: return 8
    elif i >= 24: return 7
    elif i >= 22: return 6
    elif i >= 20: return 5
    elif i >= 18: return 4
    elif i >= 16: return 3
    elif i >= 14: return 2
    elif i >= 12: return 1
    elif i >= 10: return 0
    elif i >= 8: return -1
    elif i >= 6: return -2
    elif i >= 4: return -3
    elif i >= 2: return -4
    elif i == 1: return -5
    
def create_deck() -> list:
    values= ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suit = {"spade": "\u2660", "club": "\u2663", "heart": '\u2661', 'diamond': '\u2662'}
    deck = []
    for k in suit.keys():
        for v in values:
            deck.append(str(v) + str(suit[k]))
    rand_shuffle(deck)
    return deck
    
''' ------------------------------------------- GENERATOR FUNCTIONS ------------------------------------------- '''
def generate_character(opts:list) -> dict:
    char_race =         None
    char_class =        None
    char_level =        0
    char_background =   None
    char_start_gold =   None
    char_stat_rolls =   {"STR": 0, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 0}
    char_stat_bonus =   {"STR": 0, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 0}
    char_stat_modifier ={"STR": 0, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 0}
    char_hp_rolls =     []
    char_hp =           0
                        
    if opts == [] or opts == None:
        # Random Race
        char_race = list(PHB_RACES)[rand_randrange(len(PHB_RACES)-1)]
        # Random Class
        char_class = list(PHB_CLASSES)[rand_randrange(len(PHB_CLASSES))]
        # Random Background
        char_background = list(PHB_BACKGROUNDS)[rand_randrange(0, len(PHB_BACKGROUNDS))]
        # Random Stats
        for k in char_stat_rolls.keys():
            roll = roll_dn('3d6')
            char_stat_rolls[k] = roll['kept']
        # Level 1
        char_level = 1
    else:
        # Set what opts are available
        for e in opts:
            if e.startswith('race='):
                if e[e.find('=')+1:].lower() in PHB_RACES: char_race = e[e.find('=')+1:].lower()  
            elif e.startswith('class='):
                if e[e.find('=')+1:].lower() in PHB_CLASSES: char_class = e[e.find('=')+1:].lower() 
            elif e.startswith('level='):                                       
                if e[e.find('=')+1:].isdigit(): char_level = int(e[e.find('=')+1:])
            elif e.startswith('background='):
                if e[e.find('=')+1:].lower() in PHB_BACKGROUNDS: char_background = e[e.find('=')+1:].lower() 
            elif e.startswith('rolls='):
                if is_valid_roll(e[e.find('=')+1:]):
                    for k in char_stat_rolls.keys():
                        roll = roll_dn(e[e.find('=')+1:])
                        char_stat_rolls[k] = roll['kept']
                    

        # If character traits are still None then give them random traits
        if char_race == None: char_race = list(PHB_RACES)[rand_randrange(len(PHB_RACES)-1)]
        if char_class == None: char_class = list(PHB_CLASSES)[rand_randrange(len(PHB_CLASSES))]
        if char_level == 0: char_level = 1
        if char_background == None: char_background = list(PHB_BACKGROUNDS)[rand_randrange(0, len(PHB_BACKGROUNDS))]
        if char_stat_rolls == {"STR": 0, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 0}:
            for k in char_stat_rolls.keys():
                roll = roll_dn('3d6')
                char_stat_rolls[k] = roll['kept']
    
    # All this can happen after the fact
    # Assign Racial Bonuses
    for k in char_stat_bonus.keys():
        char_stat_bonus[k] = PHB_RACES[char_race]['stats'][k]
    # Set Stat Modifiers
    for k in char_stat_modifier.keys():
        char_stat_modifier[k] = get_abs_modifier(sum(char_stat_rolls[k]) + char_stat_bonus[k])
    # Roll Starting HP
    for i in range(char_level):
        roll = roll_dn(PHB_CLASSES[char_class]['hit_die'])
        char_hp_rolls.append(sum(roll['kept']))
        char_hp += (sum(roll['kept']) + char_stat_modifier['CON']) if (sum(roll['kept']) + char_stat_modifier['CON']) >= 1 else 1
    # Give Starting Gold
    roll = roll_dn(PHB_CLASSES[char_class]['start_gold'])
    char_start_gold = sum(roll['kept']) * PHB_CLASSES[char_class]['multiplier']

    character = {
        "race": char_race,
        "class": char_class,
        "level": char_level,
        "background": char_background,
        "gold": char_start_gold,
        "abs_rolls": char_stat_rolls,
        "abs_bonuses": char_stat_bonus,
        "abs_modifiers": char_stat_modifier,
        "hp_rolls": char_hp_rolls,
        "hp": char_hp
    }
    
    return character