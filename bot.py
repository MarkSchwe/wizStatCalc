#contains the main functions for the calculator
import discord
from discord.ext import commands
import numpy as np
import os
import dotenv

dotenv.load_dotenv() #loaded from an env file instead of showing it on github

async def calc(input1,input2,input3,input4,input5):
    
    df = np.genfromtxt('./statCaps.csv', delimiter=',')
    caps150 = np.ones((7,7))
    caps160 = np.ones((7,7))
    caps170 = np.ones((7,7))
    for i in range(7):
        caps150[i] = df[i]
    for i in range(7):
        caps160[i] = df[i+7]
    for i in range(7):
        caps170[i] = df[i+14]

    input1 = input1.lower()
    school = 0
    if input1 == 'fire':
        school = 0
    elif input1 == 'ice':
        school = 1
    elif input1 == 'storm':
        school = 2
    elif input1 == 'myth':
        school = 3
    elif input1 == 'life':
        school = 4
    elif input1 == 'death':
        school = 5
    elif input1 == 'balance':
        school = 6
    else:
        return -1

    level = np.ones((7,7))
    if (float(input2) >= 150) & (float(input2)< 160):
        level = caps150
    elif (float(input2) >= 160) & (float(input2) < 170):
        level = caps160
    elif (float(input2) >= 170) & (float(input2) < 180):
        level = caps170
    else:
        return -1
    
    input3 = input3.lower()
    stat = 0
    if input3 == 'hp' or input3 == 'health':
        stat = 0
    elif input3 == 'damage' or input3 == 'dmg':
        stat = 1
    elif input3 == 'pierce':
        stat = 2
    elif input3 == 'resist' or input3 == 'res':
        stat = 3
    elif input3 == 'accuracy' or input3 == 'acc':
        stat = 4
    elif input3 == 'outgoing':
        stat = 5
    elif input3 == 'pip' or input3 == 'pip chance' or input3 == 'power pip':
        stat = 6
    else:
        return -1
    
    level2 = np.ones((7,7))
    if (float(input4) >= 150) & (float(input4)< 160):
        level2 = caps150
    elif (float(input4) >= 160) & (float(input4) < 170):
        level2 = caps160
    elif (float(input4) >= 170) & (float(input4) < 180):
        level2 = caps170
    else:
        return -1
    scale = float((float(input5)/level[school][stat])*float(level2[school][stat]))
    if float(input5) > float(level[school][stat]):
        scale = float(level2[school][stat])
    
    if float(input2) < float(input4):
        if float(input5) > float(level[school][stat]):
            scale = float(level[school][stat])
        else:
            scale = float(input5)
    
    return int(round(scale,0))

async def offschoolcalc(primary,secondary,initlvl,tolvl,dmg):
    df = np.genfromtxt('./offschool.csv', delimiter=',')
    caps150 = np.ones((7,7))
    caps160 = np.ones((7,7))
    caps170 = np.ones((7,7))
    for i in range(7):
        caps170[i] = df[i]
    for i in range(7):
        caps160[i] = df[i+7]
    for i in range(7):
        caps150[i] = df[i+14]
    prim = 0
    if primary == 'fire':
        prim = 0
    elif primary == 'ice':
        prim = 1
    elif primary == 'storm':
        prim = 2
    elif primary == 'myth':
        prim = 3
    elif primary == 'life':
        prim = 4
    elif primary == 'death':
        prim = 5
    elif primary == 'balance':
        prim = 6
    else:
        return -1

    second = 0
    if secondary == 'fire':
        second = 0
    elif secondary == 'ice':
        second = 1
    elif secondary == 'storm':
        second = 2
    elif secondary == 'myth':
        second = 3
    elif secondary == 'life':
        second = 4
    elif secondary == 'death':
        second = 5
    elif secondary == 'balance':
        second = 6
    else:
        return -1

    level = np.ones((7,7))
    if (float(initlvl) >= 150) & (float(initlvl)< 160):
        level = caps150
    elif (float(initlvl) >= 160) & (float(initlvl) < 170):
        level = caps160
    elif (float(initlvl) >= 170) & (float(initlvl) < 180):
        level = caps170
    else:
        return -1

    level2 = np.ones((7,7))
    if (float(tolvl) >= 150) & (float(tolvl)< 160):
        level2 = caps150
    elif (float(tolvl) >= 160) & (float(tolvl) < 170):
        level2 = caps160
    elif (float(tolvl) >= 170) & (float(tolvl) < 180):
        level2 = caps170
    else:
        return -1
    scale = float((float(dmg)/level[prim][second])*float(level2[prim][second]))
    if float(dmg) > float(level[prim][second]):
        scale = float(level2[prim][second])
    
    if int(initlvl) < int(tolvl):
        if float(dmg) > float(level[prim][second]):
            scale = float(level[prim][second])
        else:
            scale = float(dmg)
    return int(round(scale,0))
    
def run_discord_bot():
    TOKEN = os.environ.get('ButtonTomToken')
    testid1=os.environ.get('testingchannel1')
    Periwinkleid=os.environ.get('PeriwinkleChannelID')

    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix="/",help_command=None,intents=intents)
    guild = discord.Object(id=testid1)
    guild2 = discord.Object(id=Periwinkleid)

    @client.tree.command(name="calc",description="Calculate stat caps. Stats: damage, pierce, hp, resist, accuracy, outgoing, pip",guilds=[guild,guild2])
    async def statcapcalc(ctx: discord.interactions, school: str, level: str, desired_stat: str, desired_level: str, current_stat: str):
        calculate = await calc(school,level,desired_stat,desired_level,current_stat)
        if calculate == -1:
            await ctx.response.send_message(f'invalid response.')    
        await ctx.response.send_message(f'Your {desired_stat} would be {calculate}')
    
    @client.tree.command(name="offschooldmg",description="Calculate off school damage cap",guilds=[guild,guild2])
    async def offschool(ctx: discord.interactions, primary_school: str, secondary_school: str, level: str, scaledlvl: str, damage: str):
        calculate = await offschoolcalc(primary_school,secondary_school,level,scaledlvl,damage)
        if calculate == -1:
            await ctx.response.send_message(f'invalid response.')
        await ctx.response.send_message(f'Your {secondary_school} damage would be {calculate}')

    @client.event
    async def on_ready():
        await client.tree.sync(guild=guild2)
        print(f'{client.user} is now running!')
             
    client.run(TOKEN)
