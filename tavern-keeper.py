import secrets as secret    # Keeping my secrets secret
import generators as dnd    # DnD generators
import dndMongo as db       # DnD MongoDB tables connection, setters/getters
import random               # Python lib
import json                 # Python lib
import asyncio              # Python lib
import discord              # python3 -m pip install -U discord.py OR discord.py[Voice] 
from discord.ext import commands, tasks # Comes with above lib

##
# discord.py lib DOCS -> https://discordpy.readthedocs.io/en/stable/api.html
##

# -------------------------- Variables -------------------------- #
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

description = '''    Tavern Keeper Bot was created specifically for The Tavern.    '''
bot = commands.Bot(command_prefix='!', description=description, intents=intents, activity=discord.Game(name="!help to see commands"))
bot_db = db.DB('localhost', 27017, 'rpg-tables')    #DB obj
config_name = 'config.json' # Name of the config file to use, if not found one will be created
config = None       # This will load in on startup
autosave_time = 300 # time in second for how often autosave should occure for config

# Views ----------------------------------------------------- #
class viewItem(discord.ui.View):
    def __init__(self, info:dict):
        super().__init__()
        self.info = info
    
    @discord.ui.button(label='Info', style=discord.ButtonStyle.primary)
    async def button_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        res = f'**{self.info["Name"]}**\n'
        res += f'{self.info["Rarity"]}-{self.info["Type"]}\n'
        res += f'' if self.info['Attunement'] == '' else f'**Attunement:** {self.info["Attunement"]}\n'
        res += f'**Weight:** --\t\t' if self.info['Weight'] == '' else f'**Weight:** {self.info["Weight"]}\t\t'
        res += f'**Value:** --\t\t' if self.info['Value'] == '' else f'**Value:** {self.info["Value"]}\n'
        res += f'**Properties:** --\n' if self.info['Properties'] == '' else f'**Properties:** {self.info["Properties"]}\n'
        await interaction.response.edit_message(content=res)
    
    @discord.ui.button(label="Description", style=discord.ButtonStyle.primary)
    async def button_description(self, interaction: discord.Interaction, button: discord.ui.Button):
        res = f'**{self.info["Name"]}**\n'
        res += f'{self.info["Text"][0:2000]}' # stupid max character rate
        await interaction.response.edit_message(content=res)
        
class viewSpell(discord.ui.View):
    def __init__(self, info:dict):
        super().__init__()
        self.info = info
        
    @discord.ui.button(label="Info", style=discord.ButtonStyle.primary)
    async def button_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        res = f'**Name: {self.info["Name"]}**\n'
        res += f'**Level:** {self.info["Level"]}\t\t**Cast Time:** {self.info["casting-time"]}\t\t**Duration:** {self.info["Duration"]}\n'
        res += f'**School:** {self.info["School"]}\t\t**Range:** {self.info["Range"]}\t\t**Components:** {self.info["Components"]}\n'
        await interaction.response.edit_message(content=res[0:2000])
        
    @discord.ui.button(label="Description", style=discord.ButtonStyle.primary)
    async def button_description(self, interaction: discord.Interaction, button: discord.ui.Button):
        res = f'**Name: {self.info["Name"]}**\n'
        res += f'\t{self.info["Text"]}\n'
        await interaction.response.edit_message(content=res[0:2000])

    @discord.ui.button(label="Higher Levels", style=discord.ButtonStyle.primary)
    async def button_higher(self, interaction: discord.Interaction, button: discord.ui.Button):
        res = f'**Name: {self.info["Name"]}**\n'
        res += f'--' if self.info["at-higher-levels"] == '' else f'\t* **At Higher Levels:**{self.info["at-higher-levels"]}*'
        await interaction.response.edit_message(content=res[0:2000])

