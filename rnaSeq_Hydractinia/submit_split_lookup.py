#!/bin/env python

from subprocess import Popen

with open('file_names.txt', 'r') as ifile:
    for i in ifile:
        i = i.strip('\n')
        submit_str = "qsub %s.protein_lookup.sh" % i
        Popen(submit_str, shell=True)

