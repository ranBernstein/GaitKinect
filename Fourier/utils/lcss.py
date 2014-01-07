import numpy as np

def lcs(base, patch, isEqual):
    lengths = [[0 for j in range(len(patch)+1)] for i in range(len(base)+1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(base):
        for j, y in enumerate(patch):
            if isEqual(x, y):
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = \
                    max(lengths[i+1][j], lengths[i][j+1])
    # read the substring out from the matrix
    result = []
    x, y = len(base), len(patch)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            #assert base[x-1] == patch[y-1]
            base[x-1] = (base[x-1]+patch[y-1])/2
            x -= 1
            y -= 1
    return base
#print lcs([1,2,3.05,4], [3,4.1,5], 0.1)