import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.mebelshara.ru/contacts/'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/91.0.4472.124 Safari/537.36'}

html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')

cities = soup.find_all("div", {"class": "city-item"})
shop_phone = soup.find("span", {"class": "phone__number"})

my_dict = {}
my_list = []

for city in cities:
    city_name = city.find("h4", {"class": "js-city-name"}).contents
    shop_address = [item["data-shop-address"] for item in city.find_all() if "data-shop-address" in item.attrs]
    shop_latitude = [item["data-shop-latitude"] for item in city.find_all() if "data-shop-latitude" in item.attrs]
    shop_longitude = [item["data-shop-longitude"] for item in city.find_all() if "data-shop-longitude" in item.attrs]
    shop_name = [item["data-shop-name"] for item in city.find_all() if "data-shop-name" in item.attrs]
    shop_weekends = [item["data-shop-mode2"] for item in city.find_all() if "data-shop-mode2" in item.attrs]
    shop_work = [item["data-shop-mode1"] for item in city.find_all() if "data-shop-mode1" in item.attrs]
    if city.find("div", {"class": "shop-list-item"}) in city.find("div", {"class": "shop-list"}):
        my_dict = {"address": city_name[0] + ", " + shop_address[0], "latlon": shop_latitude + shop_longitude,
                   "name": shop_name[0], "phones": shop_phone.contents, "working_hours": shop_weekends + shop_work}
    my_list.append(my_dict)

with open('./shop_list.json', "w", encoding="utf-8") as file:
    json.dump(my_list, file, ensure_ascii=False)
