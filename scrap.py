import os
from urllib.request import urlopen  # utilisé pour récupérer l'html du site source
import re  # expressions régulières pour rechercher les liens de livres dans l'html
import requests
import ssl  # pour contourner les vérifications de la page
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # désactive l'avertissement de non-vérif
ssl._create_default_https_context = ssl._create_unverified_context  # permet de télécharger sans verif

FORMATS = ['pdf', 'epub']  # formats à rechercher dans le site source
URL = "https://tibo.life/index3.html"


def scrap(url, profondeur=1, nbmax=25):
	try:

		if profondeur == 0:
			raise StopIteration('Profondeur maximum atteinte.')

		nbmax_ = nbmax  # stockage local de nbmax

		# on ouvre la page en html pour chercher des liens vers .html
		print(f'{url=}')
		page = urlopen(url)
		html_bytes = page.read()
		html = html_bytes.decode("utf-8")

		# on récupère les liens vers d'autres pages à explorer
		liens = []
		liens += re.findall(pattern='href="/.*?>', string=html)
		liens += re.findall(pattern='href=\'/.*?>', string=html)
		print(f'{liens=}')

		for i in range(len(liens)) :
			start_index = liens[i].find('\'')
			liens[i] = liens[i][start_index+1:]
			end_index = liens[i].find('\'')
			liens[i] = liens[i][:end_index]

			liens[i] = url[:len(url)-12] + liens[i]
		print(f'{liens=}')

		# on récupère les liens vers des livres de format valide
		resultats = []
		for format_livre in FORMATS:
			resultats += re.findall(pattern='href=.*' + format_livre + '.*?>', string=html)

		# on finit de formater la liste d'url de livres,
		# en retirant le "href=" et en ajoutant l'url complète pour
		# avoir le chemin absolu des livres
		titres = []
		for i in range(len(resultats)):
			start_index = resultats[i].find("\"")
			resultats[i] = resultats[i][start_index + 1:]
			end_index = resultats[i].find("\"")
			resultats[i] = resultats[i][:end_index]

			titres.append(resultats[i])
			resultats[i] = url + resultats[i]

		# A présent résultats contient tous les liens de téléchargement.
		# On crée un dossier pour contenir les livres s'il n'existe pas
		if not os.path.exists("./Livres"):
			os.mkdir("./Livres")

		# on télécharge les livres dans le dossier Livres
		# tant que nbmax n'est pas atteint
		for i in range(len(resultats)):
			nbmax_ -= 1
			if nbmax_ > -1:
				r = requests.get(resultats[i], verify=False)
				with open("./Livres/" + titres[i], 'wb') as f:
					print(f"[{i + 1}] Téléchargement de {titres[i]}...")
					f.write(r.content)

			else:
				raise StopIteration('Max de téléchargements atteint.')
		print("Tous les livres de la page ont été chargés.")

		for lien in liens:
			scrap(lien, profondeur - 1, nbmax - nbmax_)

	except StopIteration as stop:
		print(stop)
		return 0


scrap(URL, profondeur=2, nbmax=70)
