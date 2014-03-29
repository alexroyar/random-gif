#!usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb

DATABASE = 'test'
TABLE = 'prueba'

class pruebaMYSQL:
	"""
		Constructor. No crea la base de datos ni nada.
	"""
	def __init__(self):
		self.con = mdb.connect('localhost', 'fer', 'fer', DATABASE)
		self.cursor = self.con.cursor()

	"""
		Crea la tabla de turno. La vacía si existe.
	"""
	def create_table(self, table):
		query = "DROP TABLE IF EXISTS %s" % (table)
		self.cursor.execute(query);
		query = "CREATE TABLE %s(url VARCHAR(150) NOT NULL," % (table)
		query += "name VARCHAR(150) NOT NULL, PRIMARY KEY (url))"
		self.cursor.execute(query);

	"""
		Desconexión de la base de datos.
	"""
	def disconnect(self):
		if (self.con): self.con.close()

	"""
		Añade un elemento a la base de datos.
	"""
	def insert_into_table(self, url, name):
		try:
			query = "INSERT INTO %s values(%s, %s)" % (TABLE, "'"+url+"'", "'"+name+"'")
			self.cursor.execute(query)
		except Exception as e:
			print "Exception:", e

	"""
		Mete valores de relleno para hacer pruebas.
	"""
	def insert_demo(self):
		for i in range(0, 10): self.insert_into_table("http://%d.gif" % i, "IMG_%d.gif" % i)

	"""
		Devuelve una lista de las filas de la tabla.
	"""
	def get_all_rows(self):
		if (not self.con):
			print "No hay conexión."
			return ()

		query = "SELECT * from %s" % (TABLE)
		self.cursor.execute(query)
		res = self.cursor.fetchall()
		return res

#ddbb = pruebaMYSQL()
#ddbb.create_table('prueba')
#ddbb.insert_demo()
#print ddbb.get_all_rows()