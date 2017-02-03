#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on: Jan 18 2017

#########
# GOAL: Concatenate DE expression output with associated annotations from the trinotate annotation report
#
# Input: annotation report, names of DE expressed genes(2 files, up & down)
#####

# no_header_annotation_report.xls
infile = open('no_header_annotation_report.xls', 'r')
gene_id = []
# transcript_id = []
sprot_Top_BLASTX_hit = []
# RNAMMER = []
# prot_id = []
# prot_coords = []
sprot_Top_BLASTP_hit = []
# Pfam = []
# SignalP = []
# TmHMM = []
# eggnog = []
# Kegg = []
gene_ontology_blast = []
gene_ontology_pfam = []
# transcript = []
# peptide = []
for line in infile:
    line = line.strip('\n')
    report_data = line.split('\t')

    gene_id.append(report_data[0])
    # transcript_id.append(report_data[1])
    # sprot_Top_BLASTX_hit.append(report_data[2])
    # RNAMMER.append(report_data[3])
    # prot_id.append(report_data[4])
    # prot_coords.append(report_data[5])
    # sprot_Top_BLASTP_hit.append(report_data[6])
    # Pfam.append(report_data[7])
    # SignalP.append(report_data[8])
    # TmHMM.append(report_data[9])
    # eggnog.append(report_data[10])
    # Kegg.append(report_data[11])
    gene_ontology_blast.append(report_data[12])
    gene_ontology_pfam.append(report_data[13])
    # transcript.append(report_data[14])
    # peptide.append(report_data[15])


up_file = open('threeMethods_up.txt', 'r')
down_file = open('threeMethods_down.txt', 'r')
up_genes = []
for line in up_file:
    line = line.strip('\n')
    up_genes.append(line)

down_genes = []
for line in down_file:
    line = line.strip('\n')
    down_genes.append(line)

up_dict = {}
for x in range(len(gene_id)):
    if gene_id[x] in up_genes:
        go_terms = '%s\t%s' % (gene_ontology_blast[x], gene_ontology_pfam[x])
        if go_terms != '.\t.':
            if gene_id[x] in up_dict:
                if go_terms not in up_dict[gene_id[x]]:
                    up_dict[gene_id[x]].append(go_terms)
            else:
                up_dict[gene_id[x]] = [go_terms]

nums = []
with open('up_genes_annotations.txt', 'w') as out_up:
    for key in up_dict:
        nums.append(len(up_dict[key]))
        x = len(up_dict[key])
        # print(x)
        for num in range(x):
            if num == 0:
                data = '%s\t%s\n' % (key, up_dict[key][num])
                out_up.write(data)
            elif num != 0:
                data = '----------\t%s\n' % (up_dict[key][num])
                out_up.write(data)

# nums = set(nums)
# print(nums)


