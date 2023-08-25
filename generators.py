''' ------------------------------------------- IMPORTS ------------------------------------------- '''
from random import randrange as rand_randrange
from random import seed as rand_seed
from random import shuffle as rand_shuffle
from random import randchoice as rand_choice
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

MAJOR_ARCANA = [
    {
        "name": "The Fool",
        "isReversed": False,
        "upright": "New beginnings, innocence, adventure",
        "reversed": "Recklessness, fearlessness, risk",
    },{
        "name": "The Magician",
        "isReversed": False,
        "upright": "Willpower, creation, manifestation",
        "reversed": "Manipulation, illusions",
    },{
        "name": "The High Priestess",
        "isReversed": False,
        "upright": "Intuitive, unconscious, divine feminine",
        "reversed": "Repressed feelings, withdrawal, silence"
    },{
        "name": "The Empress",
        "isReversed": False,
        "upright": "Femininity, nurturing, fertility, abundance",
        "reversed": "Dependence, smothering, emptiness"
    },{
        "name": "The Emperor",
        "isReversed": False,
        "upright": "Authority, structure, a father figure",
        "reversed": "Excessive control, rigidity, domination"
    },{
        "name": "The Hierophant",
        "isReversed": False,
        "upright": "Spiritual wisdom, tradition, conformity, morality, ethics",
        "reversed": "Rebellion, subversiveness, freedom, personal beliefs"
    },{
        "name": "The Lovers",
        "isReversed": False,
        "upright": "Love, harmony, partnerships, choices",
        "reversed": "Disbalance, one-sidedness, disharmony"
    },{
        "name": "The Charoit",
        "isReversed": False,
        "upright": "Direction, control, willpower, determination, success, action",
        "reversed": "Lack of control, opposition, lack of direction, self-discipline"
    },{
        "name": "Strength",
        "isReversed": False,
        "upright": "Strength, courage, compassion, focus, persuasion, influence",
        "reversed": "Self-doubt, weakness, insecurity, low energy, raw emotion"
    },{
        "name": "The Hermit",
        "isReversed": False,
        "upright": "Wisdom, soul searching, solitude, spiritual enlightenment, receiving or giving guidance",
        "reversed": "Loneliness, isolation, paranoia, sadness, being overcome or paralyzed by fear"
    },{
        "name": "Wheel of Fortune",
        "isReversed": False,
        "upright": "Chance, destiny and fate, karma, turning points",
        "reversed": "Upheaval, lousy luck, unwelcome change, setbacks"
    },{
        "name": "Justice",
        "isReversed": False,
        "upright": "Fairness, integrity, legal disputes, cause and effect, life lessons",
        "reversed": "Injustice, dishonesty, failure to take responsibility, deceitful practices, negative karma"
    },{
        "name": "The Hanged Man",
        "isReversed": False,
        "upright": "Letting go, sacrificing, pausing to reflect, uncertainty, spiritual development",
        "reversed": "Discontentment, stagnation, negative patterns, no solution, fear of sacrifice"
    },{
        "name": "Death",
        "isReversed": False,
        "upright": "Ending of a cycle, transitions, getting rid of excess, powerful movement, resolutions",
        "reversed": "Resisting change, fear of new beginnings, dependency, repeating negative patterns"
    },{
        "name": "Temperance",
        "isReversed": False,
        "upright": "Balance, moderation, good health, cooperating with others, finding solutions",
        "reversed": "Imbalance, discord, hastiness, overindulgence, risky behavior"
    },{
        "name": "The Devil",
        "isReversed": False,
        "upright": "Material focus, trapped in bondage, addictions and depression, negative thinking, betrayal",
        "reversed": "Overcoming addiction, independence, reclaiming power, detachment, freedom"
    },{
        "name": "The Tower",
        "isReversed": False,
        "upright": "Intense and sudden change, release, painful loss, tragedy, revelation",
        "reversed": "Resisting change, avoiding tragedy, a narrow escape, delaying what is inevitable"
    },{
        "name": "The Star",
        "isReversed": False,
        "upright": "Hope, renewal, creativity and inspiration, generosity, healing",
        "reversed": "Despair, lack of hope, creative block, boredom, focusing on the negative"
    },{
        "name": "The Moon",
        "isReversed": False,
        "upright": "Fear, anxiety, confusion, delusion, risk",
        "reversed": "Overcoming fear, finding the truth, conquering anxiety, gaining clarity"
    },{
        "name": "The Sun",
        "isReversed": False,
        "upright": "Happiness, fertility, success, optimism, truth",
        "reversed": "Sadness, procrastination, pessimism, lies, failure"
    },{
        "name": "Judgement",
        "isReversed": False,
        "upright": "Reflection, inner calling, reckoning, awakening, rebirth, absolution",
        "reversed": "Feeling down, self-doubt, missing the call fearlessness"
    },{
        "name": "The World",
        "isReversed": False,
        "upright": "Fulfillment, harmony, completion, integration, travel, unity",
        "reversed": "Incompletion, shortcuts, delays, emptiness"
    }
]

