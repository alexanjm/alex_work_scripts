#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: June 5th, 2017


### GOAL ###
# This script converts a list of blast hits at the ISOFORM level to a list of only top hits at the GENE level

import argparse

def convert(input_file):
    output_file = input_file + '.genes'
    gene_dict = {}
    # input file is blast output with annotation appended
    with open(input_file, 'r') as ifile:
        for line in ifile:
            elements = line.rstrip('\n').split('\t')
            evalue = float(elements[9])
            # set e value cutoff for blast hits
            evalue_cutoff = 0.00001
            if evalue < evalue_cutoff:
                annotation = elements[14].strip('\x00')
                elements[14] = annotation
                isoform = elements[0].split('|')[0]
                # split the isoform number off from the end of each ID
                gene = isoform.rsplit('_', 1)[0]
                # If the gene already exists in the gene dictionary, use the hit with the lower evalue
                if bool(gene in gene_dict.keys()) is True:
                    # print(gene, gene_dict[gene][9])
                    # print(float(gene_dict[gene][9]), float(evalue))
                    # print(float(gene_dict[gene][9]) > float(evalue))
                    if float(gene_dict[gene][9]) > float(evalue):
                        gene_dict[gene] = elements
                else:
                    gene_dict[gene] = elements
    ifile.close()

    # Write output file with best hit for each gene
    with open(output_file, 'w') as ofile:
        for key in gene_dict:
            new_string = '%s\t' % key
            for element in gene_dict[key]:
                new_string += '%s\t' % element
            new_string += '\n'
            ofile.write(new_string)
    ofile.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_file', help='Input file')
    in_args = parser.parse_args()

    convert(in_args.input_file)
