import pprint
import time
import requests
import json
pp = pprint.PrettyPrinter(indent=3)

now = int(time.time() * 1000)
day = int(now - 86400000)
#x = {"2251793135": {"matchId": 2251793135, "championId": 42, "kills": 2, "runes": [{"runeId": 5245, "rank": 9}, {"runeId": 5277, "rank": 9}, {"runeId": 5317, "rank": 9}, {"runeId": 5335, "rank": 1}, {"runeId": 5337, "rank": 2}], "deaths": 2, "item2": 2003, "item3": 1001, "item0": 3153, "item1": 3078, "item6": 3342, "masteries": [{"masteryId": 4112, "rank": 4}, {"masteryId": 4114, "rank": 1}, {"masteryId": 4122, "rank": 3}, {"masteryId": 4124, "rank": 1}, {"masteryId": 4131, "rank": 1}, {"masteryId": 4132, "rank": 1}, {"masteryId": 4134, "rank": 3}, {"masteryId": 4141, "rank": 1}, {"masteryId": 4142, "rank": 1}, {"masteryId": 4144, "rank": 1}, {"masteryId": 4152, "rank": 3}, {"masteryId": 4162, "rank": 1}, {"masteryId": 4211, "rank": 2}, {"masteryId": 4212, "rank": 2}, {"masteryId": 4221, "rank": 1}, {"masteryId": 4222, "rank": 3}, {"masteryId": 4232, "rank": 1}], "item4": 1055, "spell2Id": 7, "winner": 'true', "teamId": 200, "assists": 7, "spell1Id": 4, "item5": 1038, "champLevel": 14}}

url = 'https://euw.api.pvp.net/api/lol/euw/v2.2/match/2298045633?api_key=f4bcda59-abab-432d-bf37-be069ddda040'
#url = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/item?itemListData=gold&api_key=f4bcda59-abab-432d-bf37-be069ddda040'
x = requests.get(url)
pp.pprint(x.json())
#print x.json()

for thing in x['participants']
    thing['championId']
    thing['spell1Id']
    thing['spell2Id']
    thing['stats']['assists']
    thing['stats']['deaths']
    thing['stats']['kills']
    thing['stats']['assists']
