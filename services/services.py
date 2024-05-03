import json
import re


pattern = r".+_УТТ_"
replacement = ""

with open('shops_and_legals.json', 'r', encoding='utf8') as file:
    data = json.load(file)
    shops = data['shops']
    for key, value in shops.items():
        shops[key] = re.sub(pattern, replacement, value)
    legals = data['legals']




