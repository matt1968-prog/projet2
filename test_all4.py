import requests
from bs4 import BeautifulSoup as bs
import csv
import re
import os
import os.path

#Définition des variables,listes et dictionnaires
url = "http://books.toscrape.com/index.html" #"http://books.toscrape.com/catalogue/category/books_1/index.html"
url_base_site="http://books.toscrape.com/"#catalogue/"
#conversion des ratings en décimaux
RATING_BOOK ={"One":"1", "Two":"2", "Three":"3", "Four:":"4", "Five":"5"} 

#CATÉGORIES ET ADRESSE DES CATÉGORIES

def fetch_all_categories():
    x=0
    adresses=[]
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    categorie=soup.find('div', class_="side_categories").ul.li.ul
    datas=categorie.find_all('li')
    categories=[] 

    for data in datas: 
        categorie_livre=data.a.text.strip()
        
        if categorie_livre!="Add a comment":
            if not os.path.exists(categorie_livre):
                os.mkdir(categorie_livre)
                data_folder=categorie_livre+"/data"
                #print data
                os.mkdir(data_folder)
                print("Catégorie créée :",categorie_livre)
            adresse_URL=data.find('a')
            adresse2=adresse_URL.get('href')
            adresse3=url_base_site+adresse2
            adresse_categorie=adresse3.replace("../","")
            print("URL : ", adresse_categorie)#.replace("../",""))
            #insertion dans la liste
            #adresses.append(adresse_categorie) 
            #insertion dans le dictionnaire
            categories.append({'name':categorie_livre, 'url': adresse_categorie, 'books':[]}) 
    return categories    

#TITRES DES LIVRES DE TOUTES LES CATÉGORIES, CATÉGORIE PAR CATÉGORIE

def fetch_all_books(url_categorie): #ds cette fct, recherche de balise <Next>
    books=[]
    response = requests.get(url_categorie)
    soup = bs(response.text, 'html.parser')
    print("livres de la catégorie : ",books)
    #EXCTRACTION DES LIVRES DE TOUTES LES CATÉGORIES
    url_des_livres=soup.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    
    for lien_livre in url_des_livres:
        url_livre=lien_livre.article.h3.a.get('href')
        url_livre=url_livre.replace('../../../', "http://books.toscrape.com/catalogue/")
        books.append(url_livre)
        #print("URL : ",url_livre)#lien_livre.article.h3.a.get('href'))
    #RECHERCHER SI PAGE SUP
    next=soup.find('li', class_="next")
    if next!=None:
        #adresse page suivante
        print("IL Y A UNE AUTRE PAGE")
        next_page=next.find('a')
        next_page2=next_page.get('href')
        print(next_page2)
        #page_sup=url_categorie+next_page2
        base_url=url_categorie[:url_categorie.rfind('/')]
        page_sup=f'{base_url}/{next_page2}'
        print(page_sup)
        books+=fetch_all_books (page_sup) #+= pour concaténer, récursion
    else: print("PAS AUTRE PAGE")
    print("livres : ", books)
    return books

