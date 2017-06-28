#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: June 5th, 2017


import argparse

def convert(input_file1, count_matrix):
    # Write output file: Count matrix with annotations appended to its respective geneID
    gene_annot_dict = {}
    outfile = count_matrix + '.annotations'

    with open(outfile, 'w') as ofile:
        with open(count_matrix, 'r') as cmatrix:
            for line in cmatrix:
                elements = line.rstrip('\n').split('\t')
                gene = elements[0]
                # Create empty string for elements to be appended
                element_str = ''
                for element in elements:
                    element_str += '%s\t' % element
                if gene in gene_annot_dict.keys():
                    element_str += '%s\n' % gene_annot_dict[gene]
                else:
                    element_str += 'No Annotation\n'
                # print(element_str)
                ofile.write(element_str)
    ofile.close()




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_file1', help='Input file 1')
    parser.add_argument('count_matrix', help='Count matrix')
    in_args = parser.parse_args()

    convert(in_args.input_file1, in_args.count_matrix)