class viewMonster(discord.ui.View):
    def __init__(self, info):
        super().__init__()
        self.info = info

    @discord.ui.button(label="Info", style=discord.ButtonStyle.primary)
    async def button_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        res = f'## __{self.info["Name"]}__\t\tCR: {self.info["CR"]}\n>'
        res += f'' if self.info["Environment"] else f'**Environment:** {self.info["Environment"]}\n'
        res += f'*{self.info["Size"]} {self.info["Type"]} generally {self.info["Alignment"]}*\n'
        res += f'**HP:** {self.info["HP"]}\t\tAC: {self.info["AC"]}\n'
        res += f'**Speed:** {self.info["Speed"]}\n'
        res += f'**STR:** {self.info["Strength"]}\t\t**DEX:** {self.info["Dexterity"]}\t\t**CON:** {self.info["Constitution"]}\n'
        res += f'**INT:** {self.info["Intelligence"]}\t\t**WIS:** {self.info["Wisdom"]}\t\t**CHA:** {self.info["Charisma"]}\n'
        res += f'**Senses:** --' if self.info["Senses"] == '' else f'**Senses:** {self.info["Senses"]}\n'
        res += f'' if self.info["Skills"] == '' else f'**Skills:** {self.info["Skills"]}\n'
        res += f'' if self.info["Saving Throws"] == '' else f'**Saving Throws:** {self.info["Saving Throws"]}\n'
        res += f'' if self.info["Languages"] == '' else f'**Languages:** {self.info["Languages"]}\n'
        res += f'' if self.info["Damage Vulnerabilities"] == '' else f'**Damage Vulnerabilities:** {self.info["Damage Vulnerabilities"]}\n'
        res += f'' if self.info["Damage Resistances"] == '' else f'**Damage Resistances:** {self.info["Damage Resistances"]}\n'
        res += f'' if self.info["Damage Immunities"] == '' else f'**Damage Immunities:** {self.info["Damage Immunities"]}\n'
        res += f'' if self.info["Condition Immunities"] == '' else f'**Condition Immunities:** {self.info["Condition Immunities"]}\n'
        await interaction.response.edit_message(content=res)
        
    @discord.ui.button(label="Actions", style=discord.ButtonStyle.primary)
    async def button_actions(self, interaction: discord.Interaction, button: discord.ui.Button):
        res = f'## __{self.info["Name"]}__\n'
        res += '' if self.info['Actions'] == '' else f'**Actions**:\n> {self.info["Actions"]}\n\n'
        res += '' if self.info['Bonus Actions'] == '' else f'**Bonus Actions:\n> {self.info["Bonus Actions"]}\n\n'
        res += '' if self.info['Reactions'] == '' else f'**Reactions:\n> {self.info["Reactions"]}\n'
        await interaction.response.edit_message(content=res)
        
    @discord.ui.button(label="Traits", style=discord.ButtonStyle.primary)
    async def button_description(self, interaction: discord.Interaction, button: discord.ui.Button):
        res = f'## __{self.info["Name"]}__\n'
        res += f'{self.info["Traits"]}'
        await interaction.response.edit_message(content=res)
        
    @discord.ui.button(label="Special", style=discord.ButtonStyle.primary)
    async def button_special(self, interaction: discord.Interaction, button):
        if self.info["Legendary Actions"] == '' and self.info["Mythic Actions"] == '' and self.info["Lair Actions"] == '' and self.info["Regional Effects"] == '':
            res = f'## __{self.info["Name"]}__\n'
            res += f'There is nothing here.'
        else: 
            res = f'## __{self.info["Name"]}__\n'
            res += f'' if self.info["Legendary Actions"] == '' else f'**Legendary Actions:**\n>{self.info["Legendary Actions"]}\n\n'
            res += f'' if self.info["Mythic Actions"] == '' else f'**Mythic Actions:**\n>{self.info["Mythic Actions"]}\n\n'
            res += f'' if self.info["Lair Actions"] == '' else f'**Lair Actions:**\n>{self.info["Lair Actions"]}\n\n'
            res += f'' if self.info["Regional Effects"] == '' else f'**Regional Effects:**\n>{self.info["Regional Effects"]}\n\n'
        await interaction.response.edit_message(content=res)

# General Commands ------------------------------------------ #
@bot.event
async def on_ready() -> None:
    print('- - - - - - - - - - - - - -')
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'Connected to {len(bot.guilds)} guilds.')
    print('- - - - - - - - - - - - - -')
    global config
    config = loadConfig(config_name)
    AutoSaveConfig.start()    

@bot.command()
async def ping(ctx) -> None:
    """ Call and return, returns pong!"""
    await bot_send(ctx, "pong!")
    
@bot.command()
async def roll(ctx, roll:str = commands.parameter(default='1d20', description='roll of the dice')) -> None:
    """ Roll dice. 
        standard roll   3d6
        keep highest    2d20kh1
        keep lowest     2d20kl1
    """
    res = None
    try: 
        if dnd.is_valid_roll(roll):
            res = dnd.roll_dn(roll)
    except:
        pass
    if res != None:
        if res['dropped'] == None:
            await bot_send(ctx, f"{ctx.author.display_name} rolled {roll} *{res['rolls']}* for **{sum(res['rolls'])}**")
        elif res['dropped'] != None:
            await bot_send(ctx, f"{ctx.author.display_name} rolled {roll} for {res}")
    
