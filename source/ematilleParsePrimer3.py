import sys
import os
import sys
import numpy as np
import pandas as pd


def p3toD(p3file):
    p3dict={}
    filei=open(p3file,"r")
    for linei in filei:
        if len(linei)>5:
            if "SEQUENCE_ID=" in linei:
                nam=linei.rstrip().replace("SEQUENCE_ID=","")
                p3dict[nam]={}
            else:
                temp=linei.rstrip().split("=")
                p3dict[nam][temp[0]]=temp[1]
    return(p3dict)

def printPrimerList(primerdict,ofile="a.csv"):
    out=open(ofile,"w")
    out.write("seqid,sequence\n")
    for primerkey in primerdict.keys():
        primer=primerdict[primerkey]
        for j in range(5):
            try:
                key="PRIMER_LEFT_"+str(j)+"_SEQUENCE"
                out.write(primerkey+"-"+key+","+primer[key]+"\n")
                key="PRIMER_INTERNAL_"+str(j)+"_SEQUENCE"
                out.write(primerkey+"-"+key+","+primer[key]+"\n")
                key="PRIMER_RIGHT_"+str(j)+"_SEQUENCE"
                out.write(primerkey+"-"+key+","+primer[key]+"\n")
            except KeyError as e:
                print(key)
                pass
    out.close()

def printPrimerDF(primerdict,ofile="a2.csv"):
    out=open(ofile,"w")
    out.write("seqid,left,inner,right\n")
    for primerkey in primerdict.keys():
        primer=primerdict[primerkey]
        for j in range(5):
            try:
                out.write(primerkey+",")
                key="PRIMER_LEFT_"+str(j)+"_SEQUENCE"
                out.write(primer[key]+",")
                key="PRIMER_INTERNAL_"+str(j)+"_SEQUENCE"
                out.write(primer[key]+",")
                key="PRIMER_RIGHT_"+str(j)+"_SEQUENCE"
                out.write(primer[key])
            except KeyError as e:
                #pass
                out.write(primerkey+",,")
            out.write("\n")
    out.close()


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
for line in file1:
	on=0
	if len(line)>1:
		print(line)
		lineArray=line.split()
		#go for animal
		prefix=lineArray[0]
		#load split dir
		iname=fname+"."+prefix+".primer3.out"
		saveFile1=fname+"."+prefix+".primer3List.txt"
		saveFile2=fname+"."+prefix+".primer3DF.csv"
		res=p3toD(iname)
		printPrimerList(res,saveFile1)
		printPrimerDF(res,saveFile2)
file1.close()

