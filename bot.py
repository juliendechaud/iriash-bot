#code source de bisounours-discord par Julien Dechaud
#https://github.com/juliendechaud/bisounours-discord

#importation des modules
import os
from dotenv import load_dotenv #variables d'environnement
import discord #api discord
from discord.ext import commands #gestion des commandes

#initialisation
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Client()
bot = commands.Bot(command_prefix='$')

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

#execute le bot
bot.run(TOKEN)

#end of line