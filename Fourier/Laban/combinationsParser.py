import numpy as np

def getCombinations():
    f = open('combination.txt', 'r')
    qualities = set()
    for line in f:
        splited = line.split()
        if len(splited)==0:
            continue
        for q in splited[:-1]:
            qualities.add(q.replace(',', ''))
        #print splited[:-1]
    qualities =  list(qualities)
    qualities.sort()
    
    f = open('combination.txt', 'r')
    combinations = {'happy':{}, 'sad':{}, 'fear':{}, 'anger':{}, 'neutral':{}}
    for line in f:
        splited = line.split()
        if len(splited)==0:
            continue
        tag = splited[-1]
        tag.replace('=','')
        mood = tag[0]
        for m in combinations.keys():
            if m[0]==mood:
                mood = m
                break
        num = int(tag[1:])
        for q in splited[:-1]:
            q= q.replace(',', '')
            if not num in combinations[mood]:
                combinations[mood][num] = []
            combinations[mood][num].append(q)
    return qualities, combinations