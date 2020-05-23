# hagkaup has 160 pages of products, 
# # https://verslun.hagkaup.is/page/2/

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import codecs
import csv
import json

# control the application here
pages = 1 # pages to scrape
URL = "https://verslun.hagkaup.is/page/"
csvFilename = "products.csv"
jsonFilename = "products.json"

# Scraping a website
products = []
for page in range(pages):
    print("Scraping page " + str(page))
    my_url = URL+str(page)

    # opening connection, grabbing the page
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html.decode('utf-8'), "html.parser")

    # grabs each product
    containers = page_soup.findAll("article",{"class":"cmsmasters_product"})
    for product_nr in range(len(containers)):
        try:
            product_name = containers[product_nr].findAll("h4",{"class":"cmsmasters_product_title entry-title"})
            product_name = product_name[0].a.text
            price = containers[product_nr].findAll("span",{"class":"woocommerce-Price-amount amount"})
            price = price[0].text
            image = containers[product_nr].figure.a.img["src"]
            products.append([product_name,price,image])
        except:
            print("Error popped up in page " + page + " with product number " + product_nr)

# Save the data to a csv file
f = codecs.open(csvFilename, 'w', "utf-8")
for info in products:
    try:
        product_name = info[0]
        price = info[1]
        image = info[2]
        f.write(product_name + "," + price.replace(",","|") + "," + image.replace(",","|") + "\n")
    except:
        print("Error with converting from array")
f.close()

# Convert csv to json
csvfile = open(csvFilename, encoding="utf-8")
jsonfile = codecs.open(jsonFilename, 'w+')
fieldnames = ("product_name","price","image")
reader = csv.DictReader(csvfile, fieldnames)
jsonfile.write('[\n')
for row in reader:
    json.dump(row, jsonfile) # TODO: make the coding in json a readable language to users
    jsonfile.write(',\n')
    # TODO, find better way to avoid writing "," as last character in the json
jsonfile.write('{"product_name": "Coca Cola 330ml", "price": "129kr.", "image": "https://verslun.hagkaup.is/wp-content/uploads/2020/03/1263-540x540.jpg"}\n]')