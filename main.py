import requests
from bs4 import BeautifulSoup as bs
import xlsxwriter
import pandas as pd

name_list = []
old_price_list = []
new_price_list = []
discount_list = []
reviews_list = []
link_list = []

product = {"PRODUCT NAME": None,
               "OLD PRICE": None,
               "NEW PRICE": None,
               "DISCOUNT": None,
               "REVIEWS": None,
               "LINK": None}

def get_emag_product_url(nume_produs,numar_pagini):
    url = requests.get(f"https://www.emag.ro/{nume_produs}/p{numar_pagini}/c")
    return bs(url.content)

def get_product_information(html_code):

    for product_code in html_code.find_all("div", class_="card-item js-product-data"):
        name = product_code["data-name"]
        name_list.append(name)
        try:
            old_price = product_code.find("p", class_="product-old-price").s.text
            old_price_list.append(old_price)
        except AttributeError:
            old_price_list.append("No discount")
        new_price = product_code.find("p", class_="product-new-price").text
        new_price_list.append(new_price)
        try:
            discount = product_code.find("span", class_="product-this-deal").text
            discount_list.append(discount)
        except AttributeError:
            discount_list.append("No discount")
        link = product_code.find("a", class_="product-title js-product-url")["href"]
        link_list.append(link)
        try:
            reviews = product_code.find("div", class_="star-rating-text").span.text
            reviews_list.append(reviews)
        except AttributeError:
            reviews_list.append("No reviews")

    return True

def sort_information(column):
    dataframe = pd.DataFrame(product)
    dataframe.sort_values(by=column, ascending=True)

def save_information_in_excel():
    workbook = xlsxwriter.Workbook("produse.xlsx")
    worksheet = workbook.add_worksheet()
    col_num = 0
    for key, value in product.items():
        worksheet.write(0, col_num, key)
        worksheet.write_column(1, col_num, value)
        col_num += 1
    workbook.close()
    return True


def main():


    print("!!!WEB SCRAPPING EMAG.RO!!!")
    nume_produs = input("Introduceti numele produsului>> ")
    numar_pagini = int(input("Introduceti numarul de pagini emag>> "))
    count = 1
    while count <= numar_pagini:
        print(count)
        url = get_emag_product_url(nume_produs, str(count))
        get_product_information(url)
        count += 1

    product["PRODUCT NAME"] = name_list
    product["OLD PRICE"] = old_price_list
    product["NEW PRICE"] = new_price_list
    product["DISCOUNT"] = discount_list
    product["REVIEWS"] = reviews_list
    product["LINK"] = link_list

    dataframe = pd.DataFrame(product)
    dataframe.sort_values(by="PRODUCT NAME", ascending=True, kind="mergesort")
    print(dataframe)



    while True:
        choice = input("Doriti sa salvati informatiile din web scraping intr-un fisier excel ? (Y/N)>>")
        if choice == "Y":
            save_information_in_excel()
            break
        elif choice == "N":
            break
        else:
            print("Nu am inteles!!!")







main()

df = pd.DataFrame(product)
df.sort_values