@bot.command()
async def roll_character(ctx, *args) -> None:
    """ Generate a character.
        With no options, this will generate a level 1 character with random options and stats rolled as 3d6.
        level=      sets level. Invalid returns level 1
        class=      sets class. Invalid return random class
        race=       sets race. Invalid returns random race
        background= sets background. Invalid returns random background
        rolls=      style for rolling stats (standard 3d6 or 4d6kh3). Invalid returns 3d6 rolls
    """
    if args == (): character = dnd.generate_character(None)
    else: character = dnd.generate_character(list(args))

    result = f'## {ctx.author.display_name} Generated A Character\n'
    result += f'__**Race**__: {character["race"].title()}\t\t__**Class**__: {character["class"].title()}\n'
    result += f'__**Background**__: {character["background"].title()}\n'
    result += f'__**Level**__: {character["level"]}\t\t__**HP**__: {character["hp"]}\n'
    result += f'__**Starting Gold**__: {character["gold"]}\n'
    result += f'__            STATS            __\n'
    result += f'**STR**: {sum(character["abs_rolls"]["STR"]) + character["abs_bonuses"]["STR"]}\t\t'
    result += f'**DEX**: {sum(character["abs_rolls"]["DEX"]) + character["abs_bonuses"]["DEX"]}\t\t'
    result += f'**CON**: {sum(character["abs_rolls"]["CON"]) + character["abs_bonuses"]["CON"]}\t\t\n'
    result += f'**INT**: {sum(character["abs_rolls"]["INT"]) + character["abs_bonuses"]["INT"]}\t\t'
    result += f'**WIS**: {sum(character["abs_rolls"]["WIS"]) + character["abs_bonuses"]["WIS"]}\t\t'
    result += f'**CHA**: {sum(character["abs_rolls"]["CHA"]) + character["abs_bonuses"]["CHA"]}\t\t\n'
    await bot_send(ctx, result)

@bot.command()
async def spell(ctx, *args) -> None:
    """ Get information pertaining to a spell
        Ex. !spell 'Acid Splash'
        Ex. !spell 'Magic Missle'
    """
    item = bot_db.get_item_from('spells-5e', {"Name": {'$regex': f'^{(" ".join(args)).replace("+", "[+]")}', "$options": "i"}})
    if item != None:
        res = f'**Name: {item["Name"]}**\n'
        res += f'**Level:** {item["Level"]}\t\t**Cast Time:** {item["casting-time"]}\t\t**Duration:** {item["Duration"]}\n'
        res += f'**School:** {item["School"]}\t\t**Range:** {item["Range"]}\t\t**Components:** {item["Components"]}\n'
        await bot_send(ctx, res, None, viewSpell(item))
    else:
        await bot_send(ctx, f'No spell was found for {" ".join(args)}')
    
@bot.command()
async def item(ctx, *args) -> None:
    """ Get information pertaining to an item
        Ex. !item +1 Armor
        Ex. !item Bag of Tricks
    """
    item = bot_db.get_item_from('items-5e', {"Name": {'$regex': f'{(" ".join(args)).replace("+", "[+]")}', "$options": "i"}})
    if item != None:
        res = f'**{item["Name"]}**\n'
        res += f'{item["Rarity"]}-{item["Type"]}\n'
        res += f'' if item['Attunement'] == '' else f'**Attunement:** {item["Attunement"]}\n'
        res += f'**Weight:** --\t\t' if item['Weight'] == '' else f'**Weight:** {item["Weight"]}\t\t'
        res += f'**Value:** --\t\t' if item['Value'] == '' else f'**Value:** {item["Value"]}\n'
        res += f'**Properties:** --\n' if item['Properties'] == '' else f'**Properties:** {item["Properties"]}\n'
        await bot_send(ctx, res, None, viewItem(item))
    else:
        await bot_send(ctx, f'Item not found for {" ".join(args)}')

