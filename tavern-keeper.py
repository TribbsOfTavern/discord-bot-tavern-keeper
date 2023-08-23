import secrets as secret
import random
import generators as dnd
import dndMongo as db
import json
import asyncio
import discord
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

description = '''
    Tavern Keeper Bot was created specifically for The Tavern.    
'''

# -------------------------- Variables -------------------------- #
bot = commands.Bot(command_prefix='!', description=description, intents=intents, activity=discord.Game(name="!help to see commands"))
bot_db = db.DB('localhost', 27017, 'rpg-tables')
config_name = 'config.json'
config = None

# -------------------------- VIEWS -------------------------- #
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

# --------------------------  COMMANDS  -------------------------- #
@bot.event
async def on_ready():
    print('- - - - - - - - - - - - - -')
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'Connected to {len(bot.guilds)} guilds.')
    print('- - - - - - - - - - - - - -')
    global config
    config = loadConfig(config_name)
    AutoSaveConfig.start()    
    print(config)

@bot.command()
async def ping(ctx):
    """ Call and return, returns pong!"""
    await bot_send(ctx, "pong!")
    
@bot.command()
async def roll(ctx, roll:str = commands.parameter(default='1d20', description='roll of the dice')):
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
async def roll_character(ctx, *args):
    """ Generate a random character at level 1 with 3d6 stats
        level       sets level
        class       sets class
        race        sets race
        background  sets background
        rolls       style for rolling stats (standard 3d6 or 4d6kh3)
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
async def spell(ctx, *args):
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
async def item(ctx, *args):
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
async def monster(ctx, *args):
    """ Get information pertaining to a monster
        Ex. !monster 'Goblin'
        Ex. !monster 'Green Hag'
    """
    verbose = False
    if args[-1] == '--all':
        args = args[0:-1]
        verbose = True
        
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
async def draw(ctx, *args):
    """ Draws a number of random cards from the server deck. """
    global config
    args = list(args)
    try:
        if args == [] or int(args[0]) > 52: number = 1
        else: number = int(args[0])
        if number >= len(config[str(ctx.guild.id)]["server_deck"]):
            config[str(ctx.guild.id)]["server_deck"] = config[str(ctx.guild.id)]["server_deck"] + dnd.create_deck()
        cards = config[str(ctx.guild.id)]["server_deck"][:number]
        config[str(ctx.guild.id)]["server_deck"] = config[str(ctx.guild.id)]["server_deck"][number:]
        res = '| '
        for c in cards:
            res += c+' | '
        await bot_send(ctx, f"{ctx.author.display_name} drew {number} cards: {res}")
    except:
        pass

@bot.command()
async def fightme(ctx, *args):
    """ Fight the tavern keeper, if you lose you get kicked from voice channel"""
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
async def suggest(ctx, *args):
    """ Add a suggestion to the box for the developer. """
    if args:
        await ctx.guild.owner.send(content=f"New Suggestion: {' '.join(args)}", silent=True)
        await bot_send(ctx, f"Your suggestion has been submitted, {ctx.author.display_name}")
        await delete_msg(ctx)

@bot.command()
async def coinflip(ctx, call:str=None):
    ''' flip a coin and call it in the air.'''
    if call != None:
        call = True if call.lower() == "heads" else False
        flip = random.choice([True, False])
        await bot_send(ctx, f"Coin flipped {'HEADS' if flip == True else 'TAILS'}, {ctx.author.display_name} {'Wins' if call == flip else 'Loses'}")
    elif call == None:
        flip = random.choice([True, False])
        await bot_send(ctx, f"Coin flipped {'HEADS' if flip == True else 'TAILS'}")
    else:
        await bot_send(ctx, f"Coin wasn't flipped due to confusion.")
# -------------------------- Tasks ----------------------------- #
@tasks.loop(seconds=300)
async def AutoSaveConfig():
    saveConfig(config_name)

# --------------------------  Configuration Commands  -------------------------- #
@bot.command(hidden=True)
async def setChannel(ctx, chn):
    if is_owner(ctx):
        global config
        channel = discord.utils.get(ctx.guild.channels, name=chn)
        if channel != None:
            print(f'{config[str(ctx.guild.id)]}: bot_channel: {channel}')
            config[str(ctx.guild.id)]["bot_channel"] = ctx.channel.id
            await bot_send(ctx, f'Bot now configured to send only to {channel.name} or DMs')
        else:
            await bot_send(ctx, f'channel {chn} was not found and no config was sent')
    await delete_msg(ctx)
    
@bot.command(hidden=True)
async def settings(ctx, cmd:str="", val:str=None):
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
                 
# --------------------------  Owner Commands  -------------------------- #
@bot.command(hidden=True)
async def clean(ctx, ch_name:str=None, limit:int=100):
    if is_owner(ctx) and not isDM(ctx):
        channel = discord.utils.get(ctx.guild.channels, name=ch_name)
        if channel != None:
            await ctx.message.delete()
            await asyncio.sleep(1)
            await channel.purge(limit=limit)

@bot.command(hidden=True)
async def getServerDeck(ctx):
    if is_owner(ctx):
        await bot_send(ctx, f'{len(config[str(ctx.guild.id)]["server_deck"])} cards remaining. | {" | ".join(config[str(ctx.guild.id)]["server_deck"])}')

@bot.command(hidden=True)
async def test(ctx, *args):
    if is_owner(ctx):
        await ctx.send("This is a test", view=viewItem())

# --------------------------  Utility Functions  -------------------------- #
def is_owner(ctx):
    return True if ctx.author.id == ctx.guild.owner.id else False

async def bot_send(ctx, msg, embed=None, view=None):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.reply(msg, mention_author=False, embed=embed, view=view)
    else:
        if config[str(ctx.guild.id)]["bot_channel"] == None:
            await ctx.channel.send(msg, embed=embed, view=view, silent=config[str(ctx.guild.id)]["silenced"])
        else:
            channel = bot.get_channel(config[str(ctx.guild.id)]["bot_channel"])
            await channel.send(msg, embed=embed, view=view, silent=config[str(ctx.guild.id)]["silenced"])
            
async def delete_msg(msg):
    if not isDM(msg):
        await msg.message.delete()

def isDM(ctx):
    return True if isinstance(ctx.channel, discord.DMChannel) else False

def create_embed(style:str=None, data:dict=None):
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

def loadConfig(file_name):
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
                "server_deck": dnd.create_deck(),
                "tables": {}
            }
        print(f'Tavern Keeper Config was created as {file_name}')
    return res
    
def saveConfig(file_name):
    try:
        with open(file_name, "w") as fobj:
            json.dump(config, fobj)
        print(f'Autosave completed')
    except Exception as e:
        print(f'Autosave failed: {e}')
        
# ------------------------------------------------------------------------------------
if __name__ == '__main__':
    bot.run(secret.bot_token)