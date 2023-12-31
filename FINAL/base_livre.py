#!/bin/env python3
import requests
import magic
from ebooklib import epub
import PyPDF2
from PyPDF2 import PdfReader
import os

import urllib3
import ssl


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # désactive l'avertissement de non-vérif
ssl._create_default_https_context = ssl._create_unverified_context  # permet de télécharger sans verif



class BaseLivre:
	def __init__(self, ressource, bibli):
		self.ressource = ressource
		self.contenu = None  # initialisé à None
		self.bibli = bibli

		# Vérifier si ressource est une URL ou un fichier local
		if self.est_url(ressource):
			try:
				self.ajouter_depuis_url()
				with open(self.ressource, 'rb') as fichier:
					self.contenu = fichier.read()
			except requests.exceptions.RequestException as e:
				print(f"Une erreur s'est produite lors de la requête HTTP : {e}")
				raise ValueError('Livre non obtenu.')
				return None
		else:
			# Si c'est un fichier local, lisez simplement le contenu du fichier
			try:
				with open(self.ressource, 'rb') as fichier:
					self.contenu = fichier.read()
			except FileNotFoundError:
				print(f"Le fichier {self.ressource} n'a pas été trouvé.")

	def ajouter_depuis_url(self):
		if not os.path.exists(self.bibli.bibli_dir):  # si le dossier qui contient les livres n'existe pas on le créé
			os.mkdir(self.bibli.bibli_dir)

		book = requests.get(self.ressource, verify=False)  # Récupere le contenu de la page
		book.raise_for_status()

		i = self.ressource.rfind('/')  # on garde la fin de l'url pour créer le nom du fichier
		nom_fichier = self.ressource[i:]

		with open(self.bibli.bibli_dir + nom_fichier, 'wb') as f:
			f.write(book.content)

		self.ressource = self.bibli.bibli_dir + nom_fichier  # maintenant la ressource est locale

	def est_url(self, chaine):
		return chaine.startswith("http://") or chaine.startswith("https://")

	def type(self):
		try:
			if self.contenu is not None:
				mime_info = magic.Magic().from_buffer(self.contenu)
				return "EPUB" if "EPUB document" in mime_info else "PDF" if "PDF document" in mime_info else "Autre"
			else:
				return "Contenu vide"
		except Exception as e:
			raise NotImplementedError(f"Erreur lors de la détermination du type : {e}")

	def extraire_les_données(self, key):
		try:
			if self.contenu is not None:
				if self.type() == "EPUB":
					# Utiliser la bibliothèque ebooklib pour extraire le titre d'un fichier EPUB
					book = epub.read_epub(self.ressource)
					metadata = book.get_metadata('DC', key)
					# En supposant que les metadonnées soit dans le fichier
					return metadata[0][0] if metadata else f"{key} non disponible"

				elif self.type() == "PDF":
					try:
						# Utiliser la bibliothèque PyPDF2 pour extraire le titre d'un fichier PDF
						with open(self.ressource, 'rb') as pdf_file:
							pdf_reader = PdfReader(pdf_file)

							# En supposant que les informations sont dans du document
							info = pdf_reader.metadata
							return getattr(info, key.lower(), f"{key} non disponible")
					except PyPDF2.utils.PdfReadError:
						return "Erreur lors de l'extraction du titre du PDF"
				else:
					return "Autre Format"
			else:
				return "Contenu vide"
		except Exception as e:
			raise NotImplementedError(f"Erreur lors de la détermination de la {key}: {e}")

	def titre(self):
		return self.extraire_les_données('title')

	def auteur(self):
		if self.type() == "EPUB":
			return self.extraire_les_données('creator')
		elif self.type() == "PDF":
			return self.extraire_les_données('author')
		else:
			return "Autre"

	def langue(self):
		return self.extraire_les_données('language')

	def sujet(self):
		return self.extraire_les_données('subject')

	def date(self):
		return self.extraire_les_données('date')


"""
# Test methodes avec un fichier EPUB
livre = BaseLivre("https://math.univ-angers.fr/~jaclin/biblio/livres/delly_-_l_exilee.epub")
print("Type:", livre.type())
print("Titre:",livre.titre())
print("Auteur:", livre.auteur())
print("Langue:", livre.langue())
print("Sujet:", livre.sujet())
print("Date:", livre.date())
print('\n')


# Test methodes avec un fichier PDF
livre = BaseLivre("https://math.univ-angers.fr/~jaclin/biblio/livres/defoe_moll_flanders.pdf")
print("Type:", livre.type())
print("Titre:",livre.titre())
print("Auteur:", livre.auteur())
"""

# *********************************
