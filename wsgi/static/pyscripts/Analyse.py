import collections

similar={}
exceptions={}


def distance(s1, s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    neg=[]
    pos=[]
    baseTotal= 0
    simTotal = 0
    excTotal = 0
    cnt = collections.Counter()
    for c in s1:
        cnt[c] += 1
    for c in s2:
        cnt[c] -= 1
    for x,y in cnt.items():
        neg.extend([x]*(-y))
        pos.extend([x]*( y))
    #print 'pos = '+str(pos)
    #print 'neg = '+str(neg)
    for Pchar in pos[:]:
        delBool = False
        for grp, val in similar.items():
            if Pchar in set(grp):
                for Nchar in neg[:]:
                    if Nchar in set(grp):
                        delBool = True
                        simTotal += val
                        cnt[Pchar] -= 1
                        cnt[Nchar] += 1
                        neg.remove(Nchar)
                        break
        if delBool == True:
            pos.remove(Pchar)
    cnt = {x:a for x,a in cnt.items() if a!= 0}
    for char, frequency in cnt.items():
        if char in exceptions:
            diff = exceptions[char]-1
            change = diff * abs(frequency)
            excTotal += change

    magnitude = sum(abs(diff) for diff in cnt.values()) // 2
    lenDiff =  (abs(sum(cnt.values())) + 1) // 2
    baseTotal = magnitude + lenDiff
    return baseTotal + excTotal + simTotal

x = {"startIndex":{'dog':1, 'match':3},"endIndex":0,"totalGames":0}
