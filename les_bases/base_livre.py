import requests
import magic
from ebooklib import epub
import PyPDF2
import os

import urllib3
import ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # désactive l'avertissement de non-vérif
ssl._create_default_https_context = ssl._create_unverified_context  # permet de télécharger sans verif

class base_livre:
    def __init__(self, ressource):
        self.ressource = ressource
        self.contenu = None # initialisé à None 

        try:
            # Vérifier si ressource est une URL ou un fichier local
            if self.est_url(ressource):
                try:
                    self.ajouter_depuis_url()
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

    def ajouter_depuis_url(self):
        if not os.path.exists("./Livres"):  # si le dossier qui contient les livres n'existe pas on le créé
            os.mkdir("./Livres")

        book = requests.get(self.ressource, verify=False)  # Récupere le contenu de la page
        book.raise_for_status()

        i = self.ressource.rfind('/')   # on garde la fin de l'url pour créer le nom du fichier
        nom_fichier = self.ressource[i:]

        with open("./Livres/" + nom_fichier, 'wb') as f:
            f.write(book.content)

        self.ressource = "./Livres/" + nom_fichier # maintenant la ressource est locale



    def est_url(self, chaine):
        return chaine.startswith("http://") or chaine.startswith("https://")
    
    def type(self): #ne fonctionne pas correctement 
        try:
            if self.contenu is not None:   
                # Utilisation de la bibliothèque python-magic pour déterminer le type MIME du contenu
                mime_type = magic.Magic()
                mime_info = mime_type.from_buffer(self.contenu)
                print(mime_info)
            
                # Identifier le type en fonction du type MIME
                """ if detected_mime_type.endswith('epub'):  #livre ce terminant par epub
                    return "EPUB"
                elif detected_mime_type.endswith('pdf'):
                    return "PDF"
                else:
                    return "Autre" """              
                if "EPUB document" in mime_info:
                    return "EPUB"
                elif "application/pdf" in mime_info:
                    return "PDF"
                else:
                    return "Autre"
            else:

                return "Contenu vide"

        except Exception as e:
            raise NotImplementedError(f"Erreur lors de la détermination du type : {e}")


    def titre(self): #ne fonctionne pas correctement 
        try:
            if self.contenu is not None:
                if self.type() == "EPUB":
                        print(self.type())
                        # Utiliser la bibliothèque ebooklib pour extraire le titre d'un fichier EPUB
                        book = epub.read_epub(self.ressource)
                        # En supposant que le premier titre soit le titre principal
                        title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else "Titre non disponible"
                        return title
                        
                elif self.type() == "PDF":
                    print(self.type())
                    try:
                        # Utiliser la bibliothèque PyPDF2 pour extraire le titre d'un fichier PDF
                        with open(self.ressource, 'rb') as pdf_file:
                            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                            # En supposant que le titre soit dans les informations du document
                            info= pdf_reader.getDocumentInfo()
                            title = info.title if info.title else "Titre non disponible"
                            return title
                    except PyPDF2.utils.PdfReadError:
                        return "Erreur lors de l'extraction du titre du PDF"
                else:
                    return "Autre Titre"
            else:
                return "Contenu vide"
        except Exception as e:
            raise NotImplementedError(f"Erreur lors de la détermination du titre : {e}")   

    def auteur(self):
        if self.contenu is not None:
            if self.type() == "EPUB":
                try:
                    book = epub.read_epub(self.contenu)

                    #En supposant que le premier auteur soit l'auteur principal
                    author = book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else "Auteur non disponible"
                    return author
                except Exception as e:
                    print(f"Erreur lors de l'extraction de l'auteur du livre EPUB : {e}")
                    return "Auteur non doisponible"

            elif self.type() == "PDF":
                try:
                    with open(self.ressource, 'rb') as pdf_file:
                        pdf_reader = PdfReader(pdf_file)
                        info = pdf_reader.getDocumentInfo()
                        author = info.author if info.author else "Auteur non disponible"
                        return author
                except Exception as e:
                    print(f"Erreur lors de l'extraction de l'auteur du livre PDF : {e}")
                    return "Auteur non disponible"

            else:
                return "Autre Auteur"
        else:
            return "contenu vide"
    
    def langue(self):
        if self.contenu is not None:
            if self.type() == "EPUB":
                try:
                    book = epub.read_epub(self.contenu)

                    # En supposant que les informations sur la langue se trouvent dans les métadonnées
                    language = book.get_metadata('DC', 'language')[0][0] if book.get_metadata('DC', 'language') else "Langue non disponible"
                    return language
                except Exception as e:
                    print(f"Erreur lors de l'extraction de la langue du livre EPUB : {e}")
                    return "Langue non disponible"
            elif self.type() == "PDF":
                try:
                    with open(self.ressource, 'rb') as pdf_file:
                        pdf_reader = PdfReader(pdf_file)
                        # En supposant que les informations sur la langue se trouvent dans les métadonnées
                        info=pdf_reader.getDocumentInfo()
                        language = info.subject if info.subject else "Langue non disponible"
                        return language
                except Exception as e:
                    print(f"Erreur lors de l'extraction de la langue du livre PDF : {e}")
                    return "Langue non disponible"
            else:
                return "Autre Langue"
        else:
            return "Contenu vide"
    
    def sujet(self):
        if self.contenu is not None:
            if self.type() == "EPUB":
                try:
                    book = epub.read_epub(self.contenu)

                    # En supposant que les informations sur le sujet se trouvent dans les métadonnées
                    sujet = book.get_metadata('DC', 'subject')[0][0] if book.get_metadata('DC', 'subject') else "Sujet non disponible"
                    return sujet
                except Exception as e:
                    print(f"Erreur lors de l'extraction du sujet du livre EPUB : {e}")
                    return "Sujet non disponible"
            elif self.type() == "PDF":
                try:
                    with open(self.ressource, 'rb') as pdf_file:
                        pdf_reader = PdfReader(pdf_file)
                        # En supposant que les informations sur le sujet se trouvent dans les métadonnées
                        info=pdf_reader.getDocumentInfo()
                        sujet = info.subject if info.subject else "Sujet non disponible"
                        return sujet
                except Exception as e:
                    print(f"Erreur lors de l'extraction du sujet du livre PDF : {e}")
                    return "Sujet non disponible"
            else:
                return "Sujet non disponible"
        else:
            return "Contenu vide"
    
    def date(self):
        if self.contenu is not None:
            if self.type() == "EPUB":
                try:
                    book = epub.read_epub(self.contenu)
                    
                    date_published = book.get_metadata('DC', 'date')[0][0] if book.get_metadata('DC', 'date') else "Date non disponible"
                    return date_published
                except Exception as e:
                    print(f"Erreur lors de l'extraction de la date de publication du livre EPUB : {e}")
                    return "Unknown Date"

            elif self.type() == "PDF":
                try:
                    with open(self.ressource, 'rb') as pdf_file:
                        pdf_reader = PdfReader(pdf_file)
                        
                        # En supposant que les informations sur la date se trouvent dans les métadonnées
                        info= pdf_reader.getDocumentInfo()
                        date= info.created if info.created else "Date non disponible"
                        return date
                except Exception as e:
                    print(f"Erreur lors de l'extraction de la date de publication du livre PDF : {e}")
                    return "Unknown Date"
            else:
                return "Autre Date"
        else:
            return "Contenu vide"



# Test methodes avec un fichier EPUB
livre = base_livre("https://math.univ-angers.fr/~jaclin/biblio/livres/austen_jane_-_emma.epub")
print("Type:", livre.type())
print("Titre:",livre.titre())
print("Auteur:", livre.auteur())
print("Langue:", livre.langue())
print("Sujet:", livre.sujet())
print("Date:", livre.date())

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
