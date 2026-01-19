import sys
import os
import subprocess
import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix

#no IC at this time
import math
#def IC(queryMetricsFile):
#    temp=pd.read_csv(queryMetricsFile,index_col=0)
#    temp=temp.rename(columns={"0": "current"})
#    temp=temp.T
#    temp=temp.div(temp.sum(axis=1), axis=0)
#   # print(temp)
#    icVal=0
#    for let in ["A","C","G","T"]:
#        cur=-1*(temp[let].iloc[0]*math.log2(temp[let].iloc[0]))
#        icVal=icVal+cur
#    return(icVal)

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
		#load split dir
		procFolder="splits/"+prefix+"/"
		contents = os.listdir(procFolder)
		#filter to csvs
		c2=[x for x in contents if x.endswith("fa.csv")]
		for f in c2:
			#path
			f2=procFolder+f
			f3=f2
			f3=f3.replace("fa.csv","fametrics.csv")
		#	#dna=pd.read_csv(f3,index_col=0)
		#	#if dna.loc["A"].iloc[0]<200000:
		#		continue
		#	#if dna.loc["C"].iloc[0]<200000:
                #         #       continue
		#	if dna.loc["G"].iloc[0]<200000:
                #                continue
		#	if dna.loc["T"].iloc[0]<200000:
                #                continue			
		#	#print(f2)
		#		#load csv, transpose, add rowname
		#	#icval=IC(f3)
		#	#icval=float(icval.iloc[0])
		#	#if(icval<1.5):
		#	#	continue
			temp=pd.read_csv(f2,index_col=0).T
			if temp.sum(axis=1).iloc[0]<800000:
				continue
		#	#temp.index=[f]
			#convert to ratios
			temp=temp.div(temp.sum(axis=1), axis=0)
			#get distcance
			a=distance_matrix(temp,ref)
			a=pd.DataFrame(a)
			a=a.rename(columns=dict(zip(range(len(ref.index)),ref.index)))
			a.index=[f]
			#if we are new make a new thing
			if on==0:
				res=a
				on=1
			#else add to it
			else:
				res=pd.concat([res, a])
		oname=fname+"."+prefix+".csv"
		res.to_csv(oname)
file1.close()

