import numpy as np
import math;

def mylog(st, outputfile):
    outfile = open(outputfile, 'a');
    outfile.write(st + '\n');
    outfile.close();

def UniqueID(ids,n):
    ids = ids[ids.argsort(-1)]
    return str(ids)
    #uid=0;
    #for i in ids:
    #    uid = uid*n+i
    #return uid


def RankingClassesCount(n=100000,m=5,k=5,threshold=100,file=None,header=1, delim=',', cols=(2,4,5,7,8)):
    if file is None:
        data = np.random.rand(n,m)
    else:
        data = np.genfromtxt(file, delimiter=delim, skip_header=header, usecols=cols);
        data = data[0:n, 0:m];
    id = np.arange(n).reshape(n,1)
    rankingclasses = set()
    new = 0;
    while new<threshold:
        f = np.random.rand(m)
        nc = np.ones(n)
        for i in range(n):
            for j in range(m):
                nc[i]+=data[i,j]*f[j]
        tmp = np.concatenate((id,nc.reshape(n,1)), axis=1)
        tmp =  tmp[tmp[:, 1].argsort()] # the higher the better
        UID =  UniqueID(tmp[0:k,0],n)
        if UID not in rankingclasses:
            rankingclasses.add(UID)
            new=0
        else:
            new+=1
    return len(rankingclasses)


#print len(RankingClasses())

