# -*- coding: utf-8 -*-
import pymysql
import csv

#se connecter à la base de donnée
connection = pymysql.connect(user='dave', host='localhost', password='dave')
cur = connection.cursor()

#definissons une fonction pour ajouter une table à la base de donnée
def ajout():
	cur = connection.cursor()
	#cur.execute("set global local_infile = 1 ")
	#connection.commit()
	#Se connecter à la base de donnée dave
	cur.execute("use dave")
	#cur.execute('drop table personne')
	#Créer une table 
	cur.execute ("create table personne (id int PRIMARY KEY, Nom VARCHAR(10),Prenom VARCHAR(15), Localite VARCHAR(15),Facture VARCHAR(32))")
	# enregistrer les valeur dans la base de de bonnées 
	connection.commit()

	#importont un fichier csv dans une table 
	#repertorier le ficher à importer dans le repertoire par défaut. trouver le répertoir à partir de cette commande show variables like 'secure_file_priv' 

	cur.execute("load data  infile '/var/lib/mysql-files/classeur2.csv' into table personne fields terminated by ';' lines terminated by '\r\n' ignore 1 lines ")
	connection.commit()
	cur.execute("select * from personne")
	rows1 = cur.fetchall()
	print(rows1)

#pour modifier la valeur de la colone d'une table 
def modif():
	cur = connection.cursor()
	cur.execute("use dave")
	cur.execute("update personne set Facture = 'BBB' ")
	connection.commit()
	cur.execute("select * from personne")
	rows2 = cur.fetchall()
	print(rows2)

# cette fonction vas nous permettre de cypter la colone d'un champ
def crypt():
	cur = connection.cursor()
	cur.execute("use dave")
	cur.execute("alter table personne modify column Facture varbinary(32)")
	cur.execute("update personne set Facture = aes_encrypt(Facture,'newpaper')")
	connection.commit()
	cur.execute("select * from personne")
	rows3= cur.fetchall()
	print(rows3)

def decrypt():
	cur = connection.cursor()
	cur.execute("use dave")
	cur.execute("update personne set Facture = aes_decrypt(Facture,'newpaper')")
	cur.execute("alter table personne modify column Facture varchar(32)")
	connection.commit()
	cur.execute("select * from personne")
	rows4= cur.fetchall()
	print(rows4)

#cette fonction nous permettra d'afficher la table concernée
def aff():
	cur=connection.cursor()
	cur.execute("use dave")
	cur.execute("select * from personne")
	rows5= cur.fetchall()
	print(rows5)

#utilison une boucle pour appler la fonction de notre choix
A = 1
B = 2
E = 3
F = 4
G = 5

a = "\n Tapez 1 pour ajouter une table dans la base de données \n Tapez 2 pour modifier une colonne de la table \n Taper 3 pour crypter la colonde d'une table \n Tapez 4 pour décrypter la colone  \n Tapez 5 pour afficher la table "

print (a)

try:
	C = int(input('entrez un chiffre entre 1 et 5: '))
	if C == A:
		try:
			ajout()
			aff()
			pass
		except pymysql.err.OperationalError :
			print("cette table exite déja dans la base de donnée")
			pass 

	elif C == B :
		try:
			modif()
			aff()
			pass
		except pymysql.err.ProgrammingError:
			print("cette table n'existe pas dans la base de donnée")
			pass
		
	elif C == E :
		try:
			crypt()
			aff()
			pass
		except pymysql.err.ProgrammingError :
			print("cette table n'existe pas dans la base de donnée")
			pass
		
	elif C == F :
		try:
			decrypt()
			aff()
			pass
		except pymysql.err.ProgrammingError :
			print("cette table n'existe pas dans la base de donnée")
			pass
		
	elif C == G :
		try:
			aff()
			pass
		except pymysql.err.ProgrammingError:
			print("cette table n'existe pas dans la base de donnée")
			pass
		
	else :
		print("veillez entrez un nombre compris entre 1 et 5")
	pass
except ValueError :
		print("Vous avez entrez un chiffre incorrecte")
pass