@bot.command()
async def monster(ctx, *args) -> None:
    """ Get information pertaining to a monster
        Ex. !monster 'Goblin'
        Ex. !monster 'Green Hag'
    """
    info = bot_db.get_item_from('monsters-5e', {"Name": {'$regex': f'{(" ".join(args)).replace("+", "[+]")}', "$options": "i"}})
    if info != None:
        res = f'## __{info["Name"]}__\t\tCR: {info["CR"]}\n>'
        res += f'' if info["Environment"] else f'**Environment:** {info["Environment"]}\n'
        res += f'*{info["Size"]} {info["Type"]} generally {info["Alignment"]}*\n'
        res += f'**HP:** {info["HP"]}\t\tAC: {info["AC"]}\n'
        res += f'**Speed:** {info["Speed"]}\n'
        res += f'**STR:** {info["Strength"]}\t\t**DEX:** {info["Dexterity"]}\t\t**CON:** {info["Constitution"]}\n'
        res += f'**INT:** {info["Intelligence"]}\t\t**WIS:** {info["Wisdom"]}\t\t**CHA:** {info["Charisma"]}\n'
        res += f'**Senses:** --' if info["Senses"] == '' else f'**Senses:** {info["Senses"]}\n'
        res += f'' if info["Skills"] == '' else f'**Skills:** {info["Skills"]}\n'
        res += f'' if info["Saving Throws"] == '' else f'**Saving Throws:** {info["Saving Throws"]}\n'
        res += f'' if info["Languages"] == '' else f'**Languages:** {info["Languages"]}\n'
        res += f'' if info["Damage Vulnerabilities"] == '' else f'**Damage Vulnerabilities:** {info["Damage Vulnerabilities"]}\n'
        res += f'' if info["Damage Resistances"] == '' else f'**Damage Resistances:** {info["Damage Resistances"]}\n'
        res += f'' if info["Damage Immunities"] == '' else f'**Damage Immunities:** {info["Damage Immunities"]}\n'
        res += f'' if info["Condition Immunities"] == '' else f'**Condition Immunities:** {info["Condition Immunities"]}\n'
        await bot_send(ctx, res, None, view=viewMonster(info))
    else:
        await bot_send(ctx, f'No record found for monster {" ".join(args)}', None, None)
    
@bot.command()
async def draw(ctx, *args) -> None:
    """ Draws a number of random cards from the server deck.
        Ex. !draw will return a single card from the server deck.
        Ex. !draw 1 will return a single card from the server deck.
        Ex. !draw 3 will return three cards from the server deck.
        Limited to drawing 1 to 52 cards.
    """
    global config
    args = list(args)
    try:
        if args == [] or int(args[0]) > 52: number = 1
        else: number = int(args[0])
        if number >= len(config[str(ctx.guild.id)]["server_deck"]):
            config[str(ctx.guild.id)]["server_deck"] = config[str(ctx.guild.id)]["server_deck"] + dnd.create_standard_deck()
        cards = config[str(ctx.guild.id)]["server_deck"][:number]
        config[str(ctx.guild.id)]["server_deck"] = config[str(ctx.guild.id)]["server_deck"][number:]
        res = '| '
        for c in cards:
            res += c+' | '
        await bot_send(ctx, f"{ctx.author.display_name} drew {number} cards: {res}")
    except:
        pass

@bot.command()
async def fightme(ctx, *args) -> None:
    """ Fight the tavern keeper, if you lose and you are in a voice channel you get kicked from voice channel"""
    # Server Owner can force the fight, otherwise Tavern Keeper will not bother with the fight.
    # This was added to mess with my brother who kept wanting to be able to fight the Tavern Keeper.
    # I am the server owner.
    forced = False
    if args:
        if args[0] == '--force':  forced = True
    if is_owner(ctx) and not forced:
            await bot_send(ctx, f"Sorry {ctx.author.display_name}, I'd rather not fight the owner of the place.")
    else:
        val = random.randrange(1, 100)
        await bot_send(ctx, f"{ctx.author.display_name} was destroyed by the Tavern Keeper") if val < 50 else f"{ctx.author.display_name} fought and won against the Tavern Keeper"
        if val < 50:
            await ctx.author.move_to(None)

@bot.command()
async def coinflip(ctx, call:str=commands.parameter(default=None, description="your call on the coin flip")) -> None:
    ''' Flip a coin and call it in the air.
        Ex. !coinflip               returns a Heads or Tails for the flip.
        Ex. !coinflip heads|tails   return the coin flip and if you win or lose.
    '''
    if call != None:
        call = True if call.lower() == "heads" else False
        flip = random.choice([True, False])
        await bot_send(ctx, f"Coin flipped {'HEADS' if flip == True else 'TAILS'}, {ctx.author.display_name} {'Wins' if call == flip else 'Loses'}")
    elif call == None:
        flip = random.choice([True, False])
        await bot_send(ctx, f"Coin flipped {'HEADS' if flip == True else 'TAILS'}")
    else:
        await bot_send(ctx, f"Coin wasn't flipped due to confusion.")
        
