# Webpage_Parsing

Site 1: https://www.mebelshara.ru/contacts
Site 2: https://www.tui.ru/offices/
Site 3: https://www.tvoyaapteka.ru

Task:
Write a Python script that will collect the address (city, street, house number, etc.), coordinates, opening hours (spread out by days) and phone numbers (general and additional, if specified) from the site in all cities.

Description: 
The script should form a file in JSON format, in which an array of objects of the form will be stored. It is advisable to use the library queries, exclude the use of selenium

JSON file data format:
````
[
  {
    "address": "Belgorod, Pugachev, 5",
    ""latlon": [44.983268, 41.096873],
    "name": "Furniture of the world,"
    "phones": [ "8 800 551 06 10"]
    "working hours": ["mon - sun 10:00 - 20:00"]
  },
  ...
]
````
