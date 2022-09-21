import requests
from bs4 import BeautifulSoup as bs
import csv
import re
from pprint import pprint
#import lxmlpath

#Définition des variables ,listes et dictionnaires
url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
url_base_site="http://books.toscrape.com/catalogue/"
url_travel="http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
categories=[]
adresses=[]
titres=[]
quantite=[]
ratings=[]
deescriptions=[]
cat_url={} #dictionnaire qui contient toutes les catégories avec leur adresse url
ratingBook ={"One":"1", "Two":"2", "Three":"3", "Four:":"4", "Five":"5"}

page = requests.get(url)
#print(page.content)

soup = bs(page.text, 'html.parser') #ou page.content
#titre=soup.find('a')
#print(titre.text) #.text retire le nom de la balise dans l'affichage

url_travel="http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
x=0


categorie=soup.find('div', class_="side_categories")
datas=categorie.find_all('li')

#CATÉGORIES ET ADRESSES DES CATÉGORIES
for data in datas: 
        #if data.text in !="Books"+"\s" :
        categorie=data.a.text.strip()
        if categorie!="Books":
            categories.append(categorie)
            x+=1
            print("Catégorie : ",categorie)
            #l=len(data.text.strip()) #nombre de caractères de la catégorie
            adresse_URL=data.find('a')
            adresse2=adresse_URL.get('href')
            #print("adresse categorie", adresse2)
            adresse3=url_base_site+adresse2
            #print("adresse modifiée ", adresse2)
            adresse_categorie=adresse3
            print("URL de la catégorie", adresse_categorie.replace("../",""))
            adresses.append(adresse_categorie.replace("../",""))
            cat_url.update({categorie: adresse_categorie.replace("../","")}) #insertion dans bibliothèque
            #on cherche la quantité dispo sur la page du le chaque livre

#print("Dictionnaire des catégories et URL : ", cat_url)

"""print(f"Total {len(datas)} <li> category tags found")
nbre_livres=len(datas)
print(f'La liste comporte {x} catégorie(s)')
#print ("Liste des catégories : ", categories)
adult=cat_url.get("New Adult") # à des fins de test
print("URL de la catégorie New Adult : ", adult)"""

#DESCRIPTION
"""url = url_travel"
page = requests.get(url)
#print(page.content)

#print(page.headers)
#print (page.text)

soup = BeautifulSoup(page.text, 'html.parser') #ou page.content
#titre=soup.find('a')
#print(titre.text) #.text retire le nom de la balise dans l'affichage

#items=soup.findAll(class_="product_pod")
#item=items[4]
#print(item.title)

descriptionstitles=[]
description = soup.find('div', class_="content") 

x=0

#for i in description:
    #livre_i={}
    #livre_i['title']=i.title
#description1=description.find('article', class_="product_page")

description_finale=description.find('p', class_="")
print(description_finale.text)"""

#TITRES
url = url_travel #'http://books.toscrape.com/index.html'
 
reponse = requests.get(url)

page_soup = bs(reponse.text, "html.parser")

