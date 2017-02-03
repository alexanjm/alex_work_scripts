#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on: Feb 2, 2017

#########
# GOAL: Submit transdecoder blastp jobs while splitting sequences --speed up the process
#
# Input: transdecoder.pep3
#
#####

import os
import sys
import argparse
from buddysuite import buddy_resources as br
from buddysuite import SeqBuddy as sb
from subprocess import Popen, PIPE
from multiprocessing import Lock
from math import ceil, floor

# TO DO:
# figure out why number of blast hits is less than number of records - from command line

def mc_blast(records_list, args):
    database, outfile = args
    temp_file = br.TempFile()
    sub_input_seqs = sb.SeqBuddy(records_list, out_format='fasta')
    sub_input_seqs.write(temp_file.path)

    blast_cmd = "blastp -query %s -db %s -num_threads 3 -max_target_seqs 1 -outfmt 6" % (temp_file.path, database)
    output = Popen(blast_cmd, stdout=PIPE, shell=True).communicate()
    output = output[0].decode()
    with lock:
        with open(outfile, 'a') as ofile:
            ofile.write(output)
    return

lock = Lock()

if __name__ == '__main__':
    args = sys.argv
    parser = argparse.ArgumentParser(description='GOAL: Submit transdecoder blastp jobs while splitting sequences '
                                                 '--speed up the process')
    parser.add_argument('input_file', help='transdecoder file')
    parser.add_argument('database', help='blastp database path')
    parser.add_argument('num_cores', type=int, help='number of cores')
    parser.add_argument('-gs', '--group_size', type=int, help='group size')
    parser.add_argument('-o', '--out_file', default='blastp.outfmt6', help='output file')
    parser.add_argument('-q', '--quiet', help='suppress run time output counter', action='store_true')
    in_args = parser.parse_args()
    input_seqs = sb.SeqBuddy(in_args.input_file)
    num_cores = floor(in_args.num_cores / 3)
    group_size = ceil(len(input_seqs) / num_cores) if not in_args.group_size else in_args.group_size
    records_list = [input_seqs.records[i:i + group_size] for i in range(0, len(input_seqs.records), group_size)]

    # To Do:
    # make test to see if file already exists
    if os.path.exists(in_args.out_file):
        print('WARNING: This file already exists!')
        sys.exit()
    else:
        open(in_args.out_file, 'w').close()
    # mc_blast(records_list[0], [in_args.database, in_args.out_file])

        br.run_multicore_function(records_list, mc_blast, [in_args.database, in_args.out_file], max_processes=num_cores, quiet=in_args.quiet)






