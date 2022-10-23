import requests
from bs4 import BeautifulSoup as bs
import csv
import re
from pprint import pprint
#import lxmlpath

#Définition des variables ,listes et dictionnaires
url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
url_base_site="http://books.toscrape.com/catalogue/"
#url_travel="http://books.toscrape.com/catalogue/category/books/travel_2/index.html" #pour test
categories=[]
adresses=[]
titres=[]
quantite=[]
ratings=[]
descriptions=[]
cat_url={} #dictionnaire qui contient toutes les catégories avec leur URL
ratingBook ={"One":"1", "Two":"2", "Three":"3", "Four:":"4", "Five":"5"}


#CATÉGORIES ET ADRESSES DES CATÉGORIES
#def fetch_call_categories():

x=0
page = requests.get(url)
#print(page.content)
soup = bs(page.text, 'html.parser')
categorie=soup.find('div', class_="side_categories")
datas=categorie.find_all('li')

for data in datas: 
    if data.text.strip()!="Books ":
        #print(data.text.strip())
        categorie_livre=data.a.text.strip()
        categories.append(categorie_livre) #ajout à la liste des catégories pour vérif
        x+=1
        print("Catégorie : ",categorie_livre)
        #l=len(data.text.strip()) #nombre de caractères de la catégorie pour vérif
        adresse_URL=data.find('a')
        adresse2=adresse_URL.get('href')
        #print("adresse categorie", adresse2)
        adresse3=url_base_site+adresse2
        #print("adresse modifiée ", adresse2)
        adresse_categorie=adresse3.replace("../","")
        #print("URL de la catégorie", adresse_categorie)#.replace("../",""))
        adresses.append(adresse_categorie) #insertion dans la liste
        cat_url[categorie_livre]= adresse_categorie #insertion dans le dictionnaire
#print(cat_url.keys()) pour vérif
#print(cat_url.values()) pour verif
            
print("Nombre de catégories : ",x) 
adult=cat_url.get("New Adult") # à des fins de test -> #pour vérification de la concordance catégorie et url
print("URL de la catégorie New Adult : ", adult)
for cle, valeur in cat_url.items(): #vérification du dictionnaire
    print("Catégorie : ", cle, " URL : ", valeur)
    #print("Valeur :", valeur)
    #print(cat_url.items())"""

print(f"Total {len(datas)} <li> category tags found")
nbre_livres=len(datas)
#print(f'La liste comporte {x} catégorie(s)')
#print ("Liste des catégories : ", categories)

#TITRES DES LIVRES DE TOUTES LES CATÉGORIES
#def fetch_all_titles():

#adresse_categorie=cat_url["Crime"] #test
#print(adresse_categorie) # OK, renvoie l'adresse associée à la catégorie Crime
print(cat_url.keys())#on vériie si toutes les catégories sont bien dans le dictionnaire -> OK
print(cat_url["Horror"])

for categorie in cat_url.keys(): #test, fonctionne si on affiche uniquement la catégorie (ligne qui suit)
    #print(categorie)

    nom_categorie=categorie
    url_categorie=cat_url[categorie]
    print(url_categorie)
    print(cat_url.values) #verif
    page = requests.get(url_categorie)
    soup = bs(page.text, 'html.parser')
    
        #ICI INSERTION D'UNE BOUCLE POUR PARCOURIR TOUTE LA CATÉGORIE

#print(nom_categorie, url_categorie)
#print(soup)    
#books=soup.find('div', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
titre_livre=soup.h3.a["title"]
print(titre_livre)

#pour la page travel uniquement 
#livres_travel=page_soup.findAll('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")#{"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
#url = "url_travel #'http://books.toscrape.com/index.html"
#pour tous les livres
#tous_les_livres="http://books.toscrape.com/catalogue/category/books_1/index.html" 
#headers = "Book title, Price\n"

"""for categorie,adresse in cat_url.items():
    print("categorie : ",categorie)
    print("URL : ", adresse)
    url=adresse
    adresse_categorie=url
    print("URL catégorie :", adresse)
    reponse = requests.get(adresse_categorie)
    page_soup = bs(reponse.text, "html.parser")   

    for books in page_soup:
        titre_livre = books.h3.a["title"]
        titres.append(titre_livre) #ajout à la liste vide des titres
    # collect book price of all books
    #book_price = books.findAll("p", {"class": "price_color"})
    #price = book_price[0].text.strip()
        print("Titre du livre :" + titre_livre)
    #print("Price of the book :" + price)
#print(titres)
url1= soup2.find('article', class_="product_pod") 

url2=url1.find('a')
product_page_url=url2.get('href')
print (product_page_url)

#pour tous les livres
#tous_les_livres="http://books.toscrape.com/catalogue/category/books_1/index.html" 
#headers = "Book title, Price\n"
    
#CATÉGORIES

#TITRES des livres de la catégorie TRAVEL
    
url2 = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
page2 = requests.get(url)

soup2 = BeautifulSoup(page2.text, 'html.parser') #ou page.content
titre2=soup2.find_all('article', class_="product_pod")
    
for i in titre2:
        
        titre_livre=i.find('h3').a.get('title')
        print ("Le livre s'appelle : ", titre_livre)
        #stock= i.text
        #stock1=stock.find_all('tr')
        #stock2=(stock[5].td).text
        #print(stock2)
        #quantite_totale = re.findall(r'\d+', i)#[0]
        #titre_livre2=find('href.title)')
        #print("Livre :", i.titre_livre)
    #find_next
    #livre_i['title']=i.title
    #title=titre('h3')[0]
    #print(titre.text)"""

#EXPORT DANS FICHIERS CSV, UN FICHIER POUR CHAQUE CATÉGORIE
#def export_categories()

"""with open ('cat_adr.csv','w', encoding='utf-8') as all:
    for fichier in cat_url.keys()):
        nom_fichier=fichier+".csv"   
        #en_tete = ["Title", "product_page_url)""]
        en_tete = ["Category", "product_page_url"]
        writer = csv.writer(all, delimiter=',')
        writer.writerow(en_tete)
        #description_finale=description_finale.text
        #product_description = description_finale.replace('.', '.\n')
        #upc4=upc4.text
        #print("URL livre : ",product_page_url)
            for i, j in zip(categories, adresses):
                ligne=[i, j]
                writer.writerow(ligne)"""