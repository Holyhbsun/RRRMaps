import basestuff;
from basestuff import *;
#from sets import Set

infinity = 2;  # regret-ratio is always less than 1. Thus this is infinity of that :D
M = None;  # discretized matrix
F = None;  # discretized functions
Mvals = None;


def Scalardiscretize(fs, m):
    F = [];
    portion = 1.0/fs;
    v = [1 for i in range(m)];
    while True:
        f = [v[i]*portion for i in len(v)];
        F.append(f);
        i = 0;
        while v[i] == fs:
            v[i] = 1;
            i += 1;
            if i == m - 1: break;
        if i == m - 1:
            break;
        v[i] += 1;
    return F;


def Polardiscretize(fs, m):
    theta = math.pi / (2 * (fs - 1));
    v = [0 for i in range(m - 1)];
    F = [];
    while (True):
        polar = [theta * v[i] for i in range(m - 1)];
        #print polar;
        r = 1;
        f = [];
        for j in range(m - 1, 0, -1):
            f.insert(0, r * math.sin(polar[j - 1]));
            r *= math.cos(polar[j - 1]);
        f.insert(0, r);
        F.append(f);
        i = 0;
        while v[i] == fs - 1:
            v[i] = 0;
            i += 1;
            if i == m - 1: break;
        if i == m - 1:
            break;
        v[i] += 1;
    return F

def PolarRandomdiscretize(Fsize, m):
    F = [];
    for i in range(Fsize):
        polar = np.random.rand(m-1)*math.pi/2;
        #print polar;
        r = 1;
        f = [];
        for j in range(m - 1, 0, -1):
            f.insert(0, r * math.sin(polar[j - 1]));
            r *= math.cos(polar[j - 1]);
        f.insert(0, r);
        F.append(f);
    return F


'''
    x = int(fs ** (1. / (m - 1)));
    F = [];
    theta = [];
    alpha = math.pi * (m - 1) / (2 * (fs + m - 1));
    for i in range(m - 1): theta.append(1);
    for i in range(fs):
        r = 1;
        v = [];
        for j in range(m - 1, 0, -1):
            v.insert(0, r * math.cos(alpha * theta[j - 1]));
            r *= math.sin(alpha * theta[j - 1]);
        v.insert(0, r);
        F.append(v);
        j = 0;
        while j < len(theta) and theta[j] == x:
            theta[j] = 1;
            j += 1;
        if j < len(theta): theta[j] += 1;
    # print F
'''


def constructM(fs,randomDesc=False):
    global M;
    #if basestuff.dataset_sky is None:
    #    print 'initiate the dataset'
    #    return
    F = Polardiscretize(fs, basestuff.d) if randomDesc==False else PolarRandomdiscretize(fs, basestuff.d)
    #print F
    fs = len(F);
    M = np.zeros(basestuff.n * fs).reshape(basestuff.n, fs);
    cmax = np.zeros(fs);
    for t in range(basestuff.n):
        for f in range(fs):
            ft = 0;  # compute f(t)
            for j in range(basestuff.d): ft += F[f][j] * basestuff.dataset[t][j]
            M[t, f] = ft;
            if ft > cmax[f]: cmax[f] = ft;
    if basestuff.debugmod == 'on':
        print(M)
    #print M;
    for t in range(basestuff.n):  # convert the f(t) values to regret-ratio
        for f in range(fs): M[t, f] = (cmax[f] - M[t, f]) / cmax[f] if cmax[f] > 0 else 0;
    if basestuff.debugmod == 'on':
        print(M)
    return fs;


def oracle(M, epsilon):
    MPrime = np.zeros(M.shape)
    MPrime[:] = M
    MPrime = MPrime <= epsilon
    b = np.ascontiguousarray(MPrime).view(np.dtype((np.void, MPrime.dtype.itemsize * MPrime.shape[1])))
    _, uniqueRows = np.unique(b, return_index=True)

    # print uniqueRows
    # MPrimeUnique = MPrime[uniqueRows]

    items = set()
    sets = {}
    for row in uniqueRows:
        sets[row] = set(np.where(MPrime[row, :] == True)[0])
        items = items.union(sets[row])
    # print items, sets
    return greedySetCover(items, sets)


def greedySetCover(items, sets):
    selectedSets = set([])
    lentemp = []
    while (len(items) > 0):
        candidateSet = set()
        candidateSetKey = -1
        for s in sets:
            if len(sets[s]) > len(candidateSet):
                candidateSet = sets[s]
                candidateSetKey = s
        # selectedSets[candidateSetKey] = candidateSet
        selectedSets.add(candidateSetKey +1 )
        lentemp.append(len(candidateSet))
        items = items.difference(candidateSet)
        for s in list(sets.keys()):
            sets[s] = sets[s].difference(candidateSet)
            if len(sets[s]) == 0:
                del sets[s]
    return selectedSets, lentemp


def SortMvalues():
    global Mvals, M;
    Mvals = np.copy(M).reshape(-1);
    Mvals = np.sort(Mvals);
    #print Mvals


def DMM(r, fs,randomDesc=False):
    #if basestuff.convexSet is not None and len(basestuff.convexSet) <= r:
    #    return basestuff.convexSet;
    constructM(fs,randomDesc);
    SortMvalues();
    bestE = infinity;
    best = None;
    l = 0;
    h = Mvals.size;
    while (l < h):
        mid = int((l + h) / 2)
        R, tmp = oracle(M, Mvals[mid]);
        #print Mvals[mid]
        if len(R) <= r * math.log(r, 2):
            best = R;
            bestE = Mvals[mid];
            h = mid - 1;
        else:
            l = mid + 1;
    return best;
    mi = i;