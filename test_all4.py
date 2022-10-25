import requests
from bs4 import BeautifulSoup as bs
import csv
import re
from pprint import pprint

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
        x+=1
        print("Catégorie : ",categorie_livre)
        adresse_URL=data.find('a')
        adresse2=adresse_URL.get('href')
        adresse3=url_base_site+adresse2
        adresse_categorie=adresse3.replace("../","")
        print("URL : ", adresse_categorie)#.replace("../",""))
        #insertion dans la liste
        adresses.append(adresse_categorie) 
        #insertion dans le dictionnaire
        categories.append({'name':categorie_livre, 'url': adresse_categorie, 'books':[]}) 
    return categories    

#TITRES DES LIVRES DE TOUTES LES CATÉGORIES, CATÉGORIE PAR CATÉGORIE

def fetch_all_books(url_categorie): #ds cette fct, recherche de balise <Next>
    books=[]
    response = requests.get(url_categorie)
    soup = bs(response.text, 'html.parser')

    #EXCTRACTION DES LIVRES DE TOUTES LES CATÉGORIES
    url_des_livres=soup.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    
    for lien_livre in url_des_livres:
        url_livre=lien_livre.article.h3.a.get('href')
        url_livre=url_livre.replace('../../../', "http://books.toscrape.com/catalogue/")
        books.append(url_livre)
        print("URL : ",url_livre)#lien_livre.article.h3.a.get('href'))
    #RECHERCHER SI PAGE SUP
    next=soup.find('li', class_="next")
    if next!=None:
        #adresse page suivante
        print("IL Y A UNE AUTRE PAGE")
        next_page=next.find('a')
        next_page2=next_page.get('href')
        print(next_page2)
        page_sup=url_categorie+next_page2
        print(page_sup)
        books+=fetch_all_books (page_sup) #+= pour concaténer
    else: print("PAS AUTRE PAGE")

    return books

#EXTRACTION TOUTES LES INFOS D'UN SEUL LIVRE
def fetch_book_infos(book_url):
    #print("="*10)
    response=requests.get(book_url) 
    soupBooks= bs(response.text,'html.parser') #bs = alias de BeautifulSoup
    book={}
    
    #BOOK TITLE

    book['url']=book_url
    book['title']= soupBooks.find('h1').text 
    print ("Titre : ", book['title'])
    
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
    #print("Prix final",prix_final)
    book['price']=prix_final

    #PRICE EXCLUDING TAXES

    #price_ex_taxes=soupBooks
    prix=soupBooks.find('table', class_="table table-striped")
    prix1=prix.find_all('tr')
    valeur_brute=(prix1[2].td).text
    #print(valeur_brute)
    valeur_brute=valeur_brute[1:]
    valeur = re.findall(r'\d+\.\d+', valeur_brute)[0]
    print("Prix sans taxes : ", valeur)
    book['price EXCLUDING taxes']=valeur

    #PRICE INCLUDING TAXES

    #prix=soupBooks.find('table', class_="table table-striped")
    #prix1=prix.find_all('tr')
    valeur_brute=(prix1[3].td).text # A modifier
    #print(valeur_brute)
    valeur_brute=valeur_brute[1:]
    valeur = re.findall(r'\d+\.\d+', valeur_brute)[0]
    print("Prix avec taxes : ", valeur)
    book['price INCLUDING taxes']=valeur

    #EXEMPLAIRES DISPOS
    
    stock= soupBooks.find('table', class_="table table-striped") 
    stock1=stock.find_all('tr')
    stock2=(stock1[5].td).text
    #print(stock2)
    quantite = re.findall(r'\d+', stock2)[0]
    print("Stock : ",quantite)
    book['stock']=quantite

    #REVIEW RATING

    popularité=soupBooks.find('div', class_="col-sm-6 product_main")
    popularite2=soupBooks.find('p', class_="star-rating")
    popularite3=popularite2.get('class')
    popularite4=popularite3[1]
    nbre_etoiles=RATING_BOOK.get(popularite4)
    print("Rating : ",nbre_etoiles)
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

    #url= soupBooks.find('article', class_="product_pod") version d'origine, fonctionne avec tout sauf Attic
    url=soupBooks.find('div', class_="item active")
    url2=url.find('img')
    url3=(url2.get('src'))
    file_name=book['title']+".jpg"
    file_name=file_name.replace(":", " ") #On supprime les ":" pour avoir un nom de fichier valide
    print("Nom du fichier : ",file_name)
    file_path=book['url']
    open(file_name,'w')
    print("URL image : ", url3)
    book['URL de image']=url3

    return book

#EXPORT DANS FICHIERS CSV, UN FICHIER POUR CHAQUE CATÉGORIE
def write_csv_categories():
    en_tete = ["title", "product_page_url", "review rating", "category", "product_description", "universal_product_code", "price_excluding_taxes", "price_including_taxes"]
    
    for fichier in categories:
        #créer un fichier pour chaque catégorie
        nom_fichier=fichier+".csv"  
        print(nom_fichier) 
        #with open (nom_fichier,'w', encoding='utf-8') as all:
        #    writer = csv.writer(all, delimiter=',')
        #    writer.writerow(en_tete)
        

def write_csv_all(categories):
    en_tete = ["title", "product_page_url","category", "product_description", "number_available","universal_product_code", "image_url", "price_excluding_taxes", "price_including_taxes"]
    
    for category in categories:
        pass
           
def main():
    x=0
    categories = fetch_all_categories()
    print("Catégories trouvées : ",categories) #'name: nom catégorie 'url': url catégorie
    for categorie in categories:
        livres=fetch_all_books(categorie['url'])
        for book_url in livres:
            book_infos=fetch_book_infos(book_url)
            categorie['books'].append(book_infos)
            x+=1
        print ("Livres : ",livres)    #contient les titres et leur URL uniquement
        #write_csv=write_csv_categories(categories)
        break
    """for cat in categories:
        nom_categorie=str(cat)+".csv"  
        print("Catégorie : ",nom_categorie) 
        #print("Categories : ",categories)
        #print("Category : ",categorie) """
    print("Nombre total de livres : ", x)
#write_csv(categories)


if __name__ == "__main__":
    main()
    