@bot.command()
async def createdeck(ctx, deck_type:str=commands.parameter(default="standard", description="Type of deck to be created: standard|domt|tarot-full|tarot-major|tarot-minor"), deck_name:str=commands.parameter(default="", description="Name of the deck, must not contain spaces"), auto_shuffle:bool=commands.parameter(default=False, description="Should this deck reshuffle after last card is drawn.")) -> None:
    ''' Create a custom deck with a name that can be called upon.
        Ex. !createdeck standard myDeck
        Ex. !createdeck domt someName
        Ex. !createdeck tarot FortuneFavors
    '''
    types = ["standard", "domt", "tarot-full", "tarot-major", "tarot-minor"]
    try:
        if deck_name in config[str(ctx.guild.id)]["saved_decks"]: raise Exception("Deck already exists. Please consider a new name.")
        if deck_name == "": raise Exception("The deck must have a name.")
        if deck_type.lower() not in types: raise Exception(f"Invalid deck type. Make sure to use one of these: standard, domt, tarot-full, tarot-major, tarot-minor")
        
        if deck_type.lower() == "standard":     config[str(ctx.guild.id)]["saved_decks"][deck_name] ={"deck": dnd.create_standard_deck(), "discarded": [], "type": deck_type.lower(), "owner": ctx.author.id, "auto_shuffle": auto_shuffle}
        if deck_type.lower() == "domt":         config[str(ctx.guild.id)]["saved_decks"][deck_name] ={"deck": dnd.create_domt_deck(),     "discarded": [], "type": deck_type.lower(), "owner": ctx.author.id, "auto_shuffle": auto_shuffle}
        if deck_type.lower() == "tarot-major":  config[str(ctx.guild.id)]["saved_decks"][deck_name] ={"deck": dnd.create_tarot_major(),   "discarded": [], "type": deck_type.lower(), "owner": ctx.author.id, "auto_shuffle": auto_shuffle}
        if deck_type.lower() == "tarot-minor":  config[str(ctx.guild.id)]["saved_decks"][deck_name] ={"deck": dnd.create_tarot_minor(),   "discarded": [], "type": deck_type.lower(), "owner": ctx.author.id, "auto_shuffle": auto_shuffle}
        if deck_type.lower() == "tarot-full":   config[str(ctx.guild.id)]["saved_decks"][deck_name] ={"deck": dnd.create_tarot_full(),    "discarded": [], "type": deck_type.lower(), "owner": ctx.author.id, "auto_shuffle": auto_shuffle}
        
    except Exception as e:
        print(e)
        await bot_send(ctx, str(e))        

