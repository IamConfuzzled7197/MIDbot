#test
import discord
import time
from discord.ext import tasks, bridge
import random
from random import choice
import asyncio
import os
import io
import requests

from waiting import wait
import flaskthing #just the name, forgot underscroll

my_secret = os.environ['chabukswar']  #key
prefixes = ['m.', 'M.']
client = bridge.Bot(command_prefix=prefixes,
                      guild_subscriptions=True,
                      intents=discord.Intents.all(),
                      case_insensitive=True)

#changing status thing
statuslist = [
    'students talking',
    'SciOly sweats panicking',
    'MacKhoi getting called Peter',
    'people arguing for nothing',
    'other bots be more useful than me',
    'the mods go brrrrr',
]

#changes status
@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=random.choice(statuslist)))


@client.event
async def on_ready():
	change_status.start()
	print("bot is ready")


#say
@client.bridge_command(description = 'Repeat what you wants you to say!')
async def say(ctx, *, message):
	await ctx.respond(f"{message}")


#fake ban
@client.bridge_command(description = 'Fake ban a person and let them squirm in pain!')
async def fban(ctx, member: discord.Member = None, *, reason="Not given"):

	if member == None:
		await ctx.respond("mention the person to ban you dumbo")
		return
	embed = discord.Embed(title=f"*{member} banned successfully   :white_check_mark:*", description=f"Reason: {reason}", colour=0x8c9eff)
	await ctx.respond(embed = embed)



#8ball
@client.bridge_command(description = "Get the 8ball and see what's your fortune!", aliases=['8ball'])
async def _8ball(ctx):
    eightball_list = [
        'As I see it, yes.', 'Ask again later.', ' Better not tell you now.',
        ' Cannot predict now.', ' Concentrate and ask again.',
        ' Don’t count on it.', ' It is certain.', ' It is decidedly so.',
        ' Most likely.', ' My reply is no.', ' My sources say no.'
    ]
    await ctx.respond(f"{random.choice(eightball_list)}")


#murder
@client.bridge_command(description = "MURDER SOMEONE!")
async def murder(ctx, member: discord.Member = None):
	if member == None:
		await ctx.respond("Come on... WHO DO YOU WANT TO MURDER")
	if member == ctx.author:
		await ctx.respond("get hope squad")
		return
	person1 = ctx.author
	person2 = member
	murderlist = [
        f'{person1.name} pushed {person2.name} off a cliff',
        f'{person1.name} stabbed {person2.name} in the back',
		f"{person1.name} sent {person2.name} to the principal's office",
		f"{person1.name} sent {person2.name} to Jesus",
		f"{person1.name} killed {person2.name}.exe",
		f"{person1.name} made {person2.name} drink too much water",
		f"{person2.name} just died",
		f"{person1.name} is dead",
		f"{person1.name} ate {person2.name}'s liver",
		f"{person1.name} stomped {person2.name} flat"



    ]
	await ctx.respond(random.choice(murderlist))

#wyr
@client.bridge_command(description = "Would you rather questions ", aliases = ['wyr'])
async def wouldyourather(ctx):
	question = requests.get("https://would-you-rather-api.abaanshanid.repl.co/")
	question2 = question.json()
	embed = discord.Embed(title = "Would you Rather...", description = question2['data'], color = discord.Color.green())
	embed.set_thumbnail(url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMPLoqMv9Zuv7hiV7QFL1gm5wMFCqiZSf7KuTEUQpU&s")
	await ctx.respond(embed = embed)

#Nasa fun fact thing
@client.bridge_command(description = "Daily fact by NASA!", aliases = ['nf'])
async def nasafact(ctx):
	nasa1 = requests.get("https://api.nasa.gov/planetary/apod?api_key=SIwOcgh4f1W4pLZHMUwCa6ShoDgOLdh12zPxNrpd")
	rnasa = nasa1.json()
	embed = discord.Embed(title = f"Space fact by NASA! {rnasa['date']}", url = rnasa['url'],description = rnasa['explanation'], color = discord.Color.blue())
	embed.set_thumbnail(url = "http://www.nasa.gov/sites/default/files/images/nasaLogo-570x450.png")
	await ctx.respond(embed = embed)
	
#general fun fact
@client.bridge_command(description = "A fun fact for you to learn!", aliases = ['ff'])
async def funfact(ctx):
	furl = requests.get("https://www.thefact.space/random")
	funfact = furl.json()
	embed = discord.Embed(title = "Fun fact!", description = funfact['text'], color = discord.Color.blurple())
	await ctx.respond(embed = embed)
	print(type(funfact))

@client.bridge_command(description ='test')
async def test(ctx):
	await ctx.respond("tjestjdsklfjasdklf")

#calculator
@client.bridge_command(description = 'calculate stuff or something')
async def calculate(ctx, x,*,y):
	class Add(discord.ui.View): #Add
		@discord.ui.button(label = "+", row = 0, style = discord.ButtonStyle.primary)
		async def button_callback(self, button, interaction):
			try:
				answer = int(x) + int(y)
			except:
				await ctx.respond("Put actual integers")
			button.disabled = True
			await interaction.response.send_message(f"{x}+{y} = {answer}")
			for child in self.children:
				child.disabled = True
			await ctx.edit(view = self) #note to self, do ctx.edit. it works better
			
		
		@discord.ui.button(label = "-", row = 0, style = discord.ButtonStyle.primary)
		async def second_button_callback(self, button, interaction):
			answer = int(x) - int(y)
			button.disabled = True
			for child in self.children:
				child.disabled = True
			await interaction.response.send_message(f"{x}-{y} = {answer}")
			await ctx.edit(view = self) #note to self, do ctx.edit. it works better
			
		@discord.ui.button(label = "*", style = discord.ButtonStyle.primary)
		async def third_button_callback(self, button, interaction):
			answer = int(x) * int(y)
			button.disabled = True
			for child in self.children:
				child.disabled = True
			await interaction.response.send_message(f"{x}*{y} = {answer}")
			await ctx.edit(view = self)
			
		@discord.ui.button(label = "/", style = discord.ButtonStyle.primary)
		async def fourth_button_callback(self, button, interaction):
			answer = int(x) / int(y)
			button.disabled = True
			for child in self.children:
				child.disabled = True
			await interaction.response.send_message(f"{x}/{y} = {answer}")
			await ctx.edit(view = self)

			
	await ctx.respond(f"Choose an operation", view = Add() )


flaskthing.keep_alive() #initiate hosting! yeeee!
try:
	client.run(my_secret)
except:
	os.system("kill 1")

