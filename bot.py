#code source de bisounours-discord par Julien Dechaud
#https://github.com/juliendechaud/bisounours-discord

#importation des modules
import os
from dotenv import load_dotenv #variables d'environnement
import discord #api discord
from discord.ext import commands #gestion des commandes
import db

#initialisation
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Client()
bot = commands.Bot(command_prefix='$')
db = db.db("bisounours.db")

#quand le bot est prêt
@bot.event
async def on_ready():
	print(f'{bot.user} ready to work !')
	print(f'Connecté sur {len(bot.guilds)} serveur(s)')
	await bot.change_presence(activity=discord.Game("$help"))

#commande latence
@bot.command()
async def ping(ctx):
	await ctx.send(f'{ctx.author.mention}, latence de {round(bot.latency, 3)} ms')

#commande github
@bot.command()
async def github(ctx):
	await ctx.send(f'{ctx.author.mention}, Voici la page GitHub de Bisounours : https://github.com/juliendechaud/bisounours-discord')

#commande github
@bot.command()
async def event(ctx, *arg):
	result = ""
	
	if arg[0] == "list":
		cache_result = db.event_list()
		for r in cache_result:
			result += f' Event : {r[3]}, le {r[4]}. Description : {r[5]} \n'
	elif arg[0] == "add":
		result == db.event_add(ctx.message.guild.id, ctx.author.id, arg[1], arg[3], arg[2])
		print(f'result : {result}')
	await ctx.send(f' enorme : {result}')

#execute le bot
bot.run(TOKEN)

#end of line