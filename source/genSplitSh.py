import sys
import os
import subprocess
fname = sys.argv[1]
print("Processing file "+fname)
ofile=fname+".Split.sh"
file1 = open(fname, 'r')
file2 = open(ofile, 'w')

# Specify the directory name
directory_name = "splits"

# Create the directory
try:
	os.mkdir(directory_name)
	print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
	print(f"Directory '{directory_name}' already exists.")
except PermissionError:
	print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
	print(f"An error occurred: {e}")

for line in file1:
	if len(line)>1:
		print(line)
		lineArray=line.split()
		try:
			os.mkdir("splits/"+lineArray[0])
			print(f"Directory '{directory_name}' created successfully.")
		except FileExistsError:
			print(f"Directory '{directory_name}' already exists.")
		except PermissionError:
			print(f"Permission denied: Unable to create '{directory_name}'.")
		except Exception as e:
			print(f"An error occurred: {e}")
		cmd = 'grep -c "^>" '+ lineArray[1]
		out = int(subprocess.run([cmd], shell=True, capture_output=True, text=True).stdout.rstrip())

		#out = subprocess.check_output(cmd)
		print('returned value:', out)        
		#process = subprocess.Popen(['grep','-c', '^>', fname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#out, err = process.communicate()
		#print(out)
		#out=out.decode('UTF-8').rstrip()
		#print("found "+str(out)+ " contigs")
		if(out>5000):
			cmd="faSplit about "+lineArray[1]+" 1000000 splits/"+lineArray[0]+"/"+lineArray[0]+"a1e6\n"
		else:
			cmd="faSplit size "+lineArray[1]+" 1000000 splits/"+lineArray[0]+"/"+lineArray[0]+"s1e6\n"
		file2.write(cmd)
file1.close()
file2.close()

