#!/bin/env python3
from base_livre import BaseLivre
from base_bibli import BaseBibli

class simple_bibli(base_bibli):
    def __init__(self, path):
        super().__init__(path) 

    def alimenter_bibliotheque(self):
        # Ajoutez des livres à la bibliothèque
        
        # Exemple de livre au format PDF
        livre_pdf = BaseLivre("Introduction à Python", "Auteur 1", "PDF", "/chemin/vers/livre_pdf.pdf")
        self.ajouter(livre_pdf)

        # Exemple de livre au format EPUB
        livre_epub = BaseLivre("Programmation en Python", "Auteur 2", "EPUB", "/chemin/vers/livre_epub.epub")
        self.ajouter(livre_epub)

"""
#test
# Créez une instance de SimpleBibli
simple_bibli = SimpleBibli("/chemin/vers/votre/repertoire")

# Alimentez la bibliothèque avec quelques livres
simple_bibli.alimenter_bibliotheque()

# Testez la méthode rapport_livres
try:
    simple_bibli.rapport_livres('PDF', 'rapport_pdf.txt')
except Exception as e:
    print(f"Erreur lors de la génération du rapport des livres : {str(e)}")

# Testez la méthode rapport_auteurs
try:
    simple_bibli.rapport_auteurs('EPUB', 'rapport_auteurs.txt')
except Exception as e:
    print(f"Erreur lors de la génération de l'état des auteurs : {str(e)}")
"""