MINOR_ARCANA = [
    {
        "name": "Ace of Cups",
        "inReversed": False,
        "upright": "Love, new relationships, compassion, creativity",
        "reversed": "Self-love, intuition, repressed emotions"
    },{
        "name": "Two of Cups",
        "inReversed": False,
        "upright": "Unified love, partnership, mutual attraction",
        "reversed": "Self-love, break-ups, disharmony, distrust"
    },{
        "name": "Three of Cups",
        "inReversed": False,
        "upright": "Celebration, friendship, creativity, collaborations",
        "reversed": "Independence, alone time, hardcore partying, threes-a-crowd"
    },{
        "name": "Four of Cups",
        "inReversed": False,
        "upright": "Meditation, contemplation, apathy, reevaluation",
        "reversed": "Retreat, withdrawal, checking in for alignment"
    },{
        "name": "Five of Cups",
        "inReversed": False,
        "upright": "Regret, failure, disappointment, pessimism",
        "reversed": "Personal setbacks, self-forgiveness, moving on"
    },{
        "name": "Six of Cups",
        "inReversed": False,
        "upright": "Revisiting the past, childhood memories, innocence, joy",
        "reversed": "Living in the past, forgiveness, lacking playfulness"
    },{
        "name": "Seven of Cups",
        "inReversed": False,
        "upright": "Oppertunities, choices, wishful thinking, illusion",
        "reversed": "Alignment, personal values, overwhelmed by choices"
    },{
        "name": "Eight of Cups",
        "inReversed": False,
        "upright": "Disappointment, abandonment, withdrawal, escapism",
        "reversed": "Trying one more time, indecision, aimless drifting, walking away"
    },{
        "name": "Nine of Cups",
        "inReversed": False,
        "upright": "Contentment, satisfaction, gratitude, wish come true",
        "reversed": "Inner happiness, materialism, dissatisfaction, indulgence"
    },{
        "name": "Ten of Cups",
        "inReversed": False,
        "upright": "Divine love, blissful relationships,harmony, alignment",
        "reversed": "Disconnection, misaligned values, struggling relationships"
    },{
        "name": "Page of Cups",
        "inReversed": False,
        "upright": "Creative opportunities, intuitive messages, curiousity, possibility",
        "reversed": "New ideas, doubting intuition, creative blocks, emotional immaturity"
    },{
        "name": "Knight of Cups",
        "inReversed": False,
        "upright": "Creativity, romance, charm, imagination, beauty",
        "reversed": "Overactive imagination, unrealistic, jealous, moody"
    },{
        "name": "Queen of Cups",
        "inReversed": False,
        "upright": "Compassionate, caring, emotionally stable, intuitive, in flow",
        "reversed": "Inner feelings, self-care, self-love, co-depedency"
    },{
        "name": "King of Cups",
        "inReversed": False,
        "upright": "Emotionally balanced, compassionate, diplomatic",
        "reversed": "Self=compassion, inner feelings, moodiness, emotionally manipulative"
    },{
        "name": "Ace of Pentacles",
        "isReversed": False,
        "upright": "A new finacial or career opportuinity, manifestation, abundance",
        "reversed": "Lost opportunity, lack of planning and foresight"
    },{
        "name": "Two of Pentacles",
        "isReversed": False,
        "upright": "Multiple priorities, time management, prioritisation, adaptability",
        "reversed": "Over-committed, disorganisation, reprioritisation"
    },{
        "name": "Three of Pentacles",
        "isReversed": False,
        "upright": "Teamwork, collaboration, learning, implementation",
        "reversed": "Disharmony, misalignment, working alone"
    },{
        "name": "Four of Pentacles",
        "isReversed": False,
        "upright": "Saving money, security, conservatism, scarcity, control",
        "reversed": "Over-spending, greed, self-protection"
    },{
        "name": "Five of Pentacles",
        "isReversed": False,
        "upright": "Finacial loss, poverty, lack mindset, isolation, worry",
        "reversed": ""
    },{
        "name": "Six of Pentacles",
        "isReversed": False,
        "upright": "Giving, recieving, sharing wealth, generosity, charity",
        "reversed": "Self-care, unpaid debts, one-sided charity"
    },{
        "name": "Seven of Pentacles",
        "isReversed": False,
        "upright": "Long-term view, sustainable results, perseverance, investment",
        "reversed": "Lack of long-term vision, limited success or reward"
    },{
        "name": "Eight of Pentacles",
        "isReversed": False,
        "upright": "Apprenticeship, repetitive tasks, mastery, skill development",
        "reversed": "Self-development, perfectionism, misdirected activity"
    },{
        "name": "Nine of Pentacles",
        "isReversed": False,
        "upright": "Abundance, luxury, self-sifficiency, financial independence",
        "reversed": "Self-worth, over-investment in work, hustling"
    },{
        "name": "Ten of Pentacles",
        "isReversed": False,
        "upright": "Wealth, financial security, family, long-term success, contribution",
        "reversed": "The dark side of wealth, finacial failure or loss"
    },{
        "name": "Page of Pentacles",
        "isReversed": False,
        "upright": "Manifestation, finacial opportunity, skill development",
        "reversed": "Lack of progress, procrastination, learn from failure"
    },{
        "name": "Knight of Pentacles",
        "isReversed": False,
        "upright": "Hard work, productivity, routine, conservatism",
        "reversed": "Self-discipline, boredom, feeling stuck, perfectionism"
    },{
        "name": "Queen of Pentacles",
        "isReversed": False,
        "upright": "Nurturing, practical, providing finacially, a working parent",
        "reversed": "Finacial independence, self-care, work-home conflict"
    },{
        "name": "King of Pentacles",
        "isReversed": False,
        "upright": "Wealth, business, leasdership, security, discipline, abundance",
        "reversed": ""
    },{
        "name": "Ace of Swords",
        "isReversed": False,
        "upright": "Breakthroughs, new ideas, mental clarity, success",
        "reversed": "Inner clarity, re-thinking and idea, clouded judgement"
    },{
        "name": "Two of Swords",
        "isReversed": False,
        "upright": "Difficult decisions, weighing up options, animpasse, avoidance",
        "reversed": "Indecision, confusion, information overload, stalemate"
    },{
        "name": "Three of Swords",
        "isReversed": False,
        "upright": "Heartbreak, emotional pain, sorrow, grief, hurt",
        "reversed": "Negative self-talk, releasing pain, optimism, forgiveness"
    },{
        "name": "Four of Swords",
        "isReversed": False,
        "upright": "Rest, relaxation, meditation, contemplation, recuperation",
        "reversed": "Exhaustion, burn-out, deep contemplation, stagnation"
    },{
        "name": "Five of Swords",
        "isReversed": False,
        "upright": "Conflict, disagreements, competition, defeat, winning at all costs",
        "reversed": "Reconciliation, making amends, past resentment"
    },{
        "name": "Six of Swords",
        "isReversed": False,
        "upright": "Transition, change, rite of passage, releasing baggage",
        "reversed": "Personal transition, resistance to change, unfinished business"
    },{
        "name": "Seven of Swords",
        "isReversed": False,
        "upright": "Betrayal, deception, getting away with something, acting strategically",
        "reversed": "Imposter syndrome, self deceit, keeping secrets"
    },{
        "name": "Eight of Swords",
        "isReversed": False,
        "upright": "Negative thoughts, self-imposed restriction, imprisonment, victim mentality",
        "reversed": "Self-limiting beliefs, inner critic, releasing negative thoughts, open to new perspectives"
    },{
        "name": "Nine of Swords",
        "isReversed": False,
        "upright": "Anxiety, worry, fear, depression, nightmares",
        "reversed": "Inner turmoil, deep-seated fears, secrets, releasing worry"
    },{
        "name": "Ten of Swords",
        "isReversed": False,
        "upright": "Painful endings, deep wounds, betrayal, loss, crisis",
        "reversed": "Recovery, regeneration, resisting an inevitable end"
    },{
        "name": "Page of Swords",
        "isReversed": False,
        "upright": "New ideas, curiosity, thirst for knowledge, new ways of communicating",
        "reversed": "Self-expression, all talk and no action, haphazard action, haste"
    },{
        "name": "Knight of Swords",
        "isReversed": False,
        "upright": "Ambitious, action-oriented, driven to succeed, fast-thinking",
        "reversed": "Restless, unfocused, impulsive, burn-out"
    },{
        "name": "Queen of Swords",
        "isReversed": False,
        "upright": "Independent, unbiased judgment, clear boundaries, direct communication",
        "reversed": "Overly-emotional, easily influenced, bitchy, cold-hearted"
    },{
        "name": "King of Swords",
        "isReversed": False,
        "upright": "Mental clarity, intellectual power, authority, truth",
        "reversed": "Quiet power, inner truth, misuse of power, manipulation"
    },{
        "name": "Ace of Wands",
        "isReversed": False,
        "upright": "Inspiration, new opportunitues, growth, potential",
        "reversed": "An emerging idea, lack of direction, distractions, delays"
    },{
        "name": "Two of Wands",
        "isReversed": False,
        "upright": "Future planning, progress, decisions, discovery",
        "reversed": "Personal goals, inner alignment, fear of unknown, lack of planning"
    },{
        "name": "Three of Wands",
        "isReversed": False,
        "upright": "Progress, expansion, foresight, overseas opportunities",
        "reversed": "Playing small, lack of foresight, unexpected delay"
    },{
        "name": "Four of Wands",
        "isReversed": False,
        "upright": "Celebration, joy, harmony, relaxation, homecoming",
        "reversed": "Personal celebration, inner harmony, conflict with others, transition"
    },{
        "name": "Five of Wands",
        "isReversed": False,
        "upright": "Conflict, disagreements, competition, tension, diversity",
        "reversed": "Inner conflict, conflict avoidance, tension release"
    },{
        "name": "Six of Wands",
        "isReversed": False,
        "upright": "Success, public recognition, progress, self-confidence",
        "reversed": "Private achievement, personal definition of success, fall from grace egotism"
    },{
        "name": "Seven of Wands",
        "isReversed": False,
        "upright": "Challenge, competition, protection, perseverance",
        "reversed": "Exhaustion, giving up, overwhelmed"
    },{
        "name": "Eight of Wands",
        "isReversed": False,
        "upright": "Movement, fast paced change, action, alignment, air travel",
        "reversed": "Delays, frustration, resisting change, internal alignment"
    },{
        "name": "Nine of Wands",
        "isReversed": False,
        "upright": "Resilience, courage, persistence, test of faith, bounderaries",
        "reversed": "Inner resources, struggle, overwhelm, defensive, paranoia"
    },{
        "name": "Ten of Wands",
        "isReversed": False,
        "upright": "Burden, extra responsibility, hard work, completion",
        "reversed": "Doing it all, carrying the burden, delegation, release"
    },{
        "name": "Page of Wands",
        "isReversed": False,
        "upright": "Inspiration, ideas, discovery, limitless potential, free spirit",
        "reversed": "Newly-formed ideas, redirecting energy, self-limiting beliefs, a spiritual path"
    },{
        "name": "Knight of Wands",
        "isReversed": False,
        "upright": "Energy, passion, inspired action, adventure, impulsiveness",
        "reversed": "Passion project, hast, scattered energy, delays, frustration"
    },{
        "name": "Queen of Wands",
        "isReversed": False,
        "upright": "Courage, confidence, independence, social butterfly, determination",
        "reversed": "Self-respect, self-confidence, introverted, re-establish sense of self"
    },{
        "name": "King of Wands",
        "isReversed": False,
        "upright": "Natural-born leader, vision, entrepreneur, honour",
        "reversed": "Impulsiveness, haste, ruthless, high expectations"
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
    
def create_standard_deck() -> list:
    values= ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suit = {"spade": "\u2660", "club": "\u2663", "heart": '\u2661', 'diamond': '\u2662'}
    deck = []
    for k in suit.keys():
        for v in values:
            deck.append(str(v) + str(suit[k]))
    rand_shuffle(deck)
    return deck

def create_domt_deck() -> list:
    deck = DECK_OF_MANY_THINGS
    rand_shuffle(deck)
    return deck

def create_tarot_major() -> list:
    deck = MAJOR_ARCANA
    rand_shuffle(deck)
    for card in deck:
        card["isReversed"] = rand_choice([True, False])
    return deck

def create_tarot_minor() -> list:
    deck = MINOR_ARCANA
    rand_shuffle(deck)
    for card in deck:
        card["isReversed"] = rand_choice([True, False])
    return deck

def create_tarot_full() -> list:
    deck = MAJOR_ARCANA + MINOR_ARCANA
    rand_shuffle(deck)
    for card in deck:
        card["isReversed"] = rand_choice([True, False])
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