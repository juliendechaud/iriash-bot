import sqlite3 #module sqlite

class db():
	def __init__(self, db_path):
		""" création de l'objet db avec en paramètre le chemin d'accès a la base de donnée """
		self.conn = sqlite3.connect(db_path)
		self.cur = self.conn.cursor()

	def execute(self, query):
		""" fonction pour exectuer les requêtes sql """
		self.cur.execute(query)
		self.conn.commit()
		return self.cur

	#fonctions pour les events
	def event_add(self, id_server, cree_par, libelle, dateheure, description):
		""" ajout d'un event en base de donnée en fonction du serveur discord """
		return self.execute(f'INSERT INTO event (id_server, cree_par, libelle, dateheure, description) VALUES ({id_server}, {cree_par}, "{libelle}", "{dateheure}", "{description}")')

	def event_list(self, id_server):
		""" liste des events en base de donnée en fonction du serveur discord """
		result = self.execute(f'SELECT * FROM event WHERE id_server = {id_server} order by dateheure')
		return result.fetchall()

	def event_list_after(self, id_server):
		""" liste des events en base de donnée en fonction du serveur discord et seulement après ou pendant la date actuelle"""
		result = self.execute(f'SELECT * FROM event WHERE id_server = {id_server} and dateheure >= date() order by dateheure')
		return result.fetchall()

	def event_del(self, id_server, event_id):
		""" suppression d'un event en base de donnée en fonction du serveur discord et de son id """
		return self.execute(f'DELETE FROM event WHERE id_server = {id_server} AND id = {event_id}')

	def event_check(self, id_server):
		""" suppression d'un event en base de donnée en fonction du serveur discord et de son id """
		result = self.execute(f'SELECT * FROM event WHERE id_server = {id_server} AND dateheure = date()')
		return result.fetchall()	

	#fonctions pour les warnings
	def warning_add(self, id_server, cree_par, pour, message):
		""" ajout d'un warning en base de donnée en fonction du serveur discord """
		return self.execute(f'INSERT INTO warning (id_server, cree_par, pour, dateheure, message) VALUES ({id_server}, {cree_par}, {pour}, datetime(), "{message}")')

	def warning_list(self, id_server):
		""" liste des warnings en fonction du serveur discord """
		result = self.execute(f'SELECT * FROM warning WHERE id_server = {id_server}')
		return result.fetchall()

	#fonctions pour les banwords
	def banword_add(self, id_server, cree_par, mot):
		""" ajout d'un banword en base de donnée en fonction du serveur discord """
		return self.execute(f'INSERT INTO banword (id_server, cree_par, mot) VALUES ({id_server}, {cree_par}, "{mot}")')

	def banword_list(self, id_server):
		""" liste des banwords et de leurs informations en fonction du serveur discord """
		result = self.execute(f'SELECT * FROM banword WHERE id_server = {id_server}')
		return result.fetchall()

	def banword_list_mot(self, id_server):
		""" liste uniquement des banwords en fonction du serveur discord """
		result = self.execute(f'SELECT mot FROM banword WHERE id_server = {id_server}')
		return result.fetchall()

	def banword_del(self, id_server, banword_id):
		""" suppression d'un banword en base de donnée en fonction du serveur discord et de son id """
		return self.execute(f'DELETE FROM banword WHERE id_server = {id_server} AND id = {banword_id}')

	#fonctions pour la gestion du channel d'annonce
	def channel_add(self, id_server, id_channel, cree_par):
		""" ajout d'un channel d'annonce en base de donnée en fonction du serveur discord """
		return self.execute(f'INSERT INTO eventchannel (id_server, id_channel, cree_par) VALUES ({id_server}, {id_channel}, {cree_par})')

	def channel_list(self, id_server):
		""" ajout d'un channel d'annonce en base de donnée en fonction du serveur discord """
		result = self.execute(f'SELECT * FROM eventchannel WHERE id_server = {id_server}')
		return result.fetchall()

	def channel_del(self, id_server):
		""" ajout d'un channel d'annonce en base de donnée en fonction du serveur discord """
		return self.execute(f'DELETE FROM eventchannel WHERE id_server = {id_server}')

	def __del__(self):
		""" quand on détruit l'objet, on ferme la connection a la base de donnée """
		self.conn.close()
