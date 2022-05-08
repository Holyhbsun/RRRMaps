import basestuff
from basestuff import *
import twoD
from twoD import *
from time import time

folder = 'data/'
filename = 'DOTDec2017'
columns = [10,11,16,13,19,20,12,14] # DelayInv_norm:10, , taxioutInv_norm:11, ACTUAL_ELAPSED_TIME_Norm: 16, arrdelayInv_norm:13, AIR_TIME_Norm: 19, Dist_Norm: 20, taxiinInv_norm:12, CRS_ELAPSED_TIME_Norm: 14

setparams(20,2,K=5);
genData(file=folder+filename+'.csv',pythonfile=False,cols=columns[0:4])
#s = twoDRRR(debug=True)
FindRanges(findksets=True)
print(twoD.ksets)
#print maxk(s)