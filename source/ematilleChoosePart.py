import sys
import os
import pandas as pd
import numpy as np

fname = sys.argv[1]
print("Processing file "+fname)
refFile=fname+".ref.csv"
ref=pd.read_csv(refFile,index_col=0)
ref=ref.div(ref.sum(axis=1), axis=0)

file1 = open(fname, 'r')
for line in file1:
	on=0
	if len(line)>1:
		print(line)
		lineArray=line.split()
		#go for animal
		prefix=lineArray[0]
		iname=fname+"."+prefix+".csv"
		temp=pd.read_csv(iname,index_col=0)
		temp2=temp.copy()
		temp2=temp2.drop(prefix,axis=1)
		temp2=temp2.rank()
		temp2['med']=temp2.apply(lambda x: x.median(), axis=1)
		keep=temp2.sort_values(by='med',ascending=False).head(10).index
		#keep=temp2["med"].idxmax()
		oname=fname+"."+prefix+"chosen.txt"
		file2 = open(oname, 'w')
		for f in keep:
			file2.write(f+"\n")
		file2.close()
file1.close()
