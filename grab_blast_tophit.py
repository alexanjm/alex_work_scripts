#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: May 31, 2017

# GOAL: This script sorts through blast output to grab the top hit -- based on evalue -- to display for
# each gene isoform

import argparse


def test(input_file):
    # input_file = 'transdecoder_Hech_hydraNR.results'
    # output_file = 'transdecoder_Hech_hydraNR.results.top_hit'
    output_file = input_file + '.top_hit'
    final_data = {}
    with open(output_file, 'w') as ofile:
        with open(input_file, 'r') as ifile:
            for line in ifile:
                if line.startswith('#') is False:
                    transcript, info = line.rstrip('\n').split('\t', 1)
                    if bool(transcript in final_data.keys()) is False:
                        final_data[transcript] = info
                        ofile.write(line)
        ifile.close()
    ofile.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_file', help='Input file')
    in_args = parser.parse_args()

    print(in_args.input_file + '.top_hit')

    test(in_args.input_file)

    # to test speed -- probably need to hard code input/output files to make the below run correctly...
    # import timeit
    # print(timeit.repeat("test()", setup="from __main__ import test", number=1, repeat=1))
