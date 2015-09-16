from time import time, sleep
from threading import Lock

class tokenBucket:
    def __init__(self):
        self.max = 8
        self.min = 1
        self.rate = 1.20
        self.tokens = self.max
        self.lasttime = time()
        self.currenttime = time()
        
    def removeToken(self):
        self.tokens += -1

    def addTokens(self):
        diff = self.currenttime - self.lasttime
        
            
        print 'time diff: ' +str(diff)
        if diff >= self.rate:
            self.tokens += int(diff / self.rate)
            print 'new tokens: ' +str(int(diff / self.rate))
            self.lasttime = time()
        
    def update(self):
        print 'tokens before :' +str(self.tokens)
        self.currenttime = time()
        self.addTokens()
        self.removeToken()
        if self.tokens <= self.min:
            sleep(self.rate)
        if self.tokens > self.max:
            self.tokens = self.max
        print 'tokens after :' +str(self.tokens)
        
            
rateLimit = tokenBucket()
interval = 86400000 * 1
def now(): return int(round(time()*1000))
def then(): return int(round(now()-interval))

def ting():

    for i in range(1, 100):
        print '=========    iter: '+str(i)
        dank.mainthing()
        



