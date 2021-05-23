import discord #import du module discord

class embedcreator():

	def event(self, title, date, description, auteur, id_event):
		""" création du embed pour les events """
		embed=discord.Embed(title = "Event : " + str(title) + ", le : " + str(date), description = str(description), color=0x00ffd5)
		embed.set_thumbnail(url="https://www.housingeurope.eu/image/167/sectionheaderpng/events.png")
		embed.set_footer(text = "EventID : " + str(id_event) + " , crée par : " + str(auteur))
		return embed

	def banword(self, banword, auteur, id_banword):
		""" création du embed pour les banwords """
		embed=discord.Embed(title = "Banword : " + str(banword), color=0xff0000)
		embed.set_footer(text = "BanwordID : " + str(id_banword) + " , crée par : " + str(auteur))
		return embed