@bot.command()
async def drawdeck(ctx, deck_name:str=commands.parameter(default="", description="Name of the deck you wish to draw from")) -> None:
    ''' Draw a single card from a named deck.
        Ex. !drawdeck <deck name>
    '''
    try: 
        if not deck_name in config[str(ctx.guild.id)]["saved_decks"]: raise Exception("That deck doesn't exist.")
            
        is_last_card = False if len(config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"]) > 1 else True
        
        card = config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"][0]
        config[str(ctx.guild.id)]["saved_decks"][deck_name]["discarded"].append(card)
        config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"][1:]
        
        res = ""
        if config[str(ctx.guild.id)]["saved_decks"][deck_name]["type"] == "standard":
            res =  f'Drawing from {deck_name}\n'
            res += f'{card}'
        elif config[str(ctx.guild.id)]["saved_decks"][deck_name]["type"] == "domt":
            res =  f'Drawing from {deck_name}\n'
            res += f'{card["name"]}\n'
            res += f'{card["text"]}'
        elif config[str(ctx.guild.id)]["saved_decks"][deck_name]["type"] == "tarot-major":
            card = config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"][0]
            config[str(ctx.guild.id)]["saved_decks"][deck_name]["discarded"].append(card)
            config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"][1:]
            res =  f'Drawing from {deck_name}\n'
            res += f'{card["name"]} - '
            res += f'Upright\n' if card["isReversed"] else f'Reversed\n'
            res += f'{card["upright"]}' if card["isReversed"] else f'{card["reversed"]}'
        elif config[str(ctx.guild.id)]["saved_decks"][deck_name]["type"] == "tarot-minor":
            card = config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"][0]
            config[str(ctx.guild.id)]["saved_decks"][deck_name]["discarded"].append(card)
            config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"][1:]
            res =  f'Drawing from {deck_name}\n'
            res += f'{card["name"]} - '
            res += f'Upright\n' if card["isReversed"] else f'Reversed\n'
            res += f'{card["upright"]}' if card["isReversed"] else f'{card["reversed"]}'
        elif config[str(ctx.guild.id)]["saved_decks"][deck_name]["type"] == "tarot-full":
            card = config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"][0]
            config[str(ctx.guild.id)]["saved_decks"][deck_name]["discarded"].append(card)
            config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"][1:]
            res =  f'Drawing from {deck_name}\n'
            res += f'{card["name"]} - '
            res += f'Upright\n' if card["isReversed"] else f'Reversed\n'
            res += f'{card["upright"]}' if card["isReversed"] else f'{card["reversed"]}'
        
        if is_last_card and config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"]["auto_shuffle"]:
            config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"] = config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"] + config[str(ctx.guild.id)]["saved_decks"][deck_name]["discarded"]
            config[str(ctx.guild.id)]["saved_decks"][deck_name]["discarded"] = []
            random.shuffle(config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"])
            if config[str(ctx.guild.id)]["saved_decks"][deck_name]["type"] != "standard":
                for card in config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"]:
                    card["isReversed"] = random.choice([True, False])
            res += f"\n\n {ctx.author.display_name} has drawn the last card and activated autoshuffle.\n"
            res += f'{deck_name} deck has been reshuffled.' 
        
        await bot_send(ctx, res)

    except Exception as e:
        await bot_send(ctx, "That deck doesn't exist.")

@bot.command()
async def reshuffle(ctx, deck_name:str=commands.parameter(default="", description="Name of the deck you wish to reshuffle")) -> None:
    ''' Allows a deck owner to reshuffle the named deck.
        Ex. !reshuffle <deck name> 
    '''
    try:
        if deck_name not in config[str(ctx.guild.id)]["saved_decks"]: raise Exception(f"No deck with the name {deck_name} exists")
        if ctx.author.id != config[str(ctx.guild.id)]["saved_decks"][deck_name]["owner"]: raise Exception("You must be the author of the deck to reshuffle.")

        config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"] = config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"] + config[str(ctx.guild.id)]["saved_decks"][deck_name]["discarded"]
        config[str(ctx.guild.id)]["saved_decks"][deck_name]["discarded"] = []
        random.shuffle(config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"])
        if config[str(ctx.guild.id)]["saved_decks"][deck_name]["type"] != "standard":
            for card in config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"]:
                card["isReversed"] = random.choice([True, False])
        bot_send(ctx, f'Deck {deck_name} was reshuffled.')
    
    except Exception as e:
        bot_send(ctx, str(e))

@bot.command()
async def removedeck(ctx, deck_name:str=commands.parameter(default="", description="Name of the deck you wish to delete")) -> None:
    ''' Allows a deck owner to remove a deck from saved decks. 
        Server owners also can remove decks to help cleanup their server.
        Ex. !removedeck <deck name>
    '''
    try:
        if deck_name not in config[str(ctx.guild.id)]["saved_decks"]: raise Exception(f"No deck with the name {deck_name} exists.")
        if ctx.author.id != config[str(ctx.guild.id)]["saved_decks"][deck_name]["owner"] or not is_owner(ctx): raise Exception(f"You need to be the deck owner or server owner to remove a named deck.")
        
        del config[str(ctx.guild.id)]["saved_decks"][deck_name]
        await bot_send(ctx, f'Deck {deck_name} was removed.')
        
    except Exception as e:
        await bot_send(ctx, str(e))

@bot.command()
async def revealdeck(ctx, deck_name:str=commands.parameter(default="", description="Name of the deck you wish to reveal.")) -> None:
    ''' Allows a deck owner to reveal the deck and discard piles. 
        Ex. !revealdeck <deck name>
    '''
    try:
        if deck_name not in config[str(ctx.guild.id)]["saved_decks"]: raise Exception(f"No deck with the name {deck_name} exists.")
        if ctx.author.id != config[str(ctx.guild.id)]["saved_decks"][deck_name]["owner"]: raise Exception(f'You must be the deck author to reveal the deck.')
        
        res = f'{ctx.author.display_name} has decided to reveal the {deck_name} deck.\n'
        if config[str(ctx.guild.id)]["saved_decks"][deck_name]["type"] == "standard":
            res += f'Remaining deck: {" | ".join(config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"])}\n'
            res += f'Discarded: {" | ".join(config[str(ctx.guild.id)]["saved_decks"][deck_name]["discarded"])}'
            
        else:
            res += f'Remaining deck: '
            for card in config[str(ctx.guild.id)]["saved_decks"][deck_name]["deck"]:
                res += f' | {card["name"]} '
            res += f' |\n'
            res += f'Discarded: '
            for card in config[str(ctx.guild.id)]["saved_decks"][deck_name]["discarded"]:
                res += f' | {card["name"]} '
            res += f' |'
            
        await bot_send(ctx, res)
    except Exception as e:
        await bot_send(ctx, str(e))
        
@bot.command()
async def listdecks(ctx) -> None:
    ''' Get a list of current decks saved to server. '''
    res = ""
    res += f'Number of active decks: {len(config[str(ctx.guild.id)]["saved_decks"])}\n'
    for each in config[str(ctx.guild.id)]["saved_decks"]:
        res += f'{each} -- {config[str(ctx.guild.id)]["saved_decks"][each]["type"]}'
    
    await bot_send(ctx, res)
    
# Tasks ----------------------------------------------------- #
@tasks.loop(seconds=autosave_time)
async def AutoSaveConfig() -> None:
    ''' Auto save the config to file every autosave_time seconds. '''
    saveConfig(config_name)

# Owner & Configuration Commands ---------------------------- #
@bot.command(hidden=True)
async def settings(ctx, cmd:str="", val:str=None) -> None:
    ''' Configure the bot in various way specific to the server.
        ** Owner Only Command **
        !settings channel <text-channel>    Sets the text channel the bot responds in.
        !settings silent <true|false>       Sets weither or not there is a blip when a message gets sent by boy.
    '''
    if is_owner(ctx):
        global config
        if cmd == 'channel':
            channel = discord.utils.get(ctx.guild.channels, name=val)
            if channel != None and val != None:
                config[str(ctx.guild.id)]["bot_channel"] = channel.id
                await bot_send(ctx, f'Tavern Keeper now sending to {channel.name} or DMs')
            else:
                config[str(ctx.guild.id)]["bot_channel"] = None
                await bot_send(ctx, f'Tavern Keeper was unrestricted from text channels.')
        
        if cmd == 'silent' and (val.lower() == 'true' or val.lower() == 'false'):
            if val.lower() == 'true': config[str(ctx.guild.id)]["silenced"] ==  True
            if val.lower() == 'false': config[str(ctx.guild.id)]["silenced"] == False

@bot.command(hidden=True)
async def clean(ctx, limit:int=100, ch_name:str=None) -> None:
    ''' Clean up a text-channel
        ** Owner Only Command **
        Ex. !clean                      Purge last 100 messages in current text channel.
        Ex. !clean 15                   Purge last 15 messages in current text channel.
        Ex. !clean 15 <text-channel>    Purge last 15 messages in specified text channel.
    '''
    if is_owner(ctx) and not isDM(ctx):
        channel = discord.utils.get(ctx.guild.channels, name=ch_name)
        if channel != None:
            await ctx.message.delete()
            await asyncio.sleep(1)
            await channel.purge(limit=limit)
        else:
            await ctx.message.delete()
            await asyncio.sleep(1)
            await ctx.channel.purge(limit=limit)

@bot.command(hidden=True)
async def peakdeck(ctx) -> None:
    ''' Get a peak at the current server deck. 
        ** Owner only command **
        Ex. !peakdeck   Returns the current server deck.
        
        Keep in mind a deck is created, shuffled, then added to the end of current server deck.
        When cards are drawn its from the front (top) of the deck. So when a new deck is added,
        There is a chance to see 'duplicate cards' but a whole deck will be drawn before new
        cards are drawn.
    '''
    if is_owner(ctx):
        await bot_send(ctx, f'{len(config[str(ctx.guild.id)]["server_deck"])} cards remaining. | {" | ".join(config[str(ctx.guild.id)]["server_deck"])}')

@bot.command(hidden=True)
async def saveconfig(ctx) -> None:
    if ctx.author.id == secret.dev_id:
        saveConfig()
        await ctx.message.delete()

@bot.command(hidden=True)
async def test(ctx, *args) -> None:
    ''' This has speciffically only been used for dev.
        It changes based on what I am testing.
        ** Owner Only Command **
    '''
    if is_owner(ctx):
        print(config)

# Utility Functions ----------------------------------------- #
async def bot_send(ctx, msg, embed=None, view=None) -> None:
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.reply(msg, mention_author=False, embed=embed, view=view)
    else:
        if config[str(ctx.guild.id)]["bot_channel"] == None:
            await ctx.channel.send(msg, embed=embed, view=view, silent=config[str(ctx.guild.id)]["silenced"])
        else:
            channel = bot.get_channel(config[str(ctx.guild.id)]["bot_channel"])
            await channel.send(msg, embed=embed, view=view, silent=config[str(ctx.guild.id)]["silenced"])
            
async def delete_msg(msg) -> None:
    if not isDM(msg):
        await msg.message.delete()
        
def is_owner(ctx) -> bool:
    return True if ctx.author.id == ctx.guild.owner.id else False

def isDM(ctx) -> bool:
    ''' Checks if the message is from a DM or a channel '''
    return True if isinstance(ctx.channel, discord.DMChannel) else False

def create_embed(style:str=None, data:dict=None) -> discord.Embed:
    embed = None
    # style == 'item' embed
    if style == 'item':
        if data:
            embed = discord.Embed(title=data["Name"], colour=0xf4e200)
            embed.add_field(name="", value=f"*{data['Rarity']}*")
            embed.add_field(name="", value=f"*{data['Type']}*", inline=True)
            if data['Attunement'] != "":
                embed.add_field(name="", value=f"**Attunement:** *{data['Attunement']}*") # if no attunemet do no add
            # if no weight replaces with --
            embed.add_field(name="", value=f"**Weight:** *{data['Weight']}*", inline=True) if data['Weight'] != "" else embed.add_field(name=" ", value=f"**Weight:** *--*", inline=True)
            # if no value replaces with -- 
            embed.add_field(name="", value=f"**Value:** *{data['Value']}*", inline=True) if data['Value'] != "" else embed.add_field(name=" ", value=f"**Value:** *--*", inline=True) 
            # if no properties replaces with --
            embed.add_field(name="", value=f"**Properties:** *<properties>*", inline=True) if data['Properties'] != "" else embed.add_field(name=" ", value=f"**Properties:** *--*", inline=True)
            #embed.add_field(name="__Description:__", value=f"*{data['Text']}*")
            embed.set_footer(text="<SRC>")
        else:
            embed = discord.Embed(title="No item was found in the records.", colour=0xf40000)
    # style == 'spell' embed
    elif style == 'spell':
        if data:
            embed = discord.Embed(title="<Spell Name>", colour=0x00e9f4)
            embed.add_field(name="", value="**Level:** <level> <school> spell")
            embed.add_field(name="Cast Time", value="*<cast-time>*", inline=True)
            embed.add_field(name="Duration", value="*<duration>*", inline=True)
            embed.add_field(name="Range", value="*<range>*", inline=True)
            embed.add_field(name="Components", value="*<components>*", inline=True)
            embed.add_field(name="__Description__", value="*<text>*",)
            embed.add_field(name="__At Higher Levels__", value="*<text>*")
            embed.set_footer(text="<SRC>")
        else:
            embed = discord.Embed(title="No spell was found in the records.", colour=0x00e9f4)
    # style == 'monster' embed
    elif style == 'monster':
        if data:
            embed = discord.Embed(title="<Monster Name>", colour=0xf46200)
            embed.add_field(name="__HP__", value="<hp>", inline=True)
            embed.add_field(name="__AC__", value="<ac>", inline=True)
            embed.add_field(name="__CR__", value="<cr>", inline=True)
            embed.add_field(name="**Speeds:** <speeds>\n**Senses:** <senses>\n**Languages:** <languages>")
            embed.add_field(name="- - - - - - - - - - - - - - - - - - - - - - - -", value="")
            embed.add_field(name="__STR__", value="<str>", inline=True)
            embed.add_field(name="__DEX__", value="<dex>", inline=True)
            embed.add_field(name="__CON__", value="<con>", inline=True)
            embed.add_field(name="__INT__", value="<int>", inline=True)
            embed.add_field(name="__WIS__", value="<wis>", inline=True)
            embed.add_field(name="__CHA__", value="<cha>", inline=True)
            embed.add_field(name="__Saving Throws__", value="<saving throws>")
            embed.add_field(name="__Skills__", value="<skills>")
            embed.set_footer(text="<src>")
        else:
            embed = discord.Embed(title="No monster found in the records.", colour=0xf46200)
    
    return embed

def loadConfig(file_name) -> dict:
    res = {}
    try:
        with open(file_name, "r") as fobj:
            res = json.load(fobj)        
        print(f'Tavern Keeper config loaded succeffully\n\n')
    except:
        print(f'No Config could be found for Tavern Keeper. Config file was created.')       
    
    if res == {} or res == '':
        res = {}
        for guild in bot.guilds:
            res[guild.id] = {
                "bot_channel": None,
                "silenced": False,
                "prefix": "!",
                "server_deck": dnd.create_standard_deck(),
                "tables": {},
                "saved_decks": {}
            }
        print(f'Tavern Keeper Discord Bot Config was created as {file_name}')
    
    return res
    
def saveConfig(file_name) -> None:
    try:
        with open(file_name, "w") as fobj:
            json.dump(config, fobj)
    except Exception as e:
        print(f'Autosave failed: {e}')
        
# MAIN ------------------------------------------------------ #
if __name__ == '__main__':
    bot.run(secret.bot_token)