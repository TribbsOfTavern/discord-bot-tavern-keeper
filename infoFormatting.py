
TEXT_CAP = 2000

def format_spell(info:dict={}) -> str:
    ''' Format spell info given from a mongodb schema dict into a printable string '''
    res = ''
    res += f'**Name:** {info["Name"]}\n'
    res += f'**Level:** {info["Level"]}\t\t**Cast Time:** {info["casting-time"]}\t\t**Duration:** {info["Duration"]}\n'
    res += f'**School:** {info["School"]}\t\t**Range:** {info["Range"]}\t\t**Components:** {info["Components"]}\n'
    res += f'\t{info["Text"]}\n'
    res += f'' if info["at-higher-levels"] == '' else f'\t* **At Higher Levels:**{info["at-higher-levels"]}*'
    
    res = [res[i:i+TEXT_CAP] for i in range(0, len(res), TEXT_CAP)]
    return res

def format_item(info:dict={}) -> str:
    ''' Format item info given from a mongodb schema dict into a printable string '''
    res = ''
    res += f'**Name:** {info["Name"]}\n'
    res += f'{info["Rarity"]}-{info["Type"]}\n'
    res += f'' if info['Attunement'] == '' else f'**Attunement:** {info["Attunement"]}\n'
    res += f'**Weight:** --\t\t' if info['Weight'] == '' else f'**Weight:** {info["Weight"]}\t\t'
    res += f'**Value:** --\t\t' if info['Value'] == '' else f'**Value:** {info["Value"]}\n'
    res += f'**Properties:** --\n' if info['Properties'] == '' else f'**Properties:** {info["Properties"]}\n'
    res += f'\t*{info["Text"]}*\n'
    
    res = [res[i:i+TEXT_CAP] for i in range(0, len(res), TEXT_CAP)]
    return res

def format_monster(info:dict={}) -> str:
    ''' Format monster info given from a mongodb schema dict into a printable string '''
    res = ''
    res += f'**Name:** {info["Name"]}\t\t**CR:**{info["CR"]}\n'
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

    res = [res[i:i+TEXT_CAP] for i in range(0, len(res), TEXT_CAP)]
    return res

def format_monster_full(info:dict={}) -> str:
    ''' Format monster info given from a mongodb schema dict into a printable string with multiple pages '''
    pages = []
    res = ''
    res += f'## __Name: {info["Name"]}__\t\t**CR:**{info["CR"]}\n>'
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
    pages.append(res)
    res = ''
    res += f'## **{info["Name"]} Traits:**\n'
    res += f'{info["Traits"]}'
    pages.append(res)
    res = ''
    res += f'## **{info["Name"]} Actions:**\n'
    res += '' if info['Actions'] == '' else f'**Actions**:\n> {info["Actions"]}\n\n'
    res += '' if info['Bonus Actions'] == '' else f'**Bonus Actions:\n> {info["Bonus Actions"]}\n\n'
    res += '' if info['Reactions'] == '' else f'**Reactions:\n> {info["Reactions"]}\n'
    pages.append(res)
    
    if info["Legendary Actions"] != '' or info["Mythic Actions"] != '' or info["Lair Actions"] != '' or info["Regional Effects"] != '':
        res = ''
        res += f'## **{info["Name"]} Special Actions:**\n'
        res += f'' if info["Legendary Actions"] == '' else f'**Legendary Actions:**\n>{info["Legendary Actions"]}\n\n'
        res += f'' if info["Mythic Actions"] == '' else f'**Mythic Actions:**\n>{info["Mythic Actions"]}\n\n'
        res += f'' if info["Lair Actions"] == '' else f'**Lair Actions:**\n>{info["Lair Actions"]}\n\n'
        res += f'' if info["Regional Effects"] == '' else f'**Regional Effects:**\n>{info["Regional Effects"]}\n\n'
        
        res = [res[i:i+TEXT_CAP] for i in range(0, len(res), TEXT_CAP)]
        for each in res:
            pages.append(each)
    
    return pages