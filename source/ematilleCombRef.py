import sys
import os
import subprocess
import pandas as pd
import numpy as np

fname = sys.argv[1]
print("Processing file "+fname)
ofile=fname+".ref.csv"
file1 = open(fname, 'r')

on=0
for line in file1:
	if len(line)>1:
		print(line)
		lineArray=line.split()
		prefix=lineArray[0]
		refFile=lineArray[1]+".csv"
		temp=pd.read_csv(refFile,index_col=0)
		temp=temp.rename(columns={"0": prefix})
		if on==0:
			res=temp.T
			on=1
		else:
			temp2=temp.T
			res=pd.concat([res, temp2])
res.to_csv(ofile)
file1.close()

