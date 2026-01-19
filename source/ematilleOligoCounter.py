#!/usr/bin/env python3
"""

Updates:

1. added helper functions to read csv from primer3 output
2. converted everything to dictionaries instead of scalars

#begin Donna below

Computing output stats for one oligo file and a target seq directory
1.  Read each FASTA file in dir; get one boulder seq at a time.
    Read the separate input file of oligo trios; store in list.
2.  for each boulder: 
2a.    Find locations of each oligo in the boulder. 
2b.    Count how often the primers are within MAXDIST of each other
2c.    Count how often the middle oligo is in between them.  
2d.    Add these to an overall tally.
3.  Print the tally when done  

Ultimately, run for all oligo sets and for all target species / zoo species. 
"""

MAXDIST = 250 # max distance between left and right primers in boulders


import numpy as np
import pandas as pd


def primer_line(pline):
    return(pline.iloc[1]+" "+pline.iloc[2]+" "+pline.iloc[3])


def primer_lineu(pline):
    return(pline.iloc[1]+" "+pline.iloc[3])


def read_primers(pFile):
    temp=pd.read_csv(pFile)
    temp=temp.dropna()
    temp2=temp.apply(primer_line,1)
    temp3=temp.apply(primer_lineu,1)
    tempd=dict(zip(temp3, temp2))
    return(list(tempd.values()))


def read_oligos(filename):
    # Read oligo sequences from a file, one trio per line.
    # Return a list of oligo sequence trios to search for in fasta files.

    oligos = []
    with open(filename, 'r') as file:
        for line in file:
            oligo = line.strip().upper()  # Convert to uppercase 
            if oligo:  # Skip empty lines
                oligos.append(oligo)
    return oligos

def add_dict(h1,h2):
    h3={}
    for key in h1.keys():
        h3[key]=h1[key]+h2[key]
    return(h3)

def add2counts(pairhits, triohits, lpos, mpos, rpos):
    # Do the actual counting

    newpair=newtrio=lptr=rptr=mptr=0
    while (lptr < len(lpos) and rptr < len(rpos)):  # loop thru both pos lists
        if (lpos[lptr] < rpos[rptr] - MAXDIST):  # move lptr if needed
            lptr = lptr + 1
        elif (lpos[lptr] < rpos[rptr]): # if in range, count pair and test mid
            newpair = newpair + 1
            if (len(mpos) > 0):  # look for center probe
                while (mptr < len(mpos) and mpos[mptr] < lpos[lptr]):
                    mptr = mptr + 1
                if (mptr < len(mpos) and mpos[mptr] < rpos[rptr]):
                    newtrio = newtrio + 1                    
            lptr = lptr + 1   # for now, don't allow dup use of same mid oligo
            rptr = rptr + 1   #   w different primers
        else: 
            rptr = rptr + 1  
    return(newpair+pairhits, newtrio+triohits)

def empty_dict(plist):
    tempd=dict(zip(plist, [0]*len(plist)))
    return(tempd)

def find_in_boulder(boulder, oligo_file):
    # Given boulder sequence and a file with oligo trios, look at each 
    # trio and call add2counts to do the counting
    try:
        # get the boulder sequence, an argument
        boulderseq = boulder
        if (not isinstance(boulderseq, str)):  # just checking 
            print("boulder seq is not a string")
            boulderseq=str(boulderseq)		

        # Read the oligos
        #pairhits = 0
        #triohits = 0
        #oligolist = read_oligos(oligo_file)  
        oligolist = read_primers(oligo_file)  
        pairhits=empty_dict(oligolist)
        triohits=empty_dict(oligolist)


        for trio in oligolist: 
            (left, ctr, right) = trio.split() # split on spaces
            orig=right
            right=str(Seq(right).reverse_complement())  

            leftpos = [match.start() for match in re.finditer(left,boulderseq)]
            rightpos = [match.start() for match in re.finditer(right,boulderseq)]
            if (len(leftpos+rightpos) > 0):  # if you find anything, add 2 cnt
                # look for central oligo in either orientation
                midpos = [match.start() for match in re.finditer(ctr,boulderseq)]
                # flip = str(Seq(ctr).reverse_complement())
                # flippos = [match.start() for match in re.finditer(ctr,boulderseq)]
                # mergepos = sorted(set(midpos+flippos))  # uniq sorted merged list
                #(pairhits, triohits) = add2counts(pairhits, triohits,
                 #                                 leftpos, midpos, rightpos)  # can sub mergepos if want both
                (p1, t1) = add2counts(0, 0, leftpos, midpos, rightpos)
                pairhits[trio]=p1
                triohits[trio]=t1
        return(pairhits, triohits)
    
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main(fasta_dir, oligo_file):
    oligolist = read_primers(oligo_file)  
    totalpair=empty_dict(oligolist)
    totaltrio=empty_dict(oligolist)
    ofile=oligo_file+"-"+fasta_dir+".csv"
    ofile=ofile.replace("/","_")

    #totalpair = 0
    #totaltrio = 0
    fastalist = [f for f in listdir(fasta_dir)
                 if (isfile(join(fasta_dir, f)) and f[-3:] == ".fa")]

    # get the records from the fasta files
    for num, fasta_file in enumerate(fastalist):
        for record in SeqIO.parse(fasta_dir+fasta_file, 'fasta'):
            # count positions of each oligo in the file
            record.seq = Seq((str(record.seq)).upper())
            (val1,val2) = find_in_boulder(record.seq, oligo_file)
            #totalpair += val1
            #totaltrio += val2
            totalpair=add_dict(totalpair,val1)
            totaltrio=add_dict(totaltrio,val2)
        if num % 100 == 0:  # tell the user how far you've gone
            print("Just read fasta file",num)

    #print("Found a total of ",totalpair," pairs within ", MAXDIST, " and ")
    #print(totaltrio, "of them include the central oligo")
    r2=pd.DataFrame.from_dict(totalpair, orient='index')
    r2=r2.rename(columns={0: "pairs"})
    r3=pd.DataFrame.from_dict(totaltrio, orient='index')
    r3=r3.rename(columns={0: "trios"})
    r4=r2.merge(r3,left_index=True, right_index=True)
    r4.to_csv(ofile)
    return


if __name__ == "__main__":
    import sys
    from os import listdir
    from os.path import isfile, join
    from Bio import SeqIO
    from Bio.Seq import Seq
    import re
    
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python oligo_counter.py <fasta_dir> <oligo_file>")
        print("Example: python oligo_counter.py sequencedir oligos.txt")
        sys.exit(1)
    
    fasta_dir = sys.argv[1]
    oligo_file = sys.argv[2]

    if not (fasta_dir[-1] == "/"):  # make sure can concat filenames to dir
        fasta_dir = fasta_dir + "/" 
    
    main(fasta_dir, oligo_file)

