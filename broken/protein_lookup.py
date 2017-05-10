#!/bin/env python

from subprocess import Popen

with open('protein_list.txt', 'r') as ifile:
    for protein in ifile:
        protein = protein.strip()
        Popen("grep -m 1 ""{0}"" /data/projects/MMSeqs2DB/nr_1-31-17/nr.lookup | cut -f1 | (read line_num; sed ""${line_num}q;d"" /data/projects/MMSeqs2DB/nr_1-31-17/nr_h) >> proteins.txt".format(protein), shell=True)
