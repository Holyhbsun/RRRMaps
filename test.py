import basestuff
from basestuff import *
import KsetEnum
from KsetEnum import *
from MDRC import MDRC
from MD import MDRRR
import MD
import HDRR
from time import time
import twoD
import pandas as pd
folder = 'data/'
#filename = 'DOTDec2017'
#columns = [10,11,16,13,19,20,12,14]
filename = 'yelp_business'
#columns = [4,5,6,7,13,14,15,16,17,18,19,20,21,22,23]

lat, lng = 39.870329036079696, -86.06291542449275
dst = 10 * 1.60934
columns = [6,7,8,9]


genData(file=folder+filename+'.csv',pythonfile=False,cols=columns, lat=lat , lng=lng, dst=dst)
dataset = basestuff.dataset
print(dataset.shape[0])

dataset1 = pd.read_csv(folder+filename+'.csv', delimiter=',', header=0, on_bad_lines='skip');
minlat, maxlat, minlng, maxlng = basestuff.__get_area(lat, lng, dst)
dataset1 = dataset1.loc[(dataset1['latitude'] <= maxlat) & (dataset1['latitude'] >= minlat)
        & (dataset1['longitude'] <= maxlng) & (dataset1['longitude'] >= minlng)]



r = 5; n=100;gamma=4;
setparams(dataset.shape[0], 3, K=5);
#setparams(100, 3, K=5);
#Kset_random()
t = time()
S1 = MDRC()
print (time()-t)
#S1 = {2050, 8, 1034, 1930, 845, 5007, 2832, 2065, 6672, 3539, 2325, 4376, 1817, 1752, 156, 5277, 4321, 740, 934, 233, 1642, 3564, 172, 6766, 1776, 114, 117, 5303, 3516}
print (S1)

dataset1 = dataset1.iloc[list(S1),1:]
dataset1 = dataset1.reset_index(drop=True)
print(dataset1)
dataset1.to_csv("data\data2.csv", index=False)
'''
t = time()
S = twoD.twoDRRR()
print (S)
print (MD.maxk_rand(S1,100))
print (twoD.maxk(S1))
print (MD.maxk_rand(S,100))
print (twoD.maxk(S))
print (time()-t)
'''
t = time()
s = MDRRR()
print (s)
s2 = HDRR.DMM(len(s),gamma)
print (s2)
print (MD.maxk_rand(set(s2),100))
print (time()-t)

#Kset_Enum()

#print len(KsetEnum.Ksets)
#print KsetEnum.Ksets