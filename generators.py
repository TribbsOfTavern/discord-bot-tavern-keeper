''' ------------------------------------------- IMPORTS ------------------------------------------- '''
from random import randrange
from random import seed
from random import shuffle
from re import match as re_match

''' ------------------------------------------- CONSTANTS ------------------------------------------- '''
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

seed()
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
        res['rolls'].append(randrange(1, side+1))
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
    shuffle(deck)
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
        char_race = list(PHB_RACES)[randrange(len(PHB_RACES)-1)]
        # Random Class
        char_class = list(PHB_CLASSES)[randrange(len(PHB_CLASSES))]
        # Random Background
        char_background = list(PHB_BACKGROUNDS)[randrange(0, len(PHB_BACKGROUNDS))]
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
        if char_race == None: char_race = list(PHB_RACES)[randrange(len(PHB_RACES)-1)]
        if char_class == None: char_class = list(PHB_CLASSES)[randrange(len(PHB_CLASSES))]
        if char_level == 0: char_level = 1
        if char_background == None: char_background = list(PHB_BACKGROUNDS)[randrange(0, len(PHB_BACKGROUNDS))]
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