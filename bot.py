#code source de bisounours-discord par Julien Dechaud
#https://github.com/juliendechaud/bisounours-discord

#importation des modules
import os
from dotenv import load_dotenv #variables d'environnement
import discord #api discord
from discord.ext import commands #gestion des commandes
import datetime
import db
import embed

#initialisation
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Client()
intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix='$', intents=intents)
db = db.db("bisounours.db")
emgen = embed.embedcreator()

#quand le bot est prêt
@bot.event
async def on_ready():
	print(f'{bot.user} ready to work !')
	print(f'Connecté sur {len(bot.guilds)} serveur(s)')
	await bot.change_presence(activity=discord.Game("$help"))

#event a chaque message posté
@bot.event
async def on_message(message):
	nbr_banword = 0
	if message.author.id!=bot.user.id:
		for banword in db.banword_list_mot(message.guild.id):
			if banword[0] in message.content:
				nbr_banword += 1

		if nbr_banword>0:
			await message.delete()
			await message.channel.send(f"J'ai trouvé {nbr_banword} banword(s) dans ton message {message.author.mention}... fais attention !")
	await bot.process_commands(message)

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
	
	if len(arg) > 0:
		if arg[0] == "list-all":
			cache_result = db.event_list(ctx.guild.id)
			for r in cache_result:
				cree = bot.get_user(r[2])
				await ctx.send(embed=emgen.event(r[3], r[4], r[5], cree, r[0]))

		elif arg[0] == "list":
			cache_result = db.event_list_after(ctx.guild.id)
			for r in cache_result:
				cree = bot.get_user(r[2])
				await ctx.send(embed=emgen.event(r[3], r[4], r[5], cree, r[0]))

		elif arg[0] == "add":
			uneDate = datetime.datetime.strptime(arg[3], '%d-%m-%Y')
			db.event_add(ctx.guild.id, ctx.author.id, arg[1], uneDate.date(), arg[2])
			await ctx.send("event ajouter !")

		elif arg[0] == "del":
			if arg[1]!=None:
				if db.event_del(ctx.guild.id, arg[1]).rowcount == 1:
					await ctx.send(f'{ctx.author.mention}, event supprimer !')
				else:
					await ctx.send(f'{ctx.author.mention}, cette event n\'existe pas !')

		else:
			await ctx.send("$help event")

#applique des avertissements 
@bot.command()
@commands.has_permissions(kick_members=True, ban_members=True)
async def warning(ctx, arg, member: discord.Member=None, message=None):
	
	if arg=="add":
		if member != None:
			db.warning_add(ctx.guild.id, ctx.author.id, member.id, message)
			await ctx.send(f'{member.mention}, attention vous avez un warning !')
		else:
			await ctx.send(f'{ctx.author.mention}, vous devez mettre un utilisateur.')

	elif arg=="list":
		result = ""
		cache_result = db.warning_list(ctx.guild.id)
		for r in cache_result:
			cree = bot.get_user(r[2])
			pour = bot.get_user(r[3])
			result += f'\nWarning à {pour.mention} crée par {cree.mention}, le {r[4]}. Raison : {r[5]}'
		await ctx.send(f'{ctx.author.mention}, {result}')

#si la commande ne passe pas
@warning.error
async def warning_error(ctx, error):
	await ctx.send(f'{ctx.author.mention}, j\'ai rencontré un problème : {error}')

#gestion des banwords
@bot.command()
@commands.has_permissions(manage_messages=True)
async def banword(ctx, arg, word=None):
	if arg=="add":
		if word!=None and len(word)<=40:
			db.banword_add(ctx.guild.id, ctx.author.id, word)
			await ctx.send(f'{ctx.author.mention}, banword ajouter !')
		else:
			await ctx.send(f'{ctx.author.mention}, il faut écrire un banword (max 40 caractères) !')

	elif arg=="del":
		if word!=None:
			if db.banword_del(ctx.guild.id, word).rowcount == 1:
				await ctx.send(f'{ctx.author.mention}, banword supprimer !')
			else:
				await ctx.send(f'{ctx.author.mention}, ce baword n\'existe pas !')

	elif arg=="list":
		cache_result = db.banword_list(ctx.guild.id)
		for r in cache_result:
			cree = bot.get_user(r[2])
			result = emgen.banword(r[3], cree, r[0])
			await ctx.send(embed=result)
	
#si la commande ne passe pas
@banword.error
async def banword_error(ctx, error):
	await ctx.send(f'{ctx.author.mention}, j\'ai rencontré un problème : {error}')

#execute le bot
bot.run(TOKEN)

#end of line