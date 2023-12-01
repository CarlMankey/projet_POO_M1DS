#!/bin/env python3
from base_livre import BaseLivre
import os
from reportlab.pdfgen import canvas
from ebooklib import epub

from urllib.request import urlopen  # utilisé pour récupérer l'html du site source
import re  # expressions régulières pour rechercher les liens de livres dans l'html
import ssl  # pour contourner les vérifications de la page
import urllib3 # idem
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # désactive l'avertissement de non-vérif
ssl._create_default_https_context = ssl._create_unverified_context  # permet de télécharger sans verif

FORMATS = ['pdf', 'epub']  # formats acceptés

class Bibli:
	def __init__(self, path):
		self.path = path
		self.livres = []  # Liste pour stocker les livres de la bibliothèque

		# Vérifier si le répertoire existe
		if not os.path.exists(self.path):
			os.mkdir(self.path)

	def ajouter(self, livre):
		"""Ajoute un livre à la bibliothèque s'il n'est pas déjà présent."""

		# On vérifie si le livre passé en argument est une instance de la classe BaseLivre.
		if not isinstance(livre, BaseLivre):
			raise ValueError("Le livre doit être une instance de la classe BaseLivre.")

		# On vérifie si le livre est déjà présent dans la bibliothèque.
		if livre in self.livres:
			raise ValueError(f"Le livre {livre.titre()} est déjà dans la bibliothèque.")

		self.livres.append(livre)
		print(f"Le livre {livre.titre()} a été ajouté à la bibliothèque.")

	def alimenter(self, url):

		# on récupère l'html du site source

		page = urlopen(url)
		html_bytes = page.read()
		html = html_bytes.decode("utf-8")

		# on récupère pour chaque format toutes les instances de type :
		# 'href="about_homme_oreille_cassee.pdf">',
		# 'href="achard_amedee_-_madame_rose.epub">', ETC...
		# dans l'html récupéré précedemment

		resultats = []
		for format_livre in FORMATS:
			resultats += re.findall(pattern='href=.*' + format_livre + '.*?>', string=html)
		print(resultats)

		# on finit de formater la liste d'url de livres,
		# en retirant le "href=" et en ajoutant l'url complète pour
		# avoir le chemin absolu des livres

		for i in range(len(resultats)):
			start_index = resultats[i].find("\"")
			resultats[i] = resultats[i][start_index + 1:]
			end_index = resultats[i].find("\"")
			resultats[i] = resultats[i][:end_index]

			# on retrouve l'url du dossier courant du site
			# (ex : en partant de http://site.fr/dossier/index , on doit
			# récupérer http://site.fr/dossier/ )

			index_dossier = url.rfind("/")
			url_dossier = url[:index_dossier+1]
			resultats[i] = url_dossier + resultats[i]

		# A présent résultats contient tous les liens de téléchargement.

		for lien in resultats[1:15] :
			try:
				livre = BaseLivre(lien)
				self.ajouter(livre)
			except ValueError as e :
				print(f'erreur lors de l\'ajout du livre : {e}')

		return len(resultats)  # permet de compter le nombre de livres telechargés -> pour scrap._nbmax

	def rapport_livres(self, format, fichier):
		try:
			format = format.upper()  # Convertir le format en majuscules pour la comparaison
			if format not in ['EPUB', 'PDF']:
				raise ValueError("Le format doit être 'EPUB' ou 'PDF'.")

			if format == 'PDF':


				c = canvas.Canvas(fichier + ".pdf", bottomup=False)
				txt_size = 10
				c.setFont("Helvetica", txt_size)
				pos_y = 60

				for livre in self.livres:
					if pos_y+txt_size*6 >txt_size*14*6 :
						c.showPage()
						c.setFont("Helvetica", txt_size)
						pos_y = 60
					c.drawString(60, pos_y, f'Titre: {livre.titre()}')
					pos_y += txt_size
					c.drawString(60, pos_y, f'Auteur: {livre.auteur()}')
					pos_y += txt_size
					c.drawString(60, pos_y, f'Format: {livre.type()}')
					pos_y += txt_size
					c.drawString(60, pos_y, f'Fichier: {livre.ressource}')
					pos_y += txt_size
					c.drawString(60, pos_y, "----------")
					pos_y += txt_size

				c.save()
				print(f"Le rapport a été généré avec succès dans le fichier {fichier}.")

			elif format == 'EPUB':

				rapport = ""
				for livre in self.livres:
					rapport += f"<p>Titre : {livre.titre()}</p>"
					rapport += f"<p>Auteur : {livre.auteur()}</p>"
					rapport += f"<p>Type : {livre.type()}</p>"
					rapport += f"<p>Ressource : {livre.ressource}</p>"
					rapport += "--------------"

				book = epub.EpubBook()

				book.set_identifier('sample123456')
				book.set_title('Rapport Livres')
				book.set_language('fr')

				c1 = epub.EpubHtml(title='Introduction', file_name='intro.xhtml', lang='fr')
				c1.content = rapport

				book.add_item(c1)

				book.add_item(epub.EpubNcx())
				book.add_item(epub.EpubNav())

				book.spine = [c1]

				epub.write_epub(fichier + '.epub', book, {})
				print(f"Le rapport a été généré avec succès dans le fichier {fichier}.")

		except ValueError as e:
			print(e)
			return 0

	def rapport_auteurs(self, format, fichier):
		try:
			format = format.upper()  # Convertir le format en majuscules pour la comparaison
			if format not in ['EPUB', 'PDF']:
				raise ValueError("Le format doit être 'EPUB' ou 'PDF'.")

			rapport_auteurs = {}  # Un dictionnaire pour stocker les informations sur les auteurs

			for livre in self.livres:

				auteur = livre.auteur()
				if auteur not in rapport_auteurs:
					rapport_auteurs[auteur] = []

				rapport_auteurs[auteur].append(livre)

			if format == 'PDF':
				c = canvas.Canvas(fichier + ".pdf", bottomup=False)
				txt_size = 10
				c.setFont("Helvetica", txt_size)
				pos_y = 60
				pos_droite = c._pagesize[0] - 10 # position de depart pour l'alignement a droite des infos

				for auteur in rapport_auteurs:
					c.drawString(60, pos_y, f'Auteur: {auteur}')
					for livre in rapport_auteurs[auteur]:
						if pos_y + txt_size * 6 > txt_size * 14 * 6:
							c.showPage()
							c.setFont("Helvetica", txt_size)
							pos_y = 60

						# quelques superbes ouvrages ont un titre de 1 milliard de caractères, on
						# doit donc gérer pour les découper et les afficher sur plusieurs lignes :
						long_max_titre = txt_size*5
						if len(str(livre.titre())) > long_max_titre :
							c.drawRightString(pos_droite, pos_y, f'Titre: {livre.titre()[:long_max_titre]}')
							pos_y += txt_size
							c.drawRightString(pos_droite, pos_y, f'{livre.titre()[long_max_titre:]}')
							pos_y += txt_size
						else :
							c.drawRightString(pos_droite, pos_y, f'Titre: {livre.titre()}')
							pos_y += txt_size
						c.drawRightString(pos_droite, pos_y, f'Format: {livre.type()}')
						pos_y += txt_size
						c.drawRightString(pos_droite, pos_y, f'Fichier: {livre.ressource}')
						pos_y += txt_size
						c.drawRightString(pos_droite, pos_y, "----------")
						pos_y += txt_size

					if pos_y + txt_size * 6 > txt_size * 14 * 6:
						c.showPage()
						c.setFont("Helvetica", txt_size)
						pos_y = 60
					pos_y += txt_size
					c.drawString(60, pos_y, '=' * 50)
					pos_y += txt_size * 2

				c.save()
				print(f"Le rapport a été généré avec succès dans le fichier {fichier}.")

			elif format == 'EPUB':

				rapport = ""
				for auteur in rapport_auteurs:
					rapport += f"<h3>Auteur : {auteur}</h3>"
					for livre in rapport_auteurs[auteur]:
						rapport += f"<p>Titre : {livre.titre()}</p>"
						rapport += f"<p>Type : {livre.type()}</p>"
						rapport += f"<p>Ressource : {livre.ressource}</p>"
						rapport += "--------------"

				book = epub.EpubBook()

				book.set_identifier('sample654321')
				book.set_title('Rapport Auteur')
				book.set_language('fr')

				c1 = epub.EpubHtml(title='Rapport Auteurs', file_name='rapport_auteurs.xhtml', lang='fr')
				c1.content = rapport

				book.add_item(c1)

				book.add_item(epub.EpubNcx())
				book.add_item(epub.EpubNav())

				book.spine = [c1]

				epub.write_epub(fichier + '.epub', book, {})

				print(f"Le rapport a été généré avec succès dans le fichier {fichier}.")


		except Exception as e:
			raise FileNotFoundError(f"Erreur lors de la génération de l'état des auteurs : {str(e)}")


# test
# Créez une instance de base_bibli en fournissant le chemin du répertoire
bibli = Bibli("./Livres")

bibli.alimenter("https://tibo.life/index3")



# Testez la méthode rapport_livres

bibli.rapport_livres('PDF', 'rapport_livres')
bibli.rapport_livres('EPUB', 'rapport_livres')
# Testez la méthode rapport_auteurs

bibli.rapport_auteurs('PDF', 'rapport_auteurs')
bibli.rapport_auteurs('EPUB', 'rapport_auteurs')
