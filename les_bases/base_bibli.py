from baselivre_facto import BaseLivre
import os
from reportlab.pdfgen import canvas
from ebooklib import epub


class BaseBibli:
    def __init__(self, path):
        self.path = path  
        self.livres = []  # Liste pour stocker les livres de la bibliothèque

        # Vérifier si le répertoire existe
        if not os.path.exists(self.path):
            os.mkdir(self.path)

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

            if format == 'PDF':
                c = canvas.Canvas(fichier+".pdf", bottomup=False)
                txt_size = 12
                c.setFont("Helvetica", txt_size)
                pos_y  = 60
                for livre in self.livres:
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

            elif format == 'EPUB' :

                rapport = ""
                for livre in self.livres :
                    rapport +=f"<p>Titre : {livre.titre()}</p>"
                    rapport += f"<p>Auteur : {livre.auteur()}</p>"
                    rapport += f"<p>Type : {livre.type()}</p>"
                    rapport += f"<p>Ressource : {livre.ressource}</p>"
                    rapport += "--------------"
                print(rapport)

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

                epub.write_epub(fichier+'.epub', book, {})

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
                txt_size = 12
                c.setFont("Helvetica", txt_size)
                pos_y = 60

                for auteur in rapport_auteurs:
                    c.drawString(60, pos_y, f'Auteur: {auteur}')
                    for livre in rapport_auteurs[auteur]:
                        c.drawString(300, pos_y, f'Titre: {livre.titre()}')
                        pos_y += txt_size
                        c.drawString(300, pos_y, f'Format: {livre.type()}')
                        pos_y += txt_size
                        c.drawString(300, pos_y, f'Fichier: {livre.ressource}')
                        pos_y += txt_size
                        c.drawString(300, pos_y, "----------")
                        pos_y += txt_size

                    pos_y += txt_size
                    c.drawString(60, pos_y, '='*50)
                    pos_y += txt_size*2

                c.save()
                print(f"Le rapport a été généré avec succès dans le fichier {fichier}.")

            elif format == 'EPUB' :

                rapport = ""
                for auteur in rapport_auteurs:
                    rapport += f"<h3>Auteur : {auteur}</h3>"
                    for livre in rapport_auteurs[auteur] :
                        rapport +=f"<p>Titre : {livre.titre()}</p>"
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

                epub.write_epub(fichier+'.epub', book, {})

                print(f"Le rapport a été généré avec succès dans le fichier {fichier}.")


        except Exception as e:
            raise FileNotFoundError(f"Erreur lors de la génération de l'état des auteurs : {str(e)}")

#test
# Créez une instance de base_bibli en fournissant le chemin du répertoire
bibli = BaseBibli("./Livres")

# Créez quelques livres en utilisant la classe BaseLivre (assurez-vous que cette classe est définie dans votre module)
livre1 = BaseLivre("https://math.univ-angers.fr/~jaclin/biblio/livres/delly_-_l_exilee.epub")
livre2 = BaseLivre("https://math.univ-angers.fr/~jaclin/biblio/livres/defoe_moll_flanders.pdf")
livre3 = BaseLivre('https://math.univ-angers.fr/~jaclin/biblio/livres/delly_-_esclave_ou_reine.epub')

# Ajoutez les livres à la bibliothèque
bibli.ajouter(livre1)
bibli.ajouter(livre2)
bibli.ajouter(livre3)

# Testez la méthode rapport_livres

bibli.rapport_livres('PDF', 'rapport_livres')


# Testez la méthode rapport_auteurs

bibli.rapport_auteurs('EPUB', 'rapport_auteurs')

