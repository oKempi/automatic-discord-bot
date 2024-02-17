import discord
from discord.ext import commands
from discord import app_commands    
import random as r
import csv
import time as t
from typing import Optional
import asyncio
#from infractions import infraction
#from control import action
import subprocess as s
import socket
import os

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True
permissions = discord.permissions
permissions.use_application_commands = True

bot = commands.Bot(command_prefix=".", intents=intents, strip_after_prefix= True) #help_command = False

token = "nein,大丈夫です"
NOT_YET = "Sorry but that function does not work yet"
IS_WORK = "This function is still being worked on"
INV_LINK = "https://discord.com/api/oauth2/authorize?client_id=1149063646543093780&permissions=8&scope=bot"
cList = [".ping", ".uwu", ".jap", ".commandlist", ".about", "MODERATION:",".kick", ".ban", ".banlist", ".mute"]
with open("discord\\bot\\database\\Jwords.txt", "r", encoding="utf-8") as jwords_file:
    jwords = jwords_file.readlines()
ebd = discord.Embed()
uwuGirl = ebd.set_image(url="https://static.wikia.nocookie.net/beluga/images/e/e5/Realgirluwu.jpg/revision/latest/thumbnail/width/360/height/360?cb=20221107231631")
cons = "discord\\bot\\console.py"

#try:
#    s.run(["python", cons], check=True)
#except s.CalledProcessError as e:
#    print(f"Error while running: {e}")

def error():
    print("\033[31m!\033[0m", "Command that (does not exist/was written wrong) has occurred")
    print("\033[33m!\033[0m", "This error might be a mistake in the code...")

@bot.event
async def on_ready():
  print("Logged as : "+str(bot.user))
  game = discord.Game("Works! (For ANKE ;D)")
  await bot.change_presence(status=discord.Status.online, activity=game)
  print("\033[33m!\033[0m" ,"Changed the bots status!")

@bot.event
async def on_disconnect():
    print("\033[31m!\033[0m",t.strftime("%H:%M:%S") ,"The client has been disconected from the discord server OR while trying to connect to it")

@bot.event
async def on_connect():
    print("\033[32m!\033[0m",t.strftime("%H:%M:%S") ,"The client has connected (back) to the Discord servers")

@bot.event
async def on_member_join(member: discord.User):
    print("\033[32m!\033[0m", member, "joined the server", member.guild.name)
    await member.guild.text_channels[0].send(f"Welcome @{member} to {member.guild.name}!")

#@bot.event
#async def on_member_unban(ctx, guild, member):
#    print()

@bot.event
async def on_command_error(ctx, error):
    print("\033[31m!\033[0m", "Command that (does not exist/was written wrong) has occurred")
    print("\033[33m!\033[0m", "This error might be a mistake in the code...")
    print(error)
    await ctx.send("There was some kind of error...")

#NEEDS a lot of work!
#@bot.event
#async def on_message(message):
#    with open("discord\\bot\\database\\commands.csv", "r") as c:
#        csvReader = csv.reader(c)
#        for row in csvReader:
#            if message in row[1]:
#                try:
#                    value = row[1]
#    if message.content == 
        
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def uwu(ctx):
    await ctx.send(embed=uwuGirl)

@bot.command()
async def jap(ctx):
    if jwords:
        random_line = r.choice(jwords)
        await ctx.send(random_line.strip())

@bot.command()
async def commandlist(ctx):
    stripClist = cList.str
    await ctx.send(stripClist) 

@bot.command()
async def project(ctx):
    await ctx.send(NOT_YET)   

@bot.command()
async def about(ctx):
    await ctx.send("Hello, I am ANKE bot. I am a program created using python with discord.py library. You can write .commandlist to see more commands ;)")

@bot.command()
async def invite(ctx):
    await ctx.send("This is the invitation link for this bot")
    await ctx.send(f"{INV_LINK}")

#moderation tools
@bot.command()
async def kick(ctx, member: discord.Member, reason=None):
    if ctx.author.guild_permissions.kick_members:
        print("\033[31m!\033[0m", f"{member} was kicked from the server {member.guild.name}")
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} was kicked from this server!")
    else:
        await ctx.send("You do not have permissions to do that!")

@bot.command()
async def ban(ctx, member: discord.Member, reason=None):
    if ctx.author.guild_permissions.ban_members:
        with open("discord\\bot\\database\\banLog.csv", "a") as log:
            toW = f"{member.id},{member}" #stands for to Write
            log.writelines(toW)
        print("\033[31m!\033[0m", f"{member} was banned from the server {member.guild.name}")
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} was banned from this server!")
    else:
        await ctx.send("You do not have permissions to do that!")

@bot.command()
async def banlist(ctx):
    with open("discord\\bot\\database\\data.csv", "r") as logR:
        csvReader = csv.DictReader(logR)
        data = list(csvReader)
        col1_values = [row["id"] for row in data]
        col2_values = [row["user"] for row in data]
    await ctx.send(col1_values)
    await ctx.send(col2_values)

@bot.command()
async def mute(ctx, member: discord.Member, time: Optional[int]):
    if ctx.author.guild_permissions.kick_members:
        role = discord.utils.get(ctx.guild.roles, id=1167843245724807219)
        await member.add_roles(role)
        print("\033[31m!\033[0m" ,f"Added {role.name} to {member.display_name}")
        await member.guild.text_channels[8].send(f"Added {role.name} to {member.display_name}")
        if time == True:
            wait = 60 * time
            await asyncio.sleep(wait)
            await member.remove_roles(role)
            await ctx.send("Done!")
        else:
            pass
    else: 
        print("\033[31m!\033[0m" ,f"There was an attempt to mute {member} by {ctx.author}")
        await member.guild.text_channels[0].send("You do not have permissions to do that!")

@bot.command()
async def unmute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.kick_members:
        role = discord.utils.get(ctx.guild.roles, id=1167843245724807219)
        await member.remove_roles(role)
        print("\033[31m!\033[0m" ,f"Removed {role.name} from {member.display_name}")
        await member.guild.text_channels[0].send(f"Removed {role.name} from {member.display_name}")
    else:
        print("\033[31m!\033[0m" ,f"There was an attempt to mute {member} by {ctx.author}")
        await member.guild.text_channels[0].send("You do not have permissions to do that!")

#@bot.command()
#async def warn(ctx, member: discord.Member):
#    infraction_instance = infraction()
#    infraction_instance.addPoint(user=member, amount=1)
#    await ctx.send(f"{member}, has been warned!") #should show how many infr. by using return infr.

@bot.command()
async def praise(ctx, member: discord.Member):
    pass

#@bot.command()
#async def infractions(ctx):
#    await infraction.list(ctx=ctx)

@bot.command()
async def unban(ctx, member):
    pass

#@bot.command()
#async def pardon(ctx, member: discord.User.id, *, reason=None):
#    if ctx.author.guild_permissions.ban_members:
#        await ctx.guild.unban(member, reason)
#    else:
#        print("\033[31m!\033[0m" ,"Error 1")
#        await ctx.send("You do not have permissions to do that!")

#needs fixing
#@bot.command()
#async def pardon(ctx, *, member):
#    banned_users = await ctx.guild.bans()
#    member_name = member.split("#")[0]
#
#    for ban_entry in banned_users:
#        user = ban_entry.user
#
#        if user.name == member_name:
#            await ctx.guild.unban(user)
#            await ctx.send(f"Pardoned {user.name}#{user.discriminator}")
#            return
#    await ctx.send("Member not found or is not banned.")

#Sets the bot online
bot.run(token=token)