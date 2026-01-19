import sys
import os
import subprocess
import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix
from collections import deque
import sys

class kmerDequeue():
    def __init__(self,refIndex):
        self.curSums=pd.Series(np.zeros(len(refIndex)))
        self.curSums.index=refIndex
        self.refIndex=refIndex
        self.d = deque()

    def __str__(self):
        return("kmerDequeue sums \n"+str(self.curSums))

    def clearSums(self):
        self.curSums=pd.Series(np.zeros(len(self.refIndex)))
        self.curSums.index=self.refIndex

    def movingScore(self,iterable):
        if len(iterable)<150:
            return(None)
        curString=deque(maxlen=150)
        res=list()
        resKeys=[]
        scoreDeque=deque(iterable)
        keyDeque=deque(maxlen=8)
        self.clearSums()

        for i in range(150):
            temp=scoreDeque.popleft()
            keyDeque.append(temp)
            curString.append(temp)
            if i <7:
                continue
            #key is full
            key="".join(keyDeque)
            self.d.append(ref.loc[key])
            self.curSums=self.curSums+ref.loc[key]
        #print(len(curString))
        res.append(self.curSums)
        resKeys.append("".join(curString))
            #first 150 done, deque full
        for i in range(150,len(iterable)):
            temp=scoreDeque.popleft()
            keyDeque.append(temp)
            curString.append(temp)
            key="".join(keyDeque)
            #key overflows, is still ok
            self.d.append(ref.loc[key])
            self.curSums=self.curSums+ref.loc[key]
            tempSubtract=self.d.popleft()
            self.curSums=self.curSums-tempSubtract
            res.append(self.curSums)
            resKeys.append("".join(curString))
        scored=pd.DataFrame(res)
        scored.index=resKeys
        return(scored)
        #return(res,resKeys)

def fastaReader(faFile):
    file1 = open(faFile, 'r')
#file1 = open('a.txt', 'r')
    count = 0
    curString=""
    for line in file1:
        if line[0]==">":
            #print("in header")
           # we are in header
            if count>0:
                temp=curString.rstrip().upper().replace("N","").replace("\n","")
                curString=""
                yield temp
            else:
                #print("incrementing")
                count=1
        else:
            curString=curString+line
        #print(line)
        #go line force activate!
    #return last one
    temp=curString.rstrip().upper().replace("N","").replace("\n","")
    curString=""
    file1.close()
    yield(temp)

##########################
#Go!
#
#########################

fname = sys.argv[1]
print("Processing file "+fname)
refFile=fname+".ref.csv"
ref=pd.read_csv(refFile,index_col=0)
ref=ref.div(ref.sum(axis=1), axis=0)
ref=ref.T

#load config
file1 = open(fname, 'r')
#for each species
for line in file1:
	if len(line)>1:
		print(line)
		lineArray=line.split()
		#go for animal
		prefix=lineArray[0]
		#load split dir
		procFolder="splits/"+prefix+"/"
		iname=fname+"."+prefix+"chosen.txt"
		filei=open(iname,"r")
		#for each  boulder
		on=0
		for curfile in filei:
			if len(curfile)>1:
				goFile=procFolder+curfile.rstrip().replace(".csv","")
				saveFile=iname+"b"+str(on)+"Scored.csv"
				on=on+1
				print("scoring "+goFile)
				if os.path.getsize(goFile)>5000000:
					continue
				finalRes=list()
				test1=fastaReader(goFile)
				while(True):
					try:
						first=ref.loc["AAAAAAAA"]
						myD=kmerDequeue(first.index)
						finalRes.append(myD.movingScore(next(test1)))
					except StopIteration:
						break
				finalDF=pd.concat(finalRes)
				finalDF.to_csv(saveFile)
		filei.close()
file1.close()
