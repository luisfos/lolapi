import cStringIO
import requests
import json

url = 'https://www.google.co.uk/logos/doodles/2015/rugby-world-cup-2015-opening-day-6330768880041984-hp.gif'
r = requests.get(url)

img = Image.open(StringIO(r.content))

class itembuilds():
    def __init__(self, build):
        self.item0 = build[0]
        self.item1 = build[1]
        self.item2 = build[2]
        self.item3 = build[3]
        self.item4 = build[4]
        self.item5 = build[5]
        
        
