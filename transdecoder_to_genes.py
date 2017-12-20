#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: Dec 19th, 2017


# GOAL ###
# This script converts a list of blast hits at the ISOFORM level to a list of only top hits at the GENE level
# for input to BLAST

input_file = 'Trinity.fasta.transdecoder_renamedHeaders.pep3'
output_file = input_file + '.gene_level'
gene_dict = {}
gene_order = []

with open(input_file, 'r') as ifile:
    for line in ifile:
        line = line.rstrip("\n")
        if line.startswith(">"):
            new = line.strip(">").split(" ")

            # gene_id = new[0].rsplit("_", 1)
            # print(gene_id[0])
            length = new[1].split(":")[1]

            # print(length)
            # if new[0] not in gene_order:
            #     gene_order.append(new[0])
            gene_dict[new[0]] = {'length': length}
            gene_order.append(new[0])
        else:
            seq = line
            gene_dict[new[0]]['seq'] = seq
ifile.close()

print(len(gene_dict))
print(len(gene_order))

new_order = []
new_gene_dict = {}

for id in gene_order:
    gene_id = id.rsplit("_", 1)[0]
    if gene_id in new_order:
        if (gene_dict[id]['length'] > new_gene_dict[gene_id]['length']):
            new_gene_dict[gene_id] = {'length': gene_dict[id]['length'], 'seq': gene_dict[id]['seq']}
    else:
        new_gene_dict[gene_id] = {'length': gene_dict[id]['length'], 'seq': gene_dict[id]['seq']}
        new_order.append(gene_id)

print(len(new_gene_dict))
print(len(new_order))


with open(output_file, 'w') as ofile:
    for new_id in new_order:
        id_line = '>%s len:%s\n' % (new_id, new_gene_dict[new_id]['length'])
        seq_line = '%s\n' % (new_gene_dict[new_id]['seq'])
        ofile.write(id_line)
        ofile.write(seq_line)
ofile.close()

