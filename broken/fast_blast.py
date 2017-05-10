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
    # separate the args into its respective variable
    database, outfile = args
    # set temp_file as a buddy resource variable
    temp_file = br.TempFile()
    # set this variable to each record in records_list -- fasta format
    sub_input_seqs = sb.SeqBuddy(records_list, out_format='fasta')
    # write each sequence/record name to the temp_file of a certain path
    sub_input_seqs.write(temp_file.path)
    # generic blastp command for each file, blastdb used
    blast_cmd = "blastp -query %s -db %s -num_threads 3 -max_target_seqs 1 -outfmt 6" % (temp_file.path, database)
    # utilize Popen to write the full blastp command to execute
    output = Popen(blast_cmd, stdout=PIPE, shell=True).communicate()
    # output = [stdout, stderr] - get stdout and decode
    output = output[0].decode()
    # write to file while locked so no other processes can write at the same time
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
    # sb.Seqbuddy(input_file) creates a variable of input sequences
    input_seqs = sb.SeqBuddy(in_args.input_file)
    # number of 'groups' of cores -- we divide the total number requested by 3 (number of jobs to perform at once)
    # we have to floor it b/c remainders/leftover cores are not allowed -- need at least 3 cores per job
    num_cores = floor(in_args.num_cores / 3)
    # if we specify group sizes, we're good to go -- otherwise, group size is the ceil(len(input_seqs)/num_cores)
    # You should usually try to specify group sizes
    group_size = ceil(len(input_seqs) / num_cores) if not in_args.group_size else in_args.group_size
    # specifies which records/seqs are in each group based on group size -- list comprehension
    records_list = [input_seqs.records[i:i + group_size] for i in range(0, len(input_seqs.records), group_size)]

    ##########
    # Test if the file already exists -- if so exit the script and do not overwrite -- otherwise continue
    if os.path.exists(in_args.out_file):
        print('WARNING: This file already exists!')
        sys.exit()
    else:
        open(in_args.out_file, 'w').close()
    # mc_blast(records_list[0], [in_args.database, in_args.out_file])
        # use run_multicore_function from buddy resources
        # run_multicore_function(iterable, function, func_args=FALSE, max_processes=0, quiet=FALSE, out_type=sys.stdout)
        br.run_multicore_function(records_list, mc_blast, [in_args.database, in_args.out_file], max_processes=num_cores,
                                  quiet=in_args.quiet)






