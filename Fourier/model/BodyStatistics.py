upper = open('../../model/deleva_upper.txt', 'r')
headers = upper.readline().split()
CMindex = headers.index('cmM') 
segment = 'hand'
ratio = None
for line in upper:
    splited = line.split()
    if(len(splited) == 0):
        continue
    if(splited[0] == segment):
        ratio = float(splited[CMindex])/100.0

def getPointByRatio(father, sun, ratio):
    return father + (sun - father)*ratio

print getPointByRatio(5, 8, ratio)