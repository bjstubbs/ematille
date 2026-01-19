import sys
import os
import subprocess
import pandas as pd
import numpy as np
from collections import deque
fname = sys.argv[1]
print("Processing folder "+fname)
contents = os.listdir(fname)
c2=[x for x in contents if x.endswith("fa")]
contents=c2

class kmerCountDequeue():
    #https://stackoverflow.com/questions/45990454/generating-all-possible-combinations-of-characters-in-a-string
    def keyGen(self,l):
        import itertools
        yield from itertools.product(*([l] * 8))

    def __init__(self):
        self.dna={"A":0,"C":0,"G":0,"T":0}
        self.refSum={}
        for x in self.keyGen('ACGT'):
             self.refSum[''.join(x)]=0

    def __str__(self):
        return("kmerCountDequeue sums \n")

    def clearSums(self):
        self.dna={"A":0,"C":0,"G":0,"T":0}
        self.refSum={}
        for x in keyGen('ACGT'):
             self.refSum[''.join(x)]=0

    def movingSumCum(self,iterable):
        if len(iterable)<8:
            return(None)
        scoreDeque=deque(iterable)
        keyDeque=deque(maxlen=8)
        for i in range(len(iterable)):
            temp=scoreDeque.popleft()
            self.dna[temp]=self.dna[temp]+1
            keyDeque.append(temp)
            if i <7:
                continue
            #key is full
            key="".join(keyDeque)
            self.refSum[key]=self.refSum[key]+1
    def outputSums(self):
        scored=pd.DataFrame.from_dict(self.refSum, orient='index')
        return(scored)

    def outputDNA(self):
        dna=pd.DataFrame.from_dict(self.dna, orient='index')
        return(dna)

def fastaReader(faFile):
    file1 = open(faFile, 'r')
#file1 = open('a.txt', 'r')
    count = 0
    curString=""
    for line in file1:
        if line[0]==">":
            if count>0:
                temp=curString.rstrip().upper().replace("N","").replace("\n","")
                curString=""
                yield temp
            else:
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

for curFile in contents:
	myD5=kmerCountDequeue()
	iname=fname+"/"+curFile
	oname =iname +".csv"
	oname2 =iname +"metrics.csv"

	print("Processing"+iname)
	test1=fastaReader(iname)

	while(True):
		try:
			myD5.movingSumCum(next(test1))
		except StopIteration:
			res=myD5.outputSums()
			dna=myD5.outputDNA()
			break
	res.to_csv(oname)
	dna.to_csv(oname2)

