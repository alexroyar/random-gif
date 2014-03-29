#!usr/bin/python
# -*- coding: utf-8 -*-

import praw
import urllib
import time
import pruebaMYSQL as ddbb

USER_AGENT = "GIF_Collector_Test_v0" # Nombre de nuestro script.
LIMIT = 25 # Peticiones que se hacen de golpe.
SUB_REDDIT = "gifs" # Nombre del subreddit a explotar.
SEPARATOR = "/"	# Separador de URLs.
PATH = "images/" # Ruta provisional de imágenes.
TIME_SLEEP = 2 	# Reddit pide dos segundos entre petición y petición.

# Tipos
GET_TOP_HOUR 	= 1
GET_TOP_DAY 	= 2
GET_TOP_WEEK 	= 3
GET_TOP_MONTH 	= 4

def get_random_submission(save=False):
	try:
		dicc = createDiccFromDB()
		connection = praw.Reddit(user_agent = USER_AGENT)
		connection_ddbb = ddbb.pruebaMYSQL()
	
		while (True):
			try:
				# Pilla un gif aleatorio.
				sub = connection.get_subreddit(SUB_REDDIT).get_random_submission()
				
				# Spliteamos su url.
				url = sub.url
				name = url.split(SEPARATOR)[-1]

				# Caso provisional de imágenes de imgur.
				if (not ".gif" in name and "imgur" in url):
					print "Imagen especial. Añadimos terminación, a ver si cuela."
					print name
					print url
					name += ".gif"
					url = "http://i.imgur.com/" + name
					
				
				# Si no tenemos ya la imagen, la descargamos.
				if (not dicc.has_key(url)):
					dicc[url] = name
					connection_ddbb.insert_into_table(url, name)
					if save: urllib.urlretrieve(url, PATH + name)

			except Exception as exc:
				print "Exception In:", exc

			finally:
				time.sleep(2)

	except Exception as exc:
		print "Exception Out:", exc

	finally:
		print "Cerramos base de datos en el finally."
		connection_ddbb.disconnect()

def get_top(type, num, save=False):
	try:
		dicc = createDiccFromDB()
		connection = praw.Reddit(user_agent = USER_AGENT)
		connection_ddbb = ddbb.pruebaMYSQL()

		if (type == GET_TOP_HOUR):
			submissions = connection.get_subreddit(SUB_REDDIT).get_top_from_hour(limit = num)
		elif (type == GET_TOP_DAY):
			submissions = connection.get_subreddit(SUB_REDDIT).get_top_from_day(limit = num)
		elif (type == GET_TOP_WEEK):
			submissions = connection.get_subreddit(SUB_REDDIT).get_top_from_week(limit = num)
		elif (type == GET_TOP_MONTH):
			submissions = connection.get_subreddit(SUB_REDDIT).get_top_from_month(limit = num)
		else:
			raise Exception("Constante %d no definida." % type)

		# Recorremos los objetos Submission.
		for sub in submissions:
			# Spliteamos su url.
			url = sub.url
			name = url.split(SEPARATOR)[-1]
			
			# Caso provisional de imágenes de imgur.
			if (not ".gif" in name and "imgur" in url):
				print "Imagen especial. Añadimos terminación, a ver si cuela."
				print name
				print url
				name += ".gif"
				url = "http://i.imgur.com/" + name
				
			# Si no tenemos ya la imagen, la descargamos.
			if (not dicc.has_key(url)):
				dicc[url] = name
				connection_ddbb.insert_into_table(url, name)
				if save: urllib.urlretrieve(url, PATH + name)


	except Exception as exc:
		print "Exception Out:", exc

	finally:
		print "Cerramos base de datos en el finally."
		connection_ddbb.disconnect()
		time.sleep(TIME_SLEEP)

"""
	Encuentra las mejores imágenes de la última hora.
"""
def get_top_from_hour(num=LIMIT):
	get_top(GET_TOP_HOUR, num)

"""
	Encuentra las mejores imágenes del día.
"""
def get_top_from_day(num=LIMIT):
	get_top(GET_TOP_DAY, num)

"""
	Encuentra las mejores imágenes de la semana.
"""
def get_top_from_week(num=LIMIT):
	get_top(GET_TOP_WEEK, num)

"""
	Encuentra las mejores imágenes del mes.
"""
def get_top_from_month(num=LIMIT):
	get_top(GET_TOP_MONTH, num)

"""
	Devuelve un diccionario con el contenido de la DDBB.
"""
def createDiccFromDB():
	connection_ddbb = ddbb.pruebaMYSQL()
	rows = connection_ddbb.get_all_rows()
	connection_ddbb.disconnect()
	
	diccionario = {}
	for row in rows: diccionario[row[0]] = row[1]
	
	print "Diccionario tiene %d elementos." % len(diccionario)
	return diccionario

def main():
	#createDiccFromDB()
	get_top_from_month()
	get_top_from_week()
	get_top_from_day()
	get_top_from_hour()
	get_random_submission()


main()