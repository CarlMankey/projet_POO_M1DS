#!/bin/env python3
import requests
import magic
from ebooklib import epub
from PyPDF2 import PdfReader

class base_livre:
    def __init__(self, ressource):
        self.ressource = ressource
        self.contenu = None  # initialisé à None
        
        try:
            # Vérifier si ressource est une URL ou un fichier local
            if self.est_url(ressource):
                try:
                    book = requests.get(self.ressource) #Récupere le contenu de la page 
                    book.raise_for_status()             # Gère les erreurs HTTP
                    self.contenu = book.content         #renvoie le contenu de la page, en octet
                except requests.exceptions.RequestException as e:
                    print(f"Une erreur s'est produite lors de la requête HTTP : {e}")
            else:
                # Si c'est un fichier local, lisez simplement le contenu du fichier
                try:
                    with open(self.ressource, 'rb') as fichier:
                        self.contenu = fichier.read()
                except FileNotFoundError:
                    print(f"Le fichier {self.ressource} n'a pas été trouvé.")
        except Exception as e:
            raise NotImplementedError("Erreur lors de l'initialisation du livre : {}".format(str(e)))


    def est_url(self, chaine):
        return chaine.startswith("http://") or chaine.startswith("https://")

    def type(self):
        try:
            if self.contenu is not None:
                mime_info = magic.Magic().from_buffer(self.contenu)
                return "EPUB" if "application/epub+zip" in mime_info else "PDF" if "application/pdf" in mime_info else "Autre"
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
                            info = pdf_reader.getDocumentInfo()
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
        return self.extraire_les_données('creator') 

    def langue(self):
        return self.extraire_les_données('language') 

    def sujet(self):
        return self.extraire_les_données('subject') 

    def date(self):
        return self.extraire_les_données('date')
"""
# Test methodes avec un fichier EPUB
livre = base_livre("lien")
print("Type:", livre.type())
print("Titre:",livre.titre())
print("Auteur:", livre.auteur())
print("Langue:", livre.langue())
print("Sujet:", livre.sujet())
print("Date:", livre.date())
"""
"""
# Test methodes avec un fichier PDF
livre = base_livre("lien")
print("Type:", livre.type())
print("Titre:",livre.titre())
print("Auteur:", livre.auteur())
"""

""""
#Test FICHIER OU URL
livre = base_livre("lien du fichier")
# ou
livre = base_livre("FICHIER.pdf")
livre = base_livre("Fichier.epub")

print(livre.contenu)
#*********************************
"""
