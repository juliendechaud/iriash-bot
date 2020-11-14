#iriash's source code by Julien Dechaud
#https://github.com/juliendechaud/iriash-bot

#importation des modules
import os
from dotenv import load_dotenv #variables d'environnement
import discord #api discord
from discord.ext import commands #gestion des commandes
from discord.ext.commands import has_permissions #gestion des permissions des utilisateurs

#initialisation
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Client()
intents = discord.Intents.default() #droits pour la récupération des informations depuis discord
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

#quand le bot est prêt
@bot.event
async def on_ready():
	print(str(bot.user) + " prêt à travailler !")
	print("Connecté sur " + str(len(bot.guilds)) + " serveur(s)")
	await bot.change_presence(activity=discord.Game("$help"))

#commande latence
@bot.command()
async def ping(ctx):
    await ctx.send("Latence de " + str(round(bot.latency, 3)) + "ms")

#commande suppression de x messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, mnt=10):
	await ctx.channel.purge(limit=mnt+1)
@clear.error
async def clear_error(ctx, error):
	await ctx.send(str(error))

#commande pour avoir des infos sur un utilisateur
@bot.command()
async def cki(ctx, member: discord.Member=None):
	try:
		if member.nick==None:
			embed=discord.Embed(title=str(member.name))
		else:
			embed=discord.Embed(title=str(member.name) + " aka " + str(member.nick))
		embed.set_thumbnail(url=str(member.avatar_url))
		embed.add_field(name="Création :", value=str(member.created_at.date()), inline=True)
		await ctx.send(embed=embed)
	except:
		await ctx.send(ctx.message.author.mention + ", la commande s'écrit -> $cki @User")
@cki.error
async def cki_error(ctx, error):
	await ctx.send(str(error))

@bot.command()
async def github(ctx):
	await ctx.send("La page GitHub de Iriash : https://github.com/juliendechaud/iriash-bot")

@bot.command()
async def bug(ctx):
	await ctx.send("Si vous voyez un bug dites le ici : https://github.com/juliendechaud/iriash-bot/issues")

#run the bot
bot.run(TOKEN)