#EXTRACTION TOUTES LES INFOS D'UN SEUL LIVRE
def fetch_book_infos(book_url, categorie_name):
    response=requests.get(book_url) 
    soupBooks= bs(response.text,'html.parser') #bs = alias de BeautifulSoup
    book={}
    
    #BOOK TITLE

    book['url']=book_url
    book['title']= soupBooks.find('h1').text 
    #print ("Titre : ", book['title'])
    
    #DESCRIPION

    desc1=soupBooks.find('div', class_="content")
    if desc1.find('p', class_="")==None: #recherche d'absence de commentaire (Alice in Wonderland)
        desc=""
    else: desc=desc1.find('p', class_="").text
    #print(desc)
    book['description']=desc        
    
    # PRIX

    prix=soupBooks.find('article', class_="product_page")
    prix1=prix.find('div', class_="col-sm-6 product_main")
    prix2=prix1.find('p')
    prix3=prix2.text[1:] #pour retirer le caractère 'Â' au début
    prix_final=prix3[1:] #on peut conserver le symbole de la devise
    book['price']=prix_final

    #PRICE EXCLUDING TAXES

    #price_ex_taxes=soupBooks
    prix=soupBooks.find('table', class_="table table-striped")
    prix1=prix.find_all('tr')
    valeur_brute=(prix1[2].td).text
    #print(valeur_brute)
    valeur_brute=valeur_brute[1:]
    valeur = re.findall(r'\d+\.\d+', valeur_brute)[0]
    #print("Prix sans taxes : ", valeur)
    book['price EXCLUDING taxes']=valeur

    #PRICE INCLUDING TAXES

    valeur_brute=(prix1[3].td).text # A modifier
    #print(valeur_brute)
    valeur_brute=valeur_brute[1:]
    valeur = re.findall(r'\d+\.\d+', valeur_brute)[0]
    #print("Prix avec taxes : ", valeur)
    book['price INCLUDING taxes']=valeur

    #EXEMPLAIRES DISPOS
    
    stock= soupBooks.find('table', class_="table table-striped") 
    stock1=stock.find_all('tr')
    stock2=(stock1[5].td).text
    #print(stock2)
    quantite = re.findall(r'\d+', stock2)[0]
    #print("Stock : ",quantite)
    book['stock']=quantite

    #REVIEW RATING

    popularité=soupBooks.find('div', class_="col-sm-6 product_main")
    popularite2=soupBooks.find('p', class_="star-rating")
    popularite3=popularite2.get('class')
    popularite4=popularite3[1]
    nbre_etoiles=RATING_BOOK.get(popularite4)
    #print("Rating : ",nbre_etoiles)
    book['review rating']=nbre_etoiles
    
    #UPC

    upc=soupBooks.find('div', class_="content")
    upc0=upc.find('div', id="content_inner")
    upc1=upc0.find('table', class_="table table-striped")
    upc2=upc1.find('tbody')
    upc3=upc1.find('tr')
    upc4=upc3.find('td')
    book['UPC']=upc4.text

    #IMAGE URL + IMPORTATION FICHIER IMAGE

    url=soupBooks.find('div', class_="item active")
    url=url.find('img').get('src')    
    file_path=url.replace('../../', url_base_site)
    print("URL image : ",file_path)

    r = requests.get(file_path, stream=True)
    if r.status_code == 200:
        image_path=file_path[file_path.rfind('/'):]
        image_path=f'{categorie_name}/data{image_path}'
        with open(image_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    return book

#EXPORT DANS FICHIERS CSV, UN FICHIER POUR CHAQUE CATÉGORIE
def write_csv_categories(categories):
    en_tete = ["title", "product_page_url", "review rating", "category", "product_description", "universal_product_code", "price_excluding_taxes", "price_including_taxes"]
    
    for categorie in categories:
        #créer un dossier pour chaque catégorie
        fichier_csv=categorie['name']+"/"+categorie['name']+".csv"
        with open (fichier_csv,'a', encoding='utf-8', newline='') as all:
            writer = csv.writer(all, delimiter=',')
            writer.writerow(en_tete)
            print("Fichier écrit : ",fichier_csv)
            for book in categorie['books']:
                writer.writerow([book['title'], book['url'], book['review rating'], categorie['name'], book['description'], book['UPC'], book['price EXCLUDING taxes'], book['price INCLUDING taxes'] ])

def main():
    x=0
    categories = fetch_all_categories()
    #print("Catégories trouvées : ",categories) #'name: nom catégorie 'url': url catégorie
    for categorie in categories:
        livres=fetch_all_books(categorie['url'])
        for book_url in livres:
            book_infos=fetch_book_infos(book_url, categorie['name'])
            categorie['books'].append(book_infos)
            #print("Categorie :", categorie)
            x+=1
            break
        return
        #print ("Livres : ",livres)    #contient les titres et leur URL uniquement
    write_csv=write_csv_categories(categories)
    print("Nombre total de livres : ", x)
#write_csv(categories)


if __name__ == "__main__":
    main()
    