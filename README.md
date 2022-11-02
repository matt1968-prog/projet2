@@ -0,0 +1,2 @@
# projet2

Le fichier python principal permet d'extraire (scraping) toutes les informations relatives à chacune des catégories (un fichier csv par catégorie) et de les enregistrer dans un fichier csv (un fichier par catégorie).

Pour cela, il faut ouvrir une interface en ligne de commande de type MINGGW64 (utiliser pour envoyer/push ou retirer/pull des fichiers vers/depuis le repository sur GitHub. Une autre interface de type cygwin64_bash devrait également convenir.

Le fichier requirements.txt contient les versions des différents modules utilisés dans l'environnement virtuel. Ce afin que tous les utilisateurs utilisent les mêmes versions des modules.

Pour les utiliser, il faudra créer un environnement virtuel (par exemple, python -m venv env), de l'activer : env/Scripts/activate.bat" sous Windows

d'installer les modules figurant dans le fichier requirements.txt (afin que tout le monde travaille sur les mêmes versions des modules) : pip install nom_du_module_version

Enfin, de lancer le fichier principal, scraping.py (le projet comporte un seul fichier python).

Le site est alors parsé et un dossier est créé pour chaque catégorie avec un sous-dossier data qui contient les images des différents livres de la catégorie.