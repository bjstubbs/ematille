import sys
import os
import pandas as pd
import numpy as np
import math
from collections import deque

def calcCover(mys):
    res={}
    if len(mys)<3:
        return(None)
    scoreDeque=deque(mys)
    keyDeque=deque(maxlen=3)
    for i in range(len(mys)):
        temp=scoreDeque.popleft()
        keyDeque.append(temp)
        if i <2:
            continue
            #key is full
        key="".join(keyDeque)
        if key not in res:
            res[key]=1
    return(len(res)>=32)
            

def procFile(iname,prefix,b):
	if not os.path.isfile(iname):
		return(None)
	#load data scored file
	temp=pd.read_csv(iname,index_col=0)
	keep=list(map(calcCover,list(temp.index)))
	temp=temp.loc[keep]
	#sort by prefix's score (target animal)
	temp.sort_values(by=[prefix],inplace=True,ascending=False)
	#take the top 20 %, remove dups
	cut=int(np.floor(len(temp)*.2))
	temp=temp.iloc[0:cut]
	temp2 = temp.reset_index().drop_duplicates(subset='index', keep='last').set_index('index')
	#rank columns
	temp2=temp2.rank()
	#get other animals, rank, get median
	otherAnimals=list(temp.columns)
	otherAnimals.remove(prefix)
	tempMed=temp2.apply(lambda x: x[otherAnimals].median(), axis=1)
	#subtract rank of target- med rank of all others
	temp3=temp2[prefix]-tempMed
	#sort and take top
	temp3.sort_values(ascending=False, inplace=True)
	#output results (append)
	oname=fname+"."+prefix+"chosen.txtScored.csvChosen.txt"
	file2 = open(oname, 'a')
	oname2=fname+"."+prefix+".primer3.txt"
	file3=open(oname2,'a')
	for h in range(5):
		if h>0: file3.write("\n")
		file2.write(str(temp3.index[h])+"\n")
		a='''SEQUENCE_ID='''+prefix+str(b)+"-"+str(h)+'''
SEQUENCE_TEMPLATE='''+str(temp3.index[h])+'''
PRIMER_TASK=generic
PRIMER_PICK_LEFT_PRIMER=1
PRIMER_PICK_INTERNAL_OLIGO=1
PRIMER_PICK_RIGHT_PRIMER=1
PRIMER_EXPLAIN_FLAG=1
='''
		file3.write(a)
	file3.write("\n")
	file2.close()
	file3.close()

# go
# load experiment file
fname = sys.argv[1]
print("Processing file "+fname)
refFile=fname+".ref.csv"
oname3=fname+".primer3.sh"
file4=open(oname3,'w')
file1 = open(fname, 'r')


#fname/file1 is flist
#oname/file2 is flist.txt.coyotechosen.txtScored.csvChosen.txt
#oname2/file3 is input to primer3, flist.txt.bbird.primer3.txt
#oname3/file4 is shell script flist.txt.primer3.sh


#for each species in zoo
for line in file1:
	#if there is data
	on=0
	if len(line)>1:
		print(line)
		lineArray=line.split()
		#go for animal
		#write primer 3 command to sh file
		prefix=lineArray[0]
		oname2=fname+"."+prefix+".primer3.txt"
		oname4=fname+"."+prefix+".primer3.out"
		file4.write("primer3_core "+ oname2 + " --output="+oname4+"\n")
		#wasteful way to reset files, may remove later
		file3=open(oname2,'w')
		file3.close()
		oname=fname+"."+prefix+"chosen.txtScored.csvChosen.txt"
		file2=open(oname,'w')
		file2.close()
		#setup for scored loop
		for gonum in range(10):
			#files look like flist.txt.coyotechosen.txtb2Scored.csv
			iname=fname+"."+prefix+"chosen.txt"+"b"+str(gonum)+"Scored.csv"
			procFile(iname, prefix,gonum)
file1.close()
file4.close()


