import pymongo

# My Mongodb is locally run and I spent a lot of time filling out the tables,
# Some scraping and a lot of typing and cleaning soup. Probably not applicable for others,
# But I added some functions that return a dict that use the same schema as my tables.
# If someone finds this useful, cool, but mostly they were designed for my use in adding
# more to the tables in the future.
class DB():
    uri         = 'localhost'
    port        = 27017
    client      = None
    db_name     = None
    curr_db     = None

    def __init__(self, uri:str='localhost', port:int=27017, db_name:str=''):
        self.uri = uri
        self.port = port
        self.db_name = db_name
        self.client = self.conn(self.uri, self.port)
        self.curr_db = self.set_db(db_name)
        
    def conn(self, uri:str='', port:int=0) -> pymongo.MongoClient:
        return pymongo.MongoClient(uri, port)
    
    def set_db(self, db_name:str='') -> pymongo.database.Database:
        return self.client[db_name]

    def get_database_list(self) -> list:
        return self.client.list_database_names()
    
    def get_collection_list(self) -> list:
        return self.curr_db.list_collection_names()
    
    def get_item_from(self, collection:str='', query:dict={}) -> dict:
        return self.curr_db[collection].find_one(query)
    
    def get_all_from(self, collection:str='', query:dict={}, filter:dict={}, sort:str='', accending:bool=True) -> list:
        return self.curr_db[collection].find(query).sort(sort, 1 if accending else -1)

# These will come in handy when adding in homebrew and other sources to the mix.
def schema_item(item_name:str='', item_source:str='', item_rarity:str='', item_type:str='', item_attunement:str='', item_properties:str='', item_weight:str='', item_value:str='', item_text:str='') -> dict:
    '''
    item schema for the rpg-tables collection
    '''
    return dict({
        "Name": item_name, # str
        "Source": item_source, # str
        "Rarity": item_rarity, # str
        "Type": item_type, # str
        "Attunement": item_attunement, # str
        "Properties": item_properties, # str
        "Weight": item_weight, # sdtr
        "Value": item_value, # str
        "Text": item_text # str
    })

def schema_spell(spell_name:str='', spell_source:str='', spell_level:str='', spell_casting_time:str='', spell_duration:str='', spell_school:str='', spell_range:str='', spell_components:str='', spell_classes:list=[], spell_text='', spell_higher_levels:str='') -> dict:
    '''
    spell schema for the rpg-tables collection
    '''
    return dict({
        'Name': spell_name, # str
        'Source': spell_source, # str
        'Level': spell_level, # str
        'casting-time': spell_casting_time, # str
        'Duration': spell_duration, # str
        'School': spell_school, # str
        'Range': spell_range, # str
        'Components': spell_components, # str
        'Classes': spell_classes, # list of classes who can use the spell
        'Text': spell_text, # str
        'at-higher-levels': spell_higher_levels # str
    })

def schema_monster(monster_name:str='', monster_source:str='', monster_size:str='', monster_type:str='', monster_alignment:str='', monster_ac:str='', monster_hp:str='', monster_speeds:list=[], monster_str:int=10, monster_dex:int=10, monster_con:int=10, monster_int:int=10, monster_wis:int=10, monster_cha:int=10, monster_saving_throws:list=[], monster_skills:list=[], monster_vulnerabilities:list=[], monster_resistances:list=[], monster_immunities:list=[], monster_condition_immunities:list=[], monster_senses:list=[], monster_languages:list=[], monster_cr:str='0', monster_traits:list=[], monster_actions:list=[], monster_bonus_actions:list=[], monster_reactions:list=[], monster_legendary_actions:list=[], monster_mythic_actions:list=[], monster_lair_actions:list=[], monster_regional_effects:list=[], monster_environments:list=[]) -> dict:
    '''
    monster schema for the rpg-tables collection
    '''
    return dict({
        "Name": monster_name, # str
        "Source": monster_source, # str
        "Size": monster_size, # str
        "Type": monster_type, # str
        "Alignment": monster_alignment, # str
        "AC": monster_ac, # str
        "HP": monster_hp, # str
        "Speed": monster_speeds, # str
        "Strength": monster_str, # int
        "Dexterity": monster_dex, # int
        "Constitution": monster_con, # int
        "Intelligence": monster_int, # int
        "Wisdom": monster_wis, # int
        "Charisma": monster_cha, # int
        "Saving Throws": monster_saving_throws, # list of saving throw if any, empty [] if none
        "Skills": monster_skills, # list of skill if any, empty [] if none
        "Damage Vulnerabilities": monster_vulnerabilities, # list of vulnerability, empty [] if none
        "Damage Resistances": monster_resistances, # list of resistance, empty [] if none
        "Damage Immunities": monster_immunities, # list of immunities, empty [] if none
        "Condition Immunities": monster_condition_immunities, # list of condition immunities, empty [] if none
        "Senses": monster_senses, # list of senses, empty [] if none
        "Languages": monster_languages, # list of languages, empty [] if none
        "CR": monster_cr, # str
        "Traits": monster_traits, # list of traits, empty [] if none
        "Actions": monster_actions, # list of actions, empty [] if none
        "Bonus Actions": monster_bonus_actions, # list of bonus actions, empty if none
        "Reactions": monster_reactions, # list of reactions empty [] if none
        "Legendary Actions": monster_legendary_actions, # list of legendary actions, empty [] if none
        "Mythic Actions": monster_mythic_actions, # list of mythic actions, empty [] if none   
        "Lair Actions": monster_lair_actions, # list of lair actions, empty [] if none
        "Regional Effects": monster_regional_effects, # list of regional effects, empty [] if none
        "Environment": monster_environments # list of environments, empty [] if none
    })

def schema_character() -> dict:
    # TODO -- Not worked on yet.
    '''
    character sheet shcema for characters collection
    '''
    return dict({})

def schema_user() -> dict:
    # TODO -- Not worked on yet
    '''
        user schema for the user collection
    '''
    return dict({})