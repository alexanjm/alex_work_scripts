#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: Dec 6th, 2017

# GOAL: Filter blastp results by percent alignment

import argparse


def filter_alignment(input_file, percent):

    out_percent_str = '%s' % percent
    output_file = input_file + '.filter' + out_percent_str
    with open(output_file, 'w') as ofile:
        with open(input_file, 'r') as ifile:
            for line in ifile:
                blast_hit = line.rstrip('\n').split('\t')
                q_len = float(blast_hit[3])
                align_len = float(blast_hit[4])

                if (align_len/q_len) >= percent/100:
                    ofile.write(line)

        ifile.close()
    ofile.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_file', help='Input file')
    parser.add_argument('-p', '--percent', help='<Minimum alignment percent desired', type=int)
    in_args = parser.parse_args()

    print(in_args.input_file + '.filter' + str(in_args.percent))

    filter_alignment(in_args.input_file, in_args.percent)

    # to test speed -- probably need to hard code input/output files to make the below run correctly...
    # import timeit
    # print(timeit.repeat("test()", setup="from __main__ import test", number=1, repeat=1))
