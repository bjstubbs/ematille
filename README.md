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
    3 tick       GCF_050947875.1_ASM5094787v1_genomic.fna
    4 mouse      mm39.fa
    5 squirrel   speTri2.fa
  --- ---------- ------------------------------------------

## Calculate Reference Statistics
