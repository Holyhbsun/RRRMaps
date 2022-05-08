import numpy as np
import math
from heapq import heappush, heappop, heapify
import pandas as pd
from haversine import haversine
# -----------------------------------------------------------------------------------
def mylog(st, outputfile):
    outfile = open(outputfile, 'a');
    outfile.write(st + '\n');
    outfile.close();

# -----------------------------------------------------------------------------------
n = None;  # database size
d = None;  # number of attributes (|D|)
k = None;
dataset = None;  # type: numpy:ndarray; original set of points (all tuples)
dataset1 = None;
debugmod = 'on'  # type: string; turns the debug mode on and off

def cmp(a, b):
    return (a > b) - (a < b)

def setparams(numberofTuples, numberofAttributes, K=None, debug='on'):
    global n, d, k, debugmod;
    n = numberofTuples;
    d = numberofAttributes;
    k = K if K is not None else n/3;
    debugmod = debug

'''
def genData(file=None, pythonfile=True, header=1, delim=',', cols=(1,2,3)):
    global dataset,fairportion,dataset_unique;
    print('started generating/loading the data')
    if file is None:
        dataset = np.random.rand(n, d)
        dataset = np.append(dataset,np.random.randint(low=0,high=2,size=n).reshape(n,1),axis=1)
    elif pythonfile:
        dataset = np.load(file)
    else:
        dataset = pd.read_csv(file, delimiter=delim, header=0, usecols=cols, on_bad_lines='skip');
        #dataset = np.genfromtxt(file, delimiter=delim, skip_header=header, usecols=cols);#, max_rows=n);
    #dataset = dataset[0:n, 0:d]
    dataset.fillna(0)
    dataset = np.array(dataset)
    #dataset = dataset.astype(np.float32)
'''

def genData(file=None, pythonfile=True, header=1, delim=',', cols=(1,2,3), lat=0, lng=0, dst=0):
    global dataset,fairportion,dataset_unique;
    print('started generating/loading the data')
    f = open(file,"r",encoding='utf-8')
    if file is None:
        dataset = np.random.rand(n, d)
        dataset = np.append(dataset,np.random.randint(low=0,high=2,size=n).reshape(n,1),axis=1)
    elif pythonfile:
        dataset = np.load(file)
    else:
        dataset = pd.read_csv(file, delimiter=delim, header=0, usecols=cols, on_bad_lines='skip');
        dataset1 = pd.read_csv(file, delimiter=delim, header=0, on_bad_lines='skip');        
        minlat, maxlat, minlng, maxlng = __get_area(lat, lng, dst)
        dataset = dataset.loc[(dataset['latitude'] <= maxlat) & (dataset['latitude'] >= minlat)
        & (dataset['longitude'] <= maxlng) & (dataset['longitude'] >= minlng)]
        dataset1 = dataset1.loc[(dataset1['latitude'] <= maxlat) & (dataset1['latitude'] >= minlat)
        & (dataset1['longitude'] <= maxlng) & (dataset1['longitude'] >= minlng)]
        dataset['stars'] = dataset['stars'] / 5.0
        dataset['review_count'] = dataset['review_count'].apply(np.log2)
        dataset['review_count'] = dataset['review_count'] / dataset['review_count'].max()
        dataset['dist_weight'] = dataset.apply(lambda dataset: cal_distance(dataset, lat, lng, dst), axis=1)
        dataset = dataset.drop(labels=['latitude','longitude'],axis=1)
        #print(dataset.iloc[cols])
        dataset = np.array(dataset)
        #print(dataset)

def __get_area(latitude, longitude, dis):

    r = 6371.137
    dlng = 2 * math.asin(math.sin(dis / (2 * r)) / math.cos(latitude * math.pi / 180))
    dlng = dlng * 180 / math.pi

    dlat = dis / r
    dlat = dlat * 180 / math.pi

    minlat = latitude - dlat
    maxlat = latitude + dlat
    minlng = longitude - dlng
    maxlng = longitude + dlng

    return minlat, maxlat, minlng, maxlng

def cal_distance(row, lat, lng, dst):

    long1 = row['longitude']
    lat1 = row['latitude']
    long2 = lng
    lat2 = lat
    g1 = (long1, lat1)
    g2 = (long2, lat2)

    ret = abs(dst - haversine(g1, g2)) / dst
    return ret

def score(i,f):
    c = 0;
    if len(f)!= d:
        print('Error: Function length should be equal to m')
        return
    for j in range(d):
        c+=f[j] * dataset[i,j]
    return c;

def top_k_old(theta):
    global k;
    f = polartoscalar(theta)
    return sorted([ [i,score(i, f)] for i in range(n)], cmp = lambda x,y: cmp(x[1], y[1]), reverse=True)[0:k]

def top_k(input,isweight=False):
    global k;
    f = polartoscalar(input) if not isweight else input
    heap = [[score(i, f),i] for i in range(k)]
    heapify(heap) # test to be minheap
    for i in range(k,n):
        s = score(i, f)
        if s>heap[0][0]:
            heappop(heap)
            heappush(heap, [s,i])
    return [heap[i][1] for i in range(k)]

def polartoscalar(theta, r=1):
    f = [];
    #if len(theta)==1: return [math.cos(theta[0]), math.sin(theta[0])]
    for j in range(d - 1, 0, -1):
        f.insert(0, r * math.sin(theta[j - 1]));
        r *= math.cos(theta[j - 1]);
    f.insert(0, r);
    return f;

def scolartopolar(f): # test it
    if len(f)<d:
        return 'Error: length of function is not big enough'
    theta = []
    cumulative = f[0]*f[0]
    for i in range(1,d):
        theta.append(math.atan(f[i]/math.sqrt(cumulative)))
        cumulative += f[i]*f[i]
    return (math.sqrt(cumulative),theta) # (r,theta)

def angledist(th,thp):
    x = polartoscalar(th);
    y = polartoscalar(thp);
    return sum([x[i]*y[i] for i in range(len(x))]);
























