import os
from urllib.request import urlopen  # utilisé pour récupérer l'html du site source
import re  # expressions régulières pour rechercher les liens de livres dans l'html
import requests
import ssl  # pour contourner les vérifications de la page
ssl._create_default_https_context = ssl._create_unverified_context


FORMATS = ['pdf', 'epub']  # formats à rechercher dans le site source
URL = "https://math.univ-angers.fr/~jaclin/biblio/livres/"

# on récupère l'html du site source

page = urlopen(URL)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

# on récupère pour chaque format toutes les instances de type :
# 'href="about_homme_oreille_cassee.pdf">',
# 'href="achard_amedee_-_madame_rose.epub">', ETC...
# dans l'html récupéré précedemment

i=0
resultats = []
for format_livre in FORMATS:
	resultats += re.findall(pattern='href=.*' + format_livre +'.*?>', string=html)

# on finit de formater la liste d'url de livres,
# en retirant le "href=" et en ajoutant l'url complète pour
# avoir le chemin absolu des livres

titres = []

for i in range(len(resultats))  :
	start_index = resultats[i].find("\"")
	resultats[i] = resultats[i][start_index+1:]
	end_index = resultats[i].find("\"")
	resultats[i] = resultats[i][:end_index]

	titres.append(resultats[i])
	resultats[i] = URL + resultats[i]

	print(resultats[i])

# A présent résultats contient tous les liens de téléchargement.

# On crée un dossier pour contenir les livres s'il n'existe pas
if not os.path.exists("./LIVRES") :
	os.mkdir("./LIVRES")

# on télécharge les livres dans le dossier LIVRES
for i in range(len(resultats)) :
	print(resultats[i])
	r = requests.get(resultats[i], verify=False)
	with open("./LIVRES/"+titres[i], 'wb') as f :
		f.write(r.content)


