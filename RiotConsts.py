

URL = {
    'base': 'https://{proxy}.api.pvp.net/api/lol/{region}/{url}',
    'static' : 'https://global.api.pvp.net/api/lol/static-data/{region}/{url}',
    'summoner_byName': 'v{version}/summoner/by-name/{names}',
    'league_challenger' : 'v{version}/league/challenger?type=RANKED_SOLO_5x5',
    'league_master' : 'v{version}/league/master?type=RANKED_SOLO_5x5',
    'matchlist' : 'v{version}/matchlist/by-summoner/{summonerId}?rankedQueues=RANKED_SOLO_5x5',
    'match' : 'v{version}/match/{matchId}',
    'matchhistory' : 'v{version}/matchhistory/{summonerId}?rankedQueues=RANKED_SOLO_5x5',
    'champLookup' : 'v{version}/champion&api_key=9a02ca0f-a750-4f7a-91a1-7e2c19e42430'
}

API_VERSIONS = {
    'summoner': '1.4',
    'league' : '2.5',
    'match' : '2.2',
    'static-data' : '1.2'
}

REGIONS = {
    'europe west': 'euw',
    'north america': 'na',
    'korea': 'kr',
    'global': 'global'
}

PLAYERDict = {
    'playerOrTeamId': 'playerID',
    'playerOrTeamName': 'Name',
    'division': 'Division',
    'leaguePoints': 'LP',
    'losses': 'numLosses',
    'wins': 'numWins'
}

MatchRoot = [
    'matchId'
]
MatchParts = [
    'spell1Id',
    'spell2Id',
    'championId',
    'teamId',
    'masteries',
    'runes'
]
MatchStats = [
    'winner',
    'champLevel',
    'item0',
    'item1',
    'item2',
    'item3',
    'item4',
    'item5',
    'item6',
    'kills',
    'deaths',
    'assists'
]
Items = [
    'item0',
    'item1',
    'item2',
    'item3',
    'item4',
    'item5',
    'item6'
]

        
        
