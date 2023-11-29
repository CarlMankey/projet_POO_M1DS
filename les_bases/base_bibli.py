#!/bin/env python3
from base_livre import base_livre
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from ebooklib import epub

class base_bibli:
    def __init__(self, path):
        self.path = path  
        self.livres = []  # Liste pour stocker les livres de la bibliothèque

        # Vérifier si le répertoire existe
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Le répertoire {self.path} n'existe pas.")

    def ajouter(self, livre):
        """Ajoute un livre à la bibliothèque s'il n'est pas déjà présent."""
        try:
            # On vérifie si le livre passé en argument est une instance de la classe BaseLivre.
            if not isinstance(livre, BaseLivre):
                raise ValueError("Le livre doit être une instance de la classe BaseLivre.")
            
            # On vérifie si le fichier du livre existe réellement sur le système de fichiers.
            if not os.path.exists(livre.ressource):
                raise FileNotFoundError(f"Le fichier du livre {livre.titre()} n'existe pas.")
            
            # On vérifie si le livre est déjà présent dans la bibliothèque.
            if livre in self.livres:
                raise ValueError(f"Le livre {livre.titre()} est déjà dans la bibliothèque.")
       
            self.livres.append(livre)
            print(f"Le livre {livre.titre()} a été ajouté à la bibliothèque.")
            
        except Exception as e:
            raise FileNotFoundError(f"Erreur lors de l'ajout du livre : {str(e)}")
     
    def rapport_livres(self, format, fichier):
        try:
            format = format.upper()  # Convertir le format en majuscules pour la comparaison
            if format not in ['EPUB', 'PDF']:
                raise ValueError("Le format doit être 'EPUB' ou 'PDF'.")

            rapport = ""
            for livre in self.livres:
                if livre.type == format:
                    rapport += f"Titre: {livre.titre}\nAuteur: {livre.auteur}\nFormat: {livre.type}\nFichier: {livre.ressource}\n\n"

            with open(fichier, 'w') as file:
                file.write(rapport)

            print(f"Le rapport a été généré avec succès dans le fichier {fichier}.")

        except Exception as e:
            raise FileNotFoundError(f"Erreur lors de la génération du rapport : {str(e)}")

    def rapport_auteurs(self, format, fichier):
        try:
            format = format.upper()  # Convertir le format en majuscules pour la comparaison
            if format not in ['EPUB', 'PDF']:
                raise ValueError("Le format doit être 'EPUB' ou 'PDF'.")

            rapport_auteurs = {}  # Un dictionnaire pour stocker les informations sur les auteurs

            for livre in self.livres:
                if livre.type == format:
                    auteur = livre.auteur
                    if auteur not in rapport_auteurs:
                        rapport_auteurs[auteur] = []

                    livre_info = {
                        'titre': livre.titre,
                        'type': livre.type,
                        'fichier': livre.ressource
                    }

                    rapport_auteurs[auteur].append(livre_info)

            with open(fichier, 'w') as file:
                for auteur, livres in rapport_auteurs.items():
                    file.write(f"Auteur: {auteur}\n")
                    for livre in livres:
                        file.write(f"  Titre: {livre['titre']}\n")
                        file.write(f"  Type: {livre['type']}\n")
                        file.write(f"  Fichier: {livre['fichier']}\n")
                    file.write("\n")

            print(f"L'état des auteurs a été généré avec succès dans le fichier {fichier}.")

        except Exception as e:
            raise FileNotFoundError(f"Erreur lors de la génération de l'état des auteurs : {str(e)}")
"""
#test
# Créez une instance de base_bibli en fournissant le chemin du répertoire
bibli = BaseBibli("/chemin/vers/votre/repertoire")

# Créez quelques livres en utilisant la classe BaseLivre (assurez-vous que cette classe est définie dans votre module)
livre1 = BaseLivre("Titre 1", "Auteur 1", "PDF", "/chemin/vers/livre1.pdf")
livre2 = BaseLivre("Titre 2", "Auteur 2", "EPUB", "/chemin/vers/livre2.epub")

# Ajoutez les livres à la bibliothèque
bibli.ajouter(livre1)
bibli.ajouter(livre2)

# Testez la méthode rapport_livres
try:
    bibli.rapport_livres('PDF', 'rapport_pdf.txt')
except Exception as e:
    print(f"Erreur lors de la génération du rapport des livres : {str(e)}")

# Testez la méthode rapport_auteurs
try:
    bibli.rapport_auteurs('EPUB', 'rapport_auteurs.txt')
except Exception as e:
    print(f"Erreur lors de la génération de l'état des auteurs : {str(e)}")
"""