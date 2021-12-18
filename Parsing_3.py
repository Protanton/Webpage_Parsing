import requests

import simplejson

import urllib3

from bs4 import BeautifulSoup as bs

urllib3.disable_warnings()

headers = {
    'authority': 'www.tvoyaapteka.ru',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.tvoyaapteka.ru/adresa-aptek/',
    'accept-language': 'en-US,en;q=0.9',
}

# get all cities
html = requests.get('https://www.tvoyaapteka.ru/adresa-aptek/', verify=False)
soup = bs(html.text, 'html.parser')
cities = soup.find_all("a", {"class": "col-xs-12 town_xs_item town"})

my_dict = {}
my_list = []

for city in cities:
    city_name = city.text.strip()
    city_name_str = str(city_name)
    cityid = city['data-id'] # get cities id
    headers['cookie'] = 'BITRIX_SM_S_CITY_ID={};'.format(cityid) # adding the id to the query
    response = requests.get('https://www.tvoyaapteka.ru/adresa-aptek/', headers=headers)
    soup = bs(response.text, 'html.parser')
    apteki = soup.find_all("div", {"class": "apteka_item normal_store"})
    phone = soup.find("div", {"class": "number"})
    phone_str = str(phone.text.strip())

    for apteka in apteki:
        apteka_id = apteka['data-id']
        apteka_lat = apteka['data-lat']
        apteka_lon = apteka['data-lon']
        apteka_addr = apteka.find("div", {"class": "apteka_address"})
        apteka_title = apteka.find('div', {"class": "apteka_title"})
        apteka_time = apteka.find('div', {"class": "apteka_time"})
        apteka_title_str = str(apteka_title.text.strip())
        apteka_addr_str = str(apteka_addr.text)
        apteka_time_str = str(" ".join(apteka_time.text.strip().split()))
        my_dict = {"address": city_name_str + ", " + apteka_addr_str,
                   "latlon": [apteka_lat, apteka_lon],
                   "name": apteka_title_str,
                   "phones": [phone_str],
                   "working_hours": [apteka_time_str]
                   }
        my_list.append(my_dict)

with open('./shop_list_3.json', "w", encoding="utf-8") as file:
    simplejson.dump(my_list, file, ensure_ascii=False)
