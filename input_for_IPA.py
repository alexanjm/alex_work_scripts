#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: Jan 5th, 2018

# GOAL: Combine expression data with blastp data for input into IPA

import argparse


def ipa_input(input_file1, input_file2):
    gene_ann_dict = {}
    with open(input_file1, 'r') as ifile1:
        for line in ifile1:
            line = line.rstrip('\n').split('\t')
            trin_id = line[0]
            gene_id = line[1]
            gene_ann_dict[trin_id] = gene_id
    ifile1.close()
    print(len(gene_ann_dict))



    output_file = input_file2 + '.ipa'
    with open(output_file, 'w') as ofile:
        with open(input_file2, 'r') as ifile2:
            for line in ifile2:
                line = line.rstrip('\n')
                elements = line.rstrip('\n').split('\t')
                if elements[0] in gene_ann_dict.keys():
                    new_line = '%s\t%s\n' % (gene_ann_dict[elements[0]], line)
                else:
                    new_line = 'No Annotation\t%s\n' % (line)
                ofile.write(new_line)

        ifile2.close()
    ofile.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_file1', help='Input file1')
    parser.add_argument('input_file2', help='Input file2')

    in_args = parser.parse_args()

    print(in_args.input_file1 + '.ipa')

    ipa_input(in_args.input_file1, in_args.input_file2)

    # to test speed -- probably need to hard code input/output files to make the below run correctly...
    # import timeit
    # print(timeit.repeat("test()", setup="from __main__ import test", number=1, repeat=1))
