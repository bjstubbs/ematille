import sys
import os
import subprocess
fname = sys.argv[1]
print("Processing file "+fname)
ofile=fname+".FolderSum.sh"
file1 = open(fname, 'r')
file2 = open(ofile, 'w')

for line in file1:
	if len(line)>1:
		print(line)
		lineArray=line.split()
		path=os.getcwd()+"/splits/"+lineArray[0]
		cmd="python ../ematilleSumFolder.py "+path+"\n"
		file2.write(cmd)
file1.close()
file2.close()

