import sqlite3

class db():
	def __init__(self, db_path):
		self.conn = sqlite3.connect(db_path)
		self.cur = self.conn.cursor()

	def execute(self, query):
		self.cur.execute(query)
		self.conn.commit()
		return self.cur

	def server_add(self, id_server):
		return self.execute(f"INSERT INTO server (id) VALUES ({id_server})")

	def event_add(self, id_server, cree_par, libelle, dateheure, description):
		return self.execute(f'INSERT INTO event (id_server, cree_par, libelle, dateheure, description) VALUES ({id_server}, {cree_par}, "{libelle}", "{dateheure}", "{description}")')

	def event_list(self, id_server):
		result = self.execute(f'SELECT * FROM event WHERE id_server = {id_server} order by dateheure')
		return result.fetchall()

	def event_list_after(self, id_server):
		result = self.execute(f'SELECT * FROM event WHERE id_server = {id_server} and dateheure >= date() order by dateheure')
		return result.fetchall()

	def warning_list(self):
		result = self.execute("SELECT * FROM warning")
		return result.fetchall()

	def __del__(self):
		self.conn.close()