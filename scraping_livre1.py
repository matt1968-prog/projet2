import requests
import re
from bs4 import BeautifulSoup
import csv

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
#print(page.content)

soup = BeautifulSoup(page.text, 'html.parser') #ou page.content

#TITRE DU LIVRE
titre = soup.find('div', class_="col-sm-6 product_main") 

#livre_i['title']=i.title
title=titre('h1')[0]
title=title.text
print("Titre : ",title)

#EXEMPLAIRES EN STOCK DU LIVRE
stock= soup.find('table', class_="table table-striped") 
stock1=stock.find_all('tr')
stock2=(stock1[5].td).text
number_available = re.findall(r'\d+', stock2)[0]

print("Exemplaire(s) disponible(s) :", number_available)

#URL LIVRE1
url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
page2 = requests.get(url)
soup2 = BeautifulSoup(page2.text, 'html.parser') #ou page.content
url1= soup2.find('article', class_="product_pod") 

url2=url1.find('a')
product_page_url=url2.get('href')
print (product_page_url)
print("URL du livre : ",product_page_url)

#PRIX SANS TAXES LIVRE1
prix=soup.find('table', class_="table table-striped")
prix1=prix.find_all('tr')
valeur_brute=(prix1[3].td).text
valeur_brute=valeur_brute[1:]
price_excluding_taxes = re.findall(r'\d+\.\d+', valeur_brute)[0]
print("Prix sans taxes :", price_excluding_taxes)

#PRIX AVEC TAXES LIVRE1
prix=soup.find('table', class_="table table-striped")
prix1=prix.find_all('tr')
valeur_brute=(prix1[3].td).text
valeur_brute=valeur_brute[1:]
price_including_taxes = re.findall(r'\d+\.\d+', valeur_brute)[0]
print("Prix avec taxes :", price_including_taxes)


#UPC LIVRE1upc = soup.find('div', class_="content") 
upc_list=[]
upc = soup.find('div', class_="content") 
upc0=upc.find('div', id="content_inner")
upc1=upc0.find('table', class_="table table-striped")
upc2=upc1.find('tbody')
upc3=upc1.find('tr')
upc4=upc3.find('td')
universal_product_code=upc4.text
#titre_final=titre_livre.text
#print(i)
print("UPC : ",upc4.text)

#DESCRIPTION LIVRE1
description = soup.find('div', class_="content") 
description_finale=description.find('p', class_="")
print("Description :", description_finale.text)

#RATING LIVRE1
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
#print(page.content)

ratingBook ={"One":"1", "Two":"2", "Three":"3", "Four:":"4", "Five":"5"}
#print (ratingBook)

#for i in ratingBook:
#print (ratingBook[i])

rating=soup.find('div', class_="col-sm-6 product_main")
rating2=soup.find('p', class_="star-rating")
rating3=rating2.get('class')
print("Rating final",rating3)#rating2=rating2[0]#.text_content()
rating4=rating3[1] #correspond en nbre d'etoiles exprimé en lettres
print("Nbre étoiles : ", rating4) #affiche Three
review_rating=ratingBook.get(rating4) #on récupère la valeur associée à la clé rating4
print("Etoiles en décimal ", review_rating)

##URL IMAGE LIVRE1 
url_image= soup.find('article', class_="product_page") 
#print url_image
#livre_i['title']=i.title
url2=url_image.find('img')
image_url=url2.get('src')
print("URL image : ",url2.get('src'))

#EXPORT dans fichier CSV
with open ('livre1.csv','w', encoding='utf-8') as livre1:
    en_tete = ["Titre", "Quantité disponible","Description produit", "Prix HT", "Prix TTC", "Étoiles (sur 5 max)", "URL page produit", "UPC (universal_product_code)", "URL image"]
    writer = csv.writer(livre1, delimiter=',')
    writer.writerow(en_tete)
    description_finale=description_finale.text
    product_description = description_finale.replace('.', '.\n')
    upc4=upc4.text
    #print("URL livre : ",product_page_url)
    ligne=[title, number_available, product_description, price_excluding_taxes, price_including_taxes, review_rating, product_page_url, universal_product_code, image_url]
    writer.writerow(ligne)
   
    