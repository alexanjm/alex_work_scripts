#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on: Jan 18 2017

#########
# GOAL: Parse annotation report to get # of transcripts with annotations
#
# Input: annotation report
#####

#no_header_annotation_report.xls
infile = open('new_no_header_report.xls', 'r')
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
# gene_ontology_blast = []
# gene_ontology_pfam = []
# transcript = []
# peptide = []
for line in infile:
    line = line.strip('\n')
    report_data = line.split('\t')
    #(report_data[2])

    gene_id.append(report_data[0])
    # transcript_id.append(report_data[1])
    # sprot_Top_BLASTX_hit.append(report_data[2])
    # RNAMMER.append(report_data[3])
    # prot_id.append(report_data[4])
    # prot_coords.append(report_data[5])
    sprot_Top_BLASTP_hit.append(report_data[6])
    # Pfam.append(report_data[7])
    # SignalP.append(report_data[8])
    # TmHMM.append(report_data[9])
    # eggnog.append(report_data[10])
    # Kegg.append(report_data[11])
    # gene_ontology_blast.append(report_data[12])
    # gene_ontology_pfam.append(report_data[13])
    # transcript.append(report_data[14])
    # peptide.append(report_data[15])

gene_id_list_no = []
annotated = []


for x in range(len(gene_id)):
    if sprot_Top_BLASTP_hit[x] != '.':
        annotated.append(gene_id[x])
    #elif sprot_Top_BLASTP_hit[x] != '.':
    #    annotated.append(gene_id[x])
    else:
        gene_id_list_no.append(gene_id[x])


gene_count = list(gene_id_list_no)
annotated = set(annotated)

for y in range(len(gene_count)):
    if gene_count[y] in annotated:
        gene_name = gene_count[y]
        gene_id_list_no.remove(gene_name)

print('No annotation:', len(set(gene_id_list_no)))
print('annotated:', len(set(annotated)))
print('all:', len(set(gene_id)))

