import requests
from bs4 import BeautifulSoup as bs
import xlsxwriter

def get_emag_product_type(nume_produs):
    url = requests.get(f"https://www.emag.ro/{nume_produs}/c?tree_ref=2172&ref=cat_tree_91")
    return bs(url.content)

def get_product_information():
    product = {"PRODUCT NAME": None,
               "OLD PRICE": None,
               "NEW PRICE": None,
               "DISCOUNT": None,
               "REVIEWS": None,
               "LINK": None}
    name_list = []
    old_price_list = []
    new_price_list = []
    discount_list = []
    reviews_list = []
    link_list = []

    for product_code in soup.find_all("div", class_="card-item js-product-data"):
        name = product_code["data-name"]
        name_list.append(name)
        try:
            old_price = product_code.find("p", class_="product-old-price").s.text
            old_price_list.append(old_price)
        except AttributeError:
            old_price_list.append("No discount for this product")
        new_price = product_code.find("p", class_="product-new-price").text
        new_price_list.append(new_price)
        try:
            discount = product_code.find("span", class_="product-this-deal").text
            discount_list.append(discount)
        except AttributeError:
            discount_list.append("No discount for this product")
        link = product_code.find("a", class_="product-title js-product-url")["href"]
        link_list.append(link)

        product["PRODUCT NAME"] = name_list
        product["OLD PRICE"] = old_price_list
        product["NEW PRICE"] = new_price_list
        product["DISCOUNT"] = discount_list
        product["REVIEWS"] = reviews_list
        product["LINK"] = link_list

    workbook = xlsxwriter.Workbook("produse.xlsx")
    worksheet = workbook.add_worksheet()
    col_num = 0
    for key, value in product.items():
        worksheet.write(0,col_num,key)
        worksheet.write_column(1,col_num,value)
        col_num += 1

    workbook.close()











soup = get_emag_product_type("telefoane-mobile")
get_product_information()
















# driver = webdriver.Chrome(executable_path="C:/Users/Gh0sT/Desktop/chromedriver_win32")
# url = "https://www.emag.ro/"
# driver.get(url)
#
# def get_url(search_term):
#     template = "https://www.emag.ro/{}/c?tree_ref=2172&ref=cat_tree_91"
#     search_term = search_term.replace(" ", "+")
#     return template.format(search_term)
#
# url = get_url("laptopuri")
# print(url)



# workbook = Workbook()
# sheet = workbook.active
#
# sheet["A1"] = "hasdasd"
# sheet["B1"] = "world!"
#
# workbook.save(filename="hello_world.xlsx")

