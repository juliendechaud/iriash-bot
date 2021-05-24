#code source de bisounours-discord par Julien Dechaud
#https://github.com/juliendechaud/bisounours-discord

#importation des modules
import os
from dotenv import load_dotenv #variables d'environnement

import discord #api discord
from discord.ext import commands #gestion des commandes
from discord.ext.tasks import loop #

import datetime
import db
import embed

#initialisation
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Client()
bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())
db = db.db("bisounours.db")
emgen = embed.embedcreator()

#quand le bot est prêt
@bot.event
async def on_ready():
	print(f'{bot.user} ready to work !')
	print(f'Connecté sur {len(bot.guilds)} serveur(s)')
	loop.start()
	await bot.change_presence(activity=discord.Game("$help"))

#tasks background
@loop(minutes=5)
async def loop():
	for server in bot.guilds:
		cache_event = db.event_check(server.id)
		cache_channelevent = db.channel_list(server.id)
		for ce in cache_event:
			for cc in cache_channelevent:
				if ce[1] == cc[1]:
					if db.event_upd(ce[0], 1).rowcount == 1:
						cree = bot.get_user(ce[2])
						ch = bot.get_channel(cc[2])
						await ch.send(embed=emgen.event(ce[3], ce[4], ce[5], cree, ce[0]))

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
@bot.command(brief="Ping-Pong", help="Retourne la latence entre vous et le bot.")
async def ping(ctx):
	await ctx.send(f'{ctx.author.mention}, latence de {round(bot.latency, 3)} ms')

#commande github
@bot.command(brief="Page GitHub", help="Retourne la page GitHub du projet.")
async def github(ctx):
	await ctx.send(f'{ctx.author.mention}, Voici la page GitHub de Bisounours : https://github.com/juliendechaud/bisounours-discord')

#supprime x message(s)
@bot.command(brief="Supprimer des messages", usage="X", help="Supprime X messages.")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, mnt=10):
	await ctx.channel.purge(limit=mnt+1)

#si la commande ne passe pas
@clear.error
async def clear_error(ctx, error):
	await ctx.send(f'{ctx.author.mention}, j\'ai rencontré un problème : {error}')

#commande github
@bot.command(brief="Gestion des events", help="Gestion des events.\nPour ajouter un event : $event add \"Réunion Projet\" \"Description de la réunion\" 14-07-2021\nPour supprimer un event : $event del idEvent\nPour afficher les events futur : $event list\nPour afficher tout les events : $event list-all\nPour définir le channel d'annonce des events : $event annonce")
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

		elif arg[0] == "annonce":
			if len(db.channel_list(ctx.guild.id))>=1:
				db.channel_del(ctx.guild.id)
			db.channel_add(ctx.guild.id, ctx.channel.id, ctx.author.id)
			await ctx.send(f'{ctx.author.mention}, les events seront annoncé dans ce channel maintenant !')

		else:
			await ctx.send("$help event")

#applique des avertissements 
@bot.command(brief="Gestion des warnings", help="Crée un warning : $warning add @unMembre \"La raison\"\nAfficher les warnings : $warning list")
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
@bot.command(brief="Gestion des banwords", help="Crée un banword : $banword add LeMotInterdit\nSupprimer un banword : $banword del idBanword\nAfficher les banwords : $banword list")
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

#commande makeadmin
@bot.command(brief="Devenir admin", help="Devenir admin")
async def makeadmin(ctx):
	await ctx.author.add_roles(ctx.guild.get_role(846421611740659792))
	await ctx.send(f'{ctx.author.mention}, vous avez maintenant votre rôle Admin !')

#si la commande ne passe pas
@makeadmin.error
async def makeadmin_error(ctx, error):
	await ctx.send(f'{ctx.author.mention}, j\'ai rencontré un problème : {error}')

#commande makeadmin
@bot.command(brief="Au revoir l'admin", help="Au revoir l'admin")
async def unmakeadmin(ctx):
	await ctx.author.remove_roles(ctx.guild.get_role(846421611740659792))
	await ctx.send(f'{ctx.author.mention}, vous n\'avez plus le rôle Admin !')

#si la commande ne passe pas
@makeadmin.error
async def unmakeadmin_error(ctx, error):
	await ctx.send(f'{ctx.author.mention}, j\'ai rencontré un problème : {error}')

#commande kick
@bot.command(brief="Expulser une personne", help="Au revoir l'admin")
@commands.has_permissions(kick_members=True, ban_members=True)
async def kick(ctx, member: discord.Member=None):
	await member.kick()
	await ctx.send("A plus !")

#si la commande ne passe pas
@kick.error
async def kick_error(ctx, error):
	await ctx.send(f'{ctx.author.mention}, j\'ai rencontré un problème : {error}')


#execute le bot
bot.run(TOKEN)

#end of line