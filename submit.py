#!/bin/env python

from subprocess import Popen

for i in range(1,51):

       	Popen("qsub -M alexander.jones@nih.gov -m abes -j y -w e -cwd -pe make-dedicated 2 -l mem_free=2G,h_vmem=2G -b y blastp -query /data/projects/barreira/strandSpecific_transcriptome/trinotate/alex_blast/split_blast/{0} -db /data/projects/BlastDB/NCBI/nr/nr -num_threads 2 -max_target_seqs 1 -outfmt 6 >> blastp_{0}.outfmt6".format(i), shell=True)
