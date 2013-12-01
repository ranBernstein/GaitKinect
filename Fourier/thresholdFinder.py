import numpy as np
def normalByPercentile(vec):
    s = vec
    s = np.sort(np.array(s));
    l = len(vec)
    mn = s[int(0.1 * l)]
    mx = s[int(0.9 * l)]
    offset = 0.5 * (mn + mx)
    r = 0.5 * (mx - mn)
    if (r == 0):
            r = 1
    vec = (vec-offset)/r   
    return vec