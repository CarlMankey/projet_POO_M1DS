#! /usr/local/bin/python3.11
import sys

import bibli_scrap1
from datetime import datetime
import argparse
import configparser


def load_config(config_file):
	config = configparser.ConfigParser()
	config.read(config_file)
	return config


def main():
	parser = argparse.ArgumentParser(description="Bibli Application")
	parser.add_argument("-c", "--config", help="Spécifiez le fichier de configuration")
	parser.add_argument("command", choices=["collect", "reports"], help="Commande à exécuter")
	parser.add_argument("url", nargs="?", help="URL pour collectionner des livres")

	args = parser.parse_args()

	config_file = args.config or "bibli_conf.ini"
	config = load_config(config_file)

	if args.command == "collect":
		if not args.url:
			print("Veuillez fournir l'URL de collecte de livres.")
			return

		bibli_scrap = bibli_scrap1.BibliScrap(config.get("Directories", "bibliotheque"),
											  config.get("Directories", "etats"),
											  nbmax=config.getint("Parameters", "nbmax"))
		print(f"{bibli_scrap.bibli_dir=}, {bibli_scrap.etats_dir=}")
		_nbmax = bibli_scrap.nbmax  # scrap modifie la valeur self.nbmax. On la sauve ici avant le scrap...
		bibli_scrap.scrap(args.url, profondeur=1)
		bibli_scrap.nbmax = _nbmax  # ... on restaure la valeur de self.nbmax


	elif args.command == "reports":
		bibli_scrap = bibli_scrap1.BibliScrap(config.get("Directories", "bibliotheque"))

		# le script génère les rapports en PDF et EPUB avec les mêmes noms de fichier (rapport_livres et
		# rapport_auteurs). Cela pourrait entraîner l'écrasement des fichiers précédemment générés. Pour éviter cela,
		# On ajoute une estampille de date ou un autre identifiant unique au nom du fichier de rapport.
		# Ajoutez un identifiant unique basé sur la date et l'heure aux noms des fichiers de rapport
		timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

		bibli_scrap.rapport_livres('PDF', f"{config.get('Directories', 'etats')}/rapport_livres_{timestamp}")
		bibli_scrap.rapport_livres('EPUB', f"{config.get('Directories', 'etats')}/rapport_livres_{timestamp}")
		bibli_scrap.rapport_auteurs('PDF', f"{config.get('Directories', 'etats')}/rapport_auteurs_{timestamp}")
		bibli_scrap.rapport_auteurs('EPUB', f"{config.get('Directories', 'etats')}/rapport_auteurs_{timestamp}")

	else:
		print("Commande inconnue. Utilisez 'collect' ou 'reports'.")


if __name__ == "__main__":
	main()
