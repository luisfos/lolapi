import requests
import RiotConsts as Consts
import timer as RL
#from time import time

key ='f4bcda59-abab-432d-bf37-be069ddda040'

class cAPI(object):
    def __init__(self, api_key, region='europe west'):
        self.api_key = api_key
        self.region = Consts.REGIONS[region]

    def _get(self, api_url, baseURL='base', extras={}):
        args = {'api_key': self.api_key}
        for key, value in extras.items():
           if key not in args:
               args[key] = value
        
        r = requests.get(
            Consts.URL[baseURL].format(
                proxy = self.region,
                region= self.region,
                url=api_url
                ),
            params=args
            )
        print r.url
        return r.json()

    def get_champKey(self):
        api_url = Consts.URL['champLookup'].format(
            version= Consts.API_VERSIONS['static-data']
        )
        return self._get(api_url, baseURL='static')
    
    def get_summoner_byName(self, name):
        api_url = Consts.URL['summoner_byName'].format(
            version= Consts.API_VERSIONS['summoner'],
            names= name
        )
        RL.rateLimit.update()
        return self._get(api_url)
    
    def get_league_challenger(self):
        api_url = Consts.URL['league_challenger'].format(
            version = Consts.API_VERSIONS['league']
        )
        RL.rateLimit.update()
        return self._get(api_url)
    
    def get_league_master(self):
        api_url = Consts.URL['league_master'].format(
            version = Consts.API_VERSIONS['league']
        )
        RL.rateLimit.update()
        return self._get(api_url)

    def get_match_detail(self, matchId):
        api_url = Consts.URL['match'].format(
            version = Consts.API_VERSIONS['match'],
            matchId = matchId
        )
        extra = {
                'includeTimeline': False
                }
        RL.rateLimit.update()
        return self._get(api_url)
    
    def get_matchlist(self, pId, begMS=RL.then(), endMS=RL.now()):
        api_url = Consts.URL['matchlist'].format(
            version = Consts.API_VERSIONS['match'],
            summonerId = pId
            )
        extra = {
                'beginTime' : begMS,
                'endTime' : endMS
                }
        RL.rateLimit.update()
        return self._get(api_url, extras=extra)

    # vvv  depreciated vvv
    def get_matchhistory(self, pId, begin=0, end=3):
        api_url = Consts.URL['matchhistory'].format(
            version = Consts.API_VERSIONS['match'],
            summonerId = pId
            )
        extra = {
                'beginIndex' : begin,
                'endIndex' : end
                }
        RL.rateLimit.update()
        return self._get(api_url, extras=extra)
            



EUapi = cAPI(key, 'europe west')
NAapi = cAPI(key, 'north america')
KRapi = cAPI(key, 'korea')

