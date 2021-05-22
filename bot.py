#code source de bisounours-discord par Julien Dechaud
#https://github.com/juliendechaud/bisounours-discord

#importation des modules
import os
from dotenv import load_dotenv #variables d'environnement
import discord #api discord
from discord.ext import commands #gestion des commandes
import datetime
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

#supprime x message(s)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, mnt=10):
	await ctx.channel.purge(limit=mnt+1)

#si la commande ne passe pas
@clear.error
async def clear_error(ctx, error):
	await ctx.send(f'{ctx.author.mention}, j\'ai rencontré un problème : {error}')

#commande github
@bot.command()
async def event(ctx, *arg):
	result = ""
	
	if len(arg) > 0:
		if arg[0] == "list-all":
			cache_result = db.event_list(ctx.guild.id)
			for r in cache_result:
				result += f'\nEvent : {r[3]}, le {r[4]}. Description : {r[5]}'

		elif arg[0] == "list":
			cache_result = db.event_list_after(ctx.guild.id)
			for r in cache_result:
				result += f'\nEvent : {r[3]}, le {r[4]}. Description : {r[5]}'

		elif arg[0] == "add":
			uneDate = datetime.datetime.strptime(arg[3], '%d-%m-%Y')
			db.event_add(ctx.guild.id, ctx.author.id, arg[1], uneDate.date(), arg[2])
			result = "event ajouter !"

		else:
			result = "$help event"

	else:
		result = "$help event"

	await ctx.send(f'{ctx.author.mention}, {result}')

#applique des avertissements 
@bot.command()
@commands.has_permissions(kick_members=True, ban_members=True)
async def warning(ctx, member: discord.Member=None):
	if member != None:
		await ctx.send(f'{member.mention}, attention vous avez un warning !')
	else:
		await ctx.send(f'{ctx.author.mention}, vous devez mettre un utilisateur.')

#si la commande ne passe pas
@warning.error
async def warning_error(ctx, error):
	await ctx.send(f'{ctx.author.mention}, j\'ai rencontré un problème : {error}')

#execute le bot
bot.run(TOKEN)

#end of line