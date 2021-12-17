import json

import requests

url = 'https://apigate.tui.ru/api/office/list?cityId=1&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false'

json_text = requests.get(url)
info = json.loads(json_text.text)
offices = info['offices']

my_dict = {}
my_list = []

for office in offices:
    address = office['address']
    lat = office['latitude']
    lon = office['longitude']
    name = office['name']
    phones = office['phone']
    working_hours = office['hoursOfOperation']
    if not working_hours['saturday']['isDayOff']:
        working_saturday = 'cб {}-{}'.format(working_hours['saturday']['startStr'], working_hours['saturday']['endStr'])
    else:
        working_saturday = 'сб Выходной'
    if not working_hours['sunday']['isDayOff']:
        working_sunday = 'вс {}-{}'.format(working_hours['sunday']['startStr'], working_hours['sunday']['endStr'])
    else:
        working_sunday = 'вс Выходной'
    working_weekdays = 'пн - пт {} до {}'.format(working_hours['workdays']['startStr'], working_hours['workdays']['endStr'])
    my_dict = {"address": address,
               "latlon": [lat, lon],
               "name": name,
               "phones": [phones],
               "working_hours": [working_weekdays, working_saturday, working_sunday]
               }
    my_list.append(my_dict)

with open('./shop_list_2.json', "w", encoding="utf-8") as file:
    json.dump(my_list, file, ensure_ascii=False)
