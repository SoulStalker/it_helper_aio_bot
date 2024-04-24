import json

with open('shops_and_legals.json', 'r', encoding='utf8') as file:
    data = json.load(file)
    shops = data['shops']
    legals = data['legals']




