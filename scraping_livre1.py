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
#print(i.title) #ou books.string  ou str(books)
#titles.append(livre_i)

#EXEMPLAIRES EN STOCK DU LIVRE
stock= soup.find('table', class_="table table-striped") 
stock1=stock.find_all('tr')
stock2=(stock1[5].td).text
number_available = re.findall(r'\d+', stock2)[0]

print("Exemplaire(s) disponible(s) :", number_available)

#URL LIVRE1
url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser') #ou page.content

url= soup.find('article', class_="product_pod") 

url2=url.find('a')
product_page_url=url2.get('href')
print (product_page_url)
print("URL du livre : ",product_page_url)

#PRIX SANS TAXES LIVRE1
url ="http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser') #ou page.content

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
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
#print(page.content)

soup = BeautifulSoup(page.text, 'html.parser') #ou page.content
#titre=soup.find('a')
#print(titre.text) #.text retire le nom de la balise dans l'affichage

#items=soup.findAll(class_="product_pod")
#item=items[4]
#print(item.title)

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

##URL IMAGE LIVRE1 
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser') #ou page.content
url_image= soup.find('article', class_="product_page") 
#print url_image
#livre_i['title']=i.title
url2=url_image.find('img')
image_url=url2.get('src')
print("URL image : ",url2.get('src'))

#EXPORT dans fichier CSV
with open ('livre1.csv','w', encoding='utf-8') as livre1:
    en_tete = ["title", "number_available","product_description", "price_excluding_taxes", "price_including_taxes", "product_page_url", "universal_product_code", "image_url"]
    writer = csv.writer(livre1, delimiter=',')
    writer.writerow(en_tete)
    description_finale=description_finale.text
    product_description = description_finale.replace('.', '.\n')
    upc4=upc4.text
    #print("URL livre : ",product_page_url)
    ligne=[title, number_available, product_description, price_excluding_taxes, price_including_taxes, product_page_url, universal_product_code, image_url]
    writer.writerow(ligne)
    #livre1.write('Titre, Quantite, Description\n')
    
    
    #livre1.write('titre.text, quantite,description')
    