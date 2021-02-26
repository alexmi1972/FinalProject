import requests
from bs4 import BeautifulSoup as bs
import xlsxwriter
import pandas as pd
import plotly.graph_objects as go

products_list = []

def get_emag_product_url(nume_produs,numar_pagini):
    url = requests.get(f"https://www.emag.ro/{nume_produs}/p{numar_pagini}/c")
    return bs(url.content, "lxml")

def get_product_information(html_code):
    for product_code in html_code.find_all("div", class_="card-item js-product-data"):
        product = {}
        name = product_code["data-name"]
        product["PRODUCT NAME"] = name
        try:
            old_price = product_code.find("p", class_="product-old-price").s.text
            old_price = old_price.replace(".", "")
            old_price = list(old_price)
            old_price.insert(-6, ".")
            old_price = "".join(old_price)
            product["OLD PRICE"] = old_price
        except AttributeError:
            product["OLD PRICE"] = "NO DISCOUNT"
        new_price = product_code.find("p", class_="product-new-price").text
        new_price = new_price.replace(".", "")
        new_price = list(new_price)
        new_price.insert(-6, ".")
        new_price = "".join(new_price)
        product["NEW PRICE"] = new_price
        try:
            discount = product_code.find("span", class_="product-this-deal").text
            discount = discount.replace("(", "")
            discount = discount.replace(")", "")
            product["DISCOUNT"] = discount
        except AttributeError:
            product["DISCOUNT"] = "NO DISCOUNT"
        link = product_code.find("a", class_="product-title js-product-url")["href"]
        product["LINK"] = link
        try:
            reviews = product_code.find("div", class_="star-rating-text").span.text
            product["REVIEWS"] = reviews
        except AttributeError:
            product["REVIEWS"] = "NO REVIEWS"
        products_list.append(product)
    return True


def sort_product():
    menu = int(input(
        "1. sortare ascendentă PRODUCT NAME\n2. sortare descendentă PRODUCT NAME\n3. sortare ascendentă OLD PRICE\n4. sortare descendentă OLD PRICE"
        "\n5. sortare ascendentă NEW PRICE\n6. sortare descendentă NEW PRICE\n7. sortare ascendentă DISCOUNT"
        "\n8. sortare descendentă DISCOUNT\n9. sortare descendentă LINK\n10. sortare ascendentă LINK"
        "\n11. sortare descendentă REVIEWS\n12. sortare ascendentă REVIEWS\n\nSelectati un mod de sortare>> "))
    if menu == 1:
        return products_list.sort(key=lambda k: k["PRODUCT NAME"], reverse=False)
    elif menu == 2:
        return products_list.sort(key=lambda k: k["PRODUCT NAME"], reverse=True)
    elif menu == 3:
        return products_list.sort(key=lambda k: k["OLD PRICE"], reverse=False)
    elif menu == 4:
        return products_list.sort(key=lambda k: k["OLD PRICE"], reverse=True)
    elif menu == 5:
        return products_list.sort(key=lambda k: k["NEW PRICE"], reverse=False)
    elif menu == 6:
        return products_list.sort(key=lambda k: k["NEW PRICE"], reverse=True)
    elif menu == 7:
        return products_list.sort(key=lambda k: k["DISCOUNT"], reverse=False)
    elif menu == 8:
        return products_list.sort(key=lambda k: k["DISCOUNT"], reverse=True)
    elif menu == 9:
        return products_list.sort(key=lambda k: k["LINK"], reverse=False)
    elif menu == 10:
        return products_list.sort(key=lambda k: k["LINK"], reverse=True)
    elif menu == 11:
        return products_list.sort(key=lambda k: k["REVIEWS"], reverse=False)
    elif menu == 12:
        return products_list.sort(key=lambda k: k["REVIEWS"], reverse=True)

def smallest_price_products():
    products_list.sort(key=lambda k: k["NEW PRICE"], reverse=False)
    df = pd.DataFrame(products_list[0:5])
    workbook = xlsxwriter.Workbook("cheapest_products.xlsx")
    worksheet = workbook.add_worksheet()
    choice = int(input("Cate produse care au pretul cel mai mic doriti sa fie afisate ?>> "))
    col_num = 0
    for key in products_list[0].keys():
        worksheet.write(0, col_num, key)
        col_num += 1
    row_num = 0
    for product in products_list[0:choice]:
        col_num = 0
        row_num += 1
        for key, value in product.items():
            worksheet.write(row_num, col_num, value)
            col_num += 1
    workbook.close()
    return True




def save_information_in_excel():
    workbook = xlsxwriter.Workbook("produse.xlsx")
    worksheet = workbook.add_worksheet()
    col_num = 0
    for key in products_list[0].keys():
        worksheet.write(0, col_num, key)
        col_num += 1
    row_num = 0
    for product in products_list:
        col_num = 0
        row_num += 1
        for key, value in product.items():
            worksheet.write(row_num, col_num, value)
            col_num += 1
    workbook.close()
    return True

def chart_xlsx():
    excel_file = "produse.xlsx"
    df = pd.read_excel(excel_file)
    data = [go.Scatter(x=df["OLD PRICE"], y=df["DISCOUNT"])]
    chart = go.Figure(data)
    chart.show()
    # workbook = xlsxwriter.Workbook("chart.xlsx")
    # worksheet = workbook.add_worksheet()
    # choice = input("Introduceti pe ce categorie se va efectua chart>> ")
    # chart_data = []
    # for product in products_list:
    #     for key,value in product.items():
    #         if key == choice:
    #             chart_data.append(value)
    # chart = workbook.add_chart({"type": "line"})
    # chart.add_series({"values": "=products!$B$2:$B$60", "name": choice})
    # worksheet.insert_chart("A1", chart)
    # workbook.close()


def main():

    print("!!!WEB SCRAPPING EMAG.RO!!!")
    nume_produs = input("Introduceti numele produsului>> ")
    url = get_emag_product_url(nume_produs, 1)
    numar_pagini = int("".join([code for code in url.find_all("a", class_="js-change-page hidden-xs hidden-sm")[-1]]))
    print(f"Numarul pagini produse: {numar_pagini}")
    count = 1
    while count <= numar_pagini:
        print(f"Pagina in lucru: {count}")
        url = get_emag_product_url(nume_produs, str(count))
        get_product_information(url)
        count += 1

    while True:
        choice = input("Doriti sa sortati informatiile obtinute din web scraping ? (Y/N)>>").upper()
        if choice == "Y":
            sort_product()
            break
        elif choice == "N":
            break
        else:
            print("Nu am inteles!!!")

    while True:
        choice = input("Doriti sa salvati informatiile din web scraping intr-un fisier excel ? (Y/N)>>").upper()
        if choice == "Y":
            save_information_in_excel()
            break
        elif choice == "N":
            break
        else:
            print("Nu am inteles!!!")

    while True:
        choice = input("Doriti sa se efectueze un top de cele mai ieftine produse ? (Y/N)>>").upper()
        if choice == "Y":
            smallest_price_products()
            break
        elif choice == "N":
            break
        else:
            print("Nu am inteles!!!")

    while True:
        choice = input("Doriti sa se realizeze un chart dupa rulare ? (Y/N)>>").upper()
        if choice == "Y":
            chart_xlsx()
            break
        elif choice == "N":
            break
        else:
            print("Nu am inteles!!!")



main()