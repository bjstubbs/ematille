# ematille
Mining for Tick Blood Meal Hosts

# Methods

## Overview

![Ematille Workflow](flow.png){#fig:1 width="1\\linewidth"}

## Input

Ematille is designed as a turnkey solution with minimal configuration
and setup. Input to Ematille consists of a text file describing the
reference species and locations of the fasta files containing their
genomes. Instead of mining the entire genome, you can also provide the
regions of the reference genome that repeatmasker identified as
translatable elements extracted from the reference genome as the
reference.

flist.txt

  --- ---------- ------------------------------------------
    1 coyote     GCA_034620425.1_Cla-1_genomic.fna
    2 snake      GCA_023053685.1_rDiaPun1.0.p_genomic.fna
    3 deertick   GCF_000208615.1.fa
    4 mouse      mm39.fa
    5 squirrel   speTri2.fa
  --- ---------- ------------------------------------------

files downloaded from:

* https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/034/620/425/GCA_034620425.1_Cla-1/GCA_034620425.1_Cla-1_genomic.fna.gz
* https://hgdownload.soe.ucsc.edu/goldenPath/mm39/bigZips/mm39.fa.gz
* https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/023/053/685/GCA_023053685.1_rDiaPun1.0.p/GCA_023053685.1_rDiaPun1.0.p_genomic.fna.gz
* https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/236/235/GCF_000236235.1_SpeTri2.0/GCF_000236235.1_SpeTri2.0_genomic.fna.gz
* https://hgdownload.soe.ucsc.edu/hubs/GCF/000/208/615/GCF_000208615.1/GCF_000208615.1.fa.gz

## Calculate Reference Statistics

Ematille begins by creating 8-mer statistics on each of the reference
genomes. A reference genome is a fasta formatted text file containing a
collection of non-contiguous sequences of variable number and length. As
a result of experimental, biological, and technological limitations,
these references can contain wildly different numbers of sequences with
more confident genomes typically having less pieces than developing
assemblies.

We use a double ended queue to pan over each contig in a reference. As
the cursor travels over the sequence, we use the current 8-mer as a key
to increment the dictionary containing the current count data. We do not
count 8-mers that cross sequence boundaries. As we pan, we also keep
track of the counts of A,C,G, and T's we see to use in information
content calculations later.

The result of this step is a set of three files per reference:

-   GCA_023053685.1_rDiaPun1.0.p_genomic.fna

-   GCA_023053685.1_rDiaPun1.0.p_genomic.fna.csv

-   GCA_023053685.1_rDiaPun1.0.p_genomic.fnametrics.csv

This is done in ematille as follows:

1. python genRefSum.py flist.txt

generates a shell script flist.txt.RefSum.sh:

```{}
python ../ematilleSumFile.py /cluster/tufts/bj/ref/GCA_034620425.1_Cla-1_genomic.fna
python ../ematilleSumFile.py /cluster/tufts/bj/ref/GCA_023053685.1_rDiaPun1.0.p_genomic.fna
python ../ematilleSumFile.py /cluster/tufts/bj/ref/GCF_000208615.1.fa
python ../ematilleSumFile.py /cluster/tufts/bj/ref/mm39.fa
python ../ematilleSumFile.py /cluster/tufts/bj/ref/speTri2.fa
```

This script can be run to generate the sums detailed above

## Split and Sum References

In this step, Ematille first splits the references into roughly equal
chunks called boulders. The nature of the reference genomes can lead to
difficulty splitting things, so we first count the number of subsequencs
in the reference, and then alter our strategy based on the result.

We use faSplit from the UCSC genome browser to do the split
If we see less than 5,000 subsequences, then we probably
have a more confident genome and we use the \"size\" parameter to split
the genoome into roughly 1,000,000 BP boulders. Else, we have a very
fractious genome, and instead of splitting by base, we split into
boulders that are roughly 1,000,000 bytes each using the \"about\"
option.

After we split the reference genomes, we repeat the summing process we
did on the references for each boulder we created. The result is a
\"splits\" directory containing one folder per species, with each
species' folder containing some number of file collections that each
contain the sequence, the 8-mer counts in a csv, and a file containing
the A,C,G,T metrics for the boulder.

    coyote/
    |-- coyotea1e600.fa
    |-- coyotea1e600.fa.csv
    |-- coyotea1e600.fametrics.csv
    ...

In Ematille we do this by:

1. python genSplitSh.py flist.txt

generates a shell script flist.txt.Split.sh: 

```{}
faSplit about /cluster/tufts/bj/ref/GCA_034620425.1_Cla-1_genomicTE.fna 1000000 splits/coyote/coyotea1e6
faSplit about /cluster/tufts/bj/ref/GCA_023053685.1_rDiaPun1.0.p_genomicTE.fna 1000000 splits/snake/snakea1e6
faSplit about /cluster/tufts/bj/ref/GCF_000208615.1TE.fa 1000000 splits/deertick/deerticka1e6
faSplit about /cluster/tufts/bj/ref/mouseTE.fa 1000000 splits/mouse/mousea1e6
faSplit about /cluster/tufts/bj/ref/sqTE.fa 1000000 splits/squirrel/squirrela1e6
```

After running this shell script we should have a directory called spliotr wi
