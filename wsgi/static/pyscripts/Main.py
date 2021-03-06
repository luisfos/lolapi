import RiotAPI
#from ..myflaskapp import client
import RiotConsts as Consts
import pprint
import Analyse
import os
#import time
#import timestamp
from pymongo import MongoClient
import pymongo
#create index on init
pp = pprint.PrettyPrinter(indent=3)


if __name__ == "__main__":
    client = MongoClient()
else:
    client = MongoClient()
    #client = pymongo.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])

EUdb = client.EUMeta
#players.create_index({"pID":1, "pName":1}, {unique:True})
#players.create_index([("pID", pymongo.ASCENDING),
#                    ("pName", pymongo.ASCENDING)],
#                     unique=True)

def resetUsed():
    EUdb.matches.update_many({'used':True}, {'$set':{'used':False}})

def dp(val, decplaces=2):
    x = pow(10, decplaces)
    y = pow(10, decplaces+1)
    whole = int(val)
    part = (round((val%1)*x))/x
    return ((whole * y) + (part * y))/y

class extractInfo():
    def __init__(self, region):
        if region == 'euw':
            self.api = RiotAPI.EUapi
            self.db = EUdb

        if region == 'na':
            self.api = RiotAPI.NAapi
            self.db = NAdb
        if region == 'kr':
            self.api = RiotAPI.KRapi
            self.db = KRdb
        self.players = self.db.players
        self.matches = self.db.matches
        self.builds = self.db.builds
        self.analysed = self.db.analysed
        
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

    def match_list(self, pID):
        jsonObj = self.api.get_matchlist(pID)
        if 'matches' in jsonObj:
            for game in jsonObj['matches']:
                fil = {'timestamp':game['timestamp'], 'matchID':game['matchId']}
                x = {'timestamp':game['timestamp'], 'matchID':game['matchId'],'used':False, 'season':game['season']}
                #self.matches.replace_one(x, x, upsert=True)
                self.matches.update_one(fil,{'$set': x},upsert=True)

    def db_AddPlayerMatches(self):
        cursor = self.players.find({"tier":"challenger"})
        for player in cursor:
            self.match_list(player['pID'])

    def db_AddBuilds(self):
        cursor = self.matches.find({'used':False})
        for match in cursor:
            #do stuff
            self.build_from_match(match['matchID'])
            #update
            self.matches.update_one(match, {'$set': {'used':True}})

    def build_from_match(self, matchID):
        jsonObj = self.api.get_match_detail(matchID)
        x = self.readMatch(jsonObj)
        y = self.processMatch(x)
        pp.pprint(y)
        for champ in y:
            self.builds.update_one(
                {'championID' : champ['championID']},
                {'$addToSet':
                     {"sets":
                        {'build':champ['build'],
                         'score' :champ['score'],
                         'matchID':champ['matchID']}}},
                upsert=True
            )
        
        #{'championID': x['championId']
        #'build' : [x['item0'],x['item1'],x['item2'],x['item3'],x['item4'],x['item5']]}
        # score

    def readMatch(self, game):
        result = {'T1G':0,'T1K':0,'T1Dmg':0,'T1D':0,'T2G':0,'T2K':0,'T2D':0,'T2Dmg':0}
        result['players']= []
        #match info
        for key, val in game.items():
            if key in Consts.MatchRoot:
                result[key] = val
        #player info
        #pp.pprint(game)
        for champ in game['participants']:
            champStats = {}            
            #champ['championId']
            if champ['teamId'] == 100:
                result['T1G'] += champ['stats']['goldEarned']
                result['T1K'] += champ['stats']['kills']
                result['T1D'] += champ['stats']['deaths']
                result['T1Dmg'] += champ['stats']['totalDamageDealt']
            elif champ['teamId'] == 200:
                result['T2G'] += champ['stats']['goldEarned']
                result['T2K'] += champ['stats']['kills']
                result['T2D'] += champ['stats']['deaths']
                result['T2Dmg'] += champ['stats']['totalDamageDealt']

            for key,val in champ.items():
                if key in Consts.MatchParts:
                    champStats[key] = val
            for key,val in champ['stats'].items():                
                if key in Consts.MatchStats:
                    champStats[key] = val                    
            result['players'].append(champStats)        
        return result

    def processMatch(self, RM):
        result = []
        for champ in RM['players']:
            Krat = 0.0
            Drat = 0.0
            Dmgrat = 0.0
            if champ['teamId'] == 100:
                if RM['T1K'] != 0:
                    Krat = float(champ['kills'] + champ['assists']) / RM['T1K']*100
                if RM['T1Dmg']!=0:
                    Dmgrat = float(champ['totalDamageDealt']) / RM['T1Dmg']*100
                if RM['T1D']!=0:
                    Drat = float(champ['deaths']) / RM['T1D']*100

                Grat = float(champ['goldEarned']) / RM['T1G']*100
                KDrat= Krat-Drat
                if champ['winner']==True:
                    vic = 100
                else:
                    vic = 0
            elif champ['teamId']==200:
                if RM['T2K']!=0:
                    Krat = float(champ['kills'] + champ['assists']) / RM['T2K']*100
                if RM['T2Dmg']!=0:
                    Dmgrat = float(champ['totalDamageDealt']) / RM['T2Dmg']*100
                if RM['T2D']!=0:
                    Drat = float(champ['deaths']) / RM['T2D']*100
                Grat = float(champ['goldEarned']) / RM['T2G']*100
                KDrat= Krat-Drat
                if champ['winner']==True:
                    vic = 100
                else:
                    vic = 0

            score= dp((0.35 * Grat)+(0.35 * Dmgrat)+(0.25 * KDrat)+(0.05 * vic))
            bld = [champ['item0'],champ['item1'],champ['item2'],champ['item3'],champ['item4'],champ['item5']]
            bld = [item for item in bld if item !=0]
            result.append({
                'championID':champ['championId'],
                'build': bld,
                'score':score,
                'matchID':RM['matchId'],
                #'G':Grat,
                #'K':Krat,
                #'D':Drat,
                #'Dmg':Dmgrat,
                'vic':vic
            })             
        return result

    def db_analyse_builds(self):
        cursor = ctrl.builds.find({},{'championID':1, '_id':0})
        for champ in cursor.distinct('championID'):
            print champ
            self.distance_by_champ(champ)

    def distance_by_champ(self, championID):
        cursor = self.builds.find_one({'championID':championID})
        cursorGroup = cursor['sets']
        if len(cursorGroup) > 1:
            for group in cursorGroup:
                EDSum = 0
                focus = group['build']
                focus = [item for item in focus if item !=0]
                for other in cursorGroup:
                    if other is not group:
                        EDSum += Analyse.distance(focus, other['build'])
                print str(focus) + "     score:" + str(EDSum)
                self.builds.update_one({'sets':{'$elemMatch':{'matchID':group['matchID']}}},
                                       {'$set':{'sets.$.distance':EDSum}})

    def min_distance(self, championID):
        cursor = self.builds.find_one({'championID':championID})['sets']
        


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






ctrl = extractInfo('euw')


#get players/challengers (more than 200 as ppl drop out/enter)
#db_addPlayerMatches
#	> match_list (player ID)
#db_AddBuilds
	#> build_from_match (match ID)
	#	> readMatch (match detail)
	#	> processMatch (readMatch)
	#> update match (used = True)

