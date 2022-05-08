#View
from django.shortcuts import render, HttpResponse
import json
import basestuff
from basestuff import *
import KsetEnum
from KsetEnum import *
from MDRC import MDRC
from MD import MDRRR
import MD
import HDRR
from time import time
#import twoD
import pandas as pd
folder = 'data/'
filename = 'yelp_business'

def index(request):
    return render(request, "index.html")

def solve(request):
    if request.method == 'POST':
        if request.POST.get('lat', '') != '':
            lat = float(request.POST.get('lat', ''))
            lng = float(request.POST.get('lng', ''))
            dst = float(request.POST.get("dst")) * 1.60934
            columns = [6,7,8,9]
            t = time()
            dataset1 = pd.read_csv(folder+filename+'.csv', delimiter=',', header=0, on_bad_lines='skip');
            minlat, maxlat, minlng, maxlng = basestuff.__get_area(lat, lng, dst)
            dataset1 = dataset1.loc[(dataset1['latitude'] <= maxlat) & (dataset1['latitude'] >= minlat)
                    & (dataset1['longitude'] <= maxlng) & (dataset1['longitude'] >= minlng)]
            genData(file=folder+filename+'.csv',pythonfile=False,cols=columns, lat=lat , lng=lng, dst=dst)
            print("Dataset processing time:")
            print(time()-t)
            dataset = basestuff.dataset
            r = 5;
            gamma = 4;
            setparams(dataset.shape[0], 3, K=5);
            print("Businesses within the given area:")
            print(dataset.shape[0])
            #setparams(100, 3, K=5);
            t = time()
            S1 = MDRC()
            print("Calculation time:")
            print(time()-t)
            print("The size of the subset:")
            print(len(S1))
            print("The index of the subset mapped in the dataset:")
            print(S1)            
            dataset1 = dataset1.iloc[list(S1),1:]
            dataset1 = dataset1.reset_index(drop=True)
            js = dataset1.to_json(orient="index")
            dataset1.to_csv("data\data2.csv", index=False)            
    return HttpResponse(js)