#pour la page travel uniquement 
livres_travel=page_soup.findAll('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")#{"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
#pour tous les livres
#tous_les_livres="http://books.toscrape.com/catalogue/category/books_1/index.html" 
#headers = "Book title, Price\n"
 
for books in livres_travel:
 
    # collect title of all books
    titre_livre = books.h3.a["title"]
    titres.append(titre_livre) #ajout à la liste vide des titres
    # collect book price of all books
    #book_price = books.findAll("p", {"class": "price_color"})
    #price = book_price[0].text.strip()
 
    print("Titre du livre :" + titre_livre)
    #print("Price of the book :" + price)
#print(titres)
#url=url_travel
"""reponse=requests.get(url_travel)
soup_livres=bs(reponse.text, 'html.parser')
titre=soup_livres.find_all('p', class_="product_pod")
print(titre, "" "Les titres sont :")
for book in titre:
    print(book.get_text) #titre1=i.a
    #print("titre 1 :", titre1)
    #titre2=titre1.hrefref
    #print (titre2)
    #print ("Titre :",titre3)
#for i in titre:
 #   titre=i.find

url1= soup2.find('article', class_="product_pod") 

url2=url1.find('a')
product_page_url=url2.get('href')
print (product_page_url)"""

#RATINGS
"""url = url_travel #'http://books.toscrape.com/index.html'
reponse = requests.get(url)

page_soup = bs(reponse.text, "html.parser")

#pour la page travel uniquement 
livres_travel=page_soup.findAll('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")#{"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})

for etoiles in livres_travel:
 
    # collect title of all books
    print(etoiles)#etoiles = livres_travel.get('p', class_="star-rating")
    print("Etoile : ", etoiles)
    #etoiles2=etoiles[1]
    #print("Etoile : ", etoile2)
    #print("Rating : ", etoiles_livre)[1]
    #books.h3.a["title"]
    #ratingBook.append(etoiles_livre) #ajout à la liste vide des titres
    # collect book price of all books
    #book_price = books.findAll("p", {"class": "price_color"})
    #price = book_price[0].text.strip()"""



#pour tous les livres
#tous_les_livres="http://books.toscrape.com/catalogue/category/books_1/index.html" 
#headers = "Book title, Price\n"
 
"""for etoiles in livres_travel:
 
    # collect rating of all books
    rating_livre = books.h3.a["title"]
    ratings.append(rating_livre) #ajout à la liste vide des évaluations"""
    

"""url_page_travel="http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
page_travel=requests.get(url_page_travel)
soup_travel = BeautifulSoup(page_travel.text, 'html.parser') #ou page.content
soup_travel=soup_travel.find_all('p', class_="star-rating")
#print (soup_travel)
for i in soup_travel:
    #i= soup_travel.find('p', class_="star-rating") 
    etoile=i.get('class)')
    print(etoile)
    #rating_book2=rating_book1.get('class')
    etoiles=etoile[2]
    #rating_book3=rating_book2[1]
    nbre_etoiles=ratingBook.get(etoiles)
    print ("Etoiles : ", nbre_etoiles)
#print(titles)

for i in titles:

    #titre_livre=titles.find('h3') #affiche titre partiel avec 3 points
    titre=i.find('h3').a.get('title')
    #url_livre0=i.find('h3').a.get('href') #pour l'URL
    print("Titre :",titre)
    url_livre=url_base_site+url_livre0.replace("../../../","")
    #titres.append(titre)
    print("URL: ", url_livre)
    #book_rating=titles('p', class_="star-rating")
    #print(book_rating)
    #titre_livre=titles('h3')[0]
    #titre_livre=(i.print(i) #print(titre.text)
    
print(titres)"""

#RATINGS
#print(url_travel)  
#soup_travel=BeautifulSoup(page_travel.text, 'html.parser')
#rating_book=soup_travel.find_all ('p', class_="star-rating")

#CATÉGORIES


"""for i in rating_book:

    #rating2=rating1.get('class')
    #print("RATING 2 : ", rating2)
    #print("Rating final",rating2)#rating2=rating2[0]#.text_content()
    rating3=rating1[1] #correspond en nbre d'etoiles exprimé en lettres
    print(rating3) #print("Nbre étoiles : ", rating3) #affiche Three
    nbre_etoiles=ratingBook.get(rating3) #on récupère la valeur associée à la clé rating4
    print("Etoiles en décimal ", nbre_etoiles)"""

#TITRES des livres de la catégorie TRAVEL
    
"""url2 = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
page2 = requests.get(url)

soup2 = BeautifulSoup(page2.text, 'html.parser') #ou page.content
titre2=soup2.find_all('article', class_="product_pod")
    
for i in titre2:
        
        titre_livre=i.find('h3').a.get('title')
        print ("Le livre s'appelle : ", titre_livre)"""
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



#EXPORT dans fichier CSV
"""with open ('cat_adr.csv','w', encoding='utf-8') as all:
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