import RiotAPI
#import LolClasses as LC
import json
#import requests
import RiotConsts as Consts
import pprint
#import time
#import timestamp
from pymongo import MongoClient
import pymongo
#create index on init
pp = pprint.PrettyPrinter(indent=3)
client = MongoClient()
EUdb = client.EUMeta
#players = EUdb.players
# = EUdb.matches
#players.create_index({"pID":1, "pName":1}, {unique:True})
#players.create_index([("pID", pymongo.ASCENDING),
#                    ("pName", pymongo.ASCENDING)],
#                     unique=True)

class extractInfo():
    def __init__(self, region):
        if region == 'euw':
            self.api = RiotAPI.EUapi
            self.db = EUdb
            self.players = self.db.players
            self.matches = self.db.matches
        if region == 'na':
            self.api = RiotAPI.NAapi
        if region == 'kr':
            self.api = RiotAPI.KRapi
        
    def players_AddChallenger(self):
        jsonObj = self.api.get_league_challenger()      
        for key in jsonObj['entries']:
            x = {'pID':key['playerOrTeamId'], 'pName':key['playerOrTeamName'], 'tier':'challenger'}
            self.players.replace_one(x, x, upsert=True)

    def players_AddMaster(self):
        jsonObj = self.api.get_league_master()          
        for key in jsonObj['entries']:
            x = {'pID':key['playerOrTeamId'], 'pName':key['playerOrTeamName'], 'tier':'master'}
            self.players.replace_one(x, x, upsert=True)

    def match_PlayerHistory(self, pId):
        jsonObj = RiotAPI.api.get_matchhistory(pId)
        for game in jsonObj['matches']:
            extract = self.readMatch(game)
            db.matchDict['matches'][str(pId)+'_'+str(game['matchId'])] = extract

    def match_list(self, pID):
        jsonObj = self.api.get_matchlist(pID)
        if 'matches' in jsonObj:
            for game in jsonObj['matches']:
                x = {'timestamp':game['timestamp'], 'matchID':game['matchId'], 'season':game['season']}
                self.matches.replace_one(x, x, upsert=True)

    def build_byChamp(self):
        for match in db.matchDict['matches'].values():
            champ, build = self.readBuild(match)
            champEx = False
            for cKey in db.buildDict['champion'].keys():
                if champ == cKey:
                    db.buildDict['champion'][cKey].append(build)
                    champEx = True
            if champEx == False:
                db.buildDict['champion'][champ]= [build]
            #self.buildDict['champion'].append({champ : [build]})

    def db_AddPlayerMatches(self):
        cursor = self.players.find({"tier":"challenger"})
        for player in cursor:
            self.match_list(player['pID'])
            
    def readMatch(self, game):
        result = {}
        for key, val in game.items():
            if key in Consts.MatchRoot:
                result[key] = val
        for key,val in game['participants'][0].items():
            if key in Consts.MatchParts:
                result[key] = val
        for key,val in game['participants'][0]['stats'].items():
            if key in Consts.MatchStats:
                result[key] = val
        return result

    def readBuild(self, match):
        bList = []
        champ = ''        
        for key,val in match.items():
            if key == 'championId':
                champ = val
            if key in Consts.Items:
                bList.append(val)
        return champ, bList
    
    def mostCommonBuilds(self, champId):
        results={}
        builds = db.buildDict['champion'][str(champId)]
        for focus in builds:
            focus.sort()
        for index, focus in enumerate(builds):
            EDSum = 0
            for other in builds:
                if other is not focus:
                    EDSum += LD(focus, other)
            results[index] = EDSum
        min_val = min(results.itervalues())
        print results
        #str(champId) : builds[[k for k, v in results.iteritems() if v == min_val][0]] }


def main():
    api = cAPI(key)
    #r = api.get_summoner_by_name('Luijee')
    #print r
    #x = api.get_matches(36298701)
    #print x
    




ctrl = extractInfo('euw')




