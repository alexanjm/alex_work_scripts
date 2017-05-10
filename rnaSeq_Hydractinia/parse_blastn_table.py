#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on: Oct 24 2016

#########
# GOAL: Parse overrepresented file data to find files that do and do not have rRNA or ribosomal in their description
#
# Input: Blast table
# python3 parse_blastn_table.py input_file 'terms'
#####


import os
import sys
import argparse
import re
from Bio import SeqIO

# renamed argument_array
args = sys.argv
parser = argparse.ArgumentParser(description='GOAL: Parse overrepresented file data to find files that contain or do '
                                             'not contain certain terms (that do and do not contain rRNA or ribosomal '
                                             'in their description). Please add input file and terms to be searched')
parser.add_argument('input_file', help='file you want to search from--blastn outfmt -7')
parser.add_argument('-over', '--overrep_seqs_list', help='file containing concatenated list of overrepresented sequences')
in_args = parser.parse_args()

# tabular file created from blastn with the following command:
# qsub -cwd -N fmt7 -V -b y
# blastn -task blastn
# -evalue 0.1
# -num_alignments 3
# -outfmt \"7 qseqid sseqid stitle pident qlen length qstart qend evalue start send\"
# -out all_seq_fmt7_blastn.txt
# -query all_over_represented.fa
# -db /data/projects/barreira/alex/DB/nt


########################################################################################################################
# Sort files into files_with_rRNA, files_no_rRNA, and master_list of all over-represented files
# Input: all_seq_fmt7_blastn.txt --- output from blastn
# Output: files_with_rRNA, files_no_rRNA, master_list
# Output: blast_summary <directory> files
#
# input_file = '/Users/jonesalm/Documents/playground/rna_2016/all_seq_fmt7_blastn.txt'

files_with_rRNA = []
files_no_rRNA = []
master_list = []
infile = open(in_args.input_file, 'r')
# iterate through each line of the blastn table file
for line in infile:
    # Search for lines that start with '# Query: FILENAME'
    if line.startswith('# Query:'):
        line = line.strip('\n')
        master_name = line.split(': ')[1]
        master_list.append(master_name)
    # if the line doesn't start with a '#' it is a blastn hit in tabular form
    if not line.startswith('#'):
        line = line.strip('\n')
        element_list = line.split('\t')
        # test if anything in the sequence alignment description matches 'ribosomal' or 'rRNA' & add to list accordingly
        if bool(re.search('rRNA', element_list[2])) or bool((re.search('ribosomal', element_list[2]))):
            # if match, append sequence name to files with rRNA in description
            files_with_rRNA.append(master_name)
            if master_name in files_no_rRNA:
                # if the sequence name exists in files_no_rRNA, then remove it from the list, because a match for
                # rRNA/ribosomal was found
                files_no_rRNA.remove(master_name)
        else:
            # If there is no match for rRNA or ribosomal in sequence subject then add the sequence name to files_no_rRNA
            files_no_rRNA.append(master_name)
            # Check to make sure if a seq file has rRNA, then it is not included in the files_no_rRNA
            if master_name in files_with_rRNA:
                files_no_rRNA.remove(master_name)


########################################################################################################################
# Adapted from: /home/klasfeldsj/scripts/reverse-compliment.py
# Get reverse compliments of each unique overrepresented sequence
# Input: uniq_list.fa
# Output: uniq_rc.fa
#
all_overrep_rc = open('all_overrep_rc.fa', 'w')
# SeqIO parses each sequence record in fasta format and writes the reverse complement to uniq_rc.fa
for seq_record in SeqIO.parse(in_args.overrep_seqs_list, "fasta"):
    my_seq = seq_record.seq
    rc_string = ">%s_reverse-compliment\n%s\n" % (seq_record.id, my_seq.reverse_complement())
    all_overrep_rc.write(rc_string)
    # print(">%s_reverse-compliment" % (seq_record.id))
    # print(my_seq.reverse_complement())
all_overrep_rc.close()


########################################################################################################################
# Concatenate all_over_represented.fa and all_overrep_rc.fa
# Input: all_over_represented.fa, all_overrep_rc.fa
# Output: all_seqs_with_rc.fa
#
file_names = ['all_over_represented.fa', 'all_overrep_rc.fa']
with open('all_seqs_with_rc.fa', 'w') as outfile:
    # for each file in the list of files
    for fname in file_names:
        # open current file as infile
        with open(fname) as infile:
            # for each line in the file write the contents to the output file
            for line in infile:
                outfile.write(line)
outfile.close()


########################################################################################################################
# Create dictionary for all overrepresented files
# Input: all_over_represented.fa
# Output: all_files <class 'dict'>
#
# create a dictionary containing sequence names as keys and their respective sequences as their values.
all_files = {}
# all_over_represented = open('/Users/jonesalm/Documents/playground/rna_2016/all_over_represented.fa')
all_over_represented_with_rc = open('all_seqs_with_rc.fa', 'r')

# line counter -- starts as an even # (name of the sequence) -- odd #'s (sent to the else statement) append seq to
# its corresponding name
counter = 1
# iterate over all lines in all_over_represented.fa -- MUST BE IN THE SAME DIRECTORY TO RUN THIS SCRIPT
for line in all_over_represented_with_rc:
    # strip end-of-line character
    line = line.strip('\n')
    counter += 1
    # if line counter is even, add the name of the sequence with blank string
    if counter % 2 == 0:
        seq_name = line
        all_files[seq_name] = ''
    # else add the sequence to its preceeding seq name
    else:
        all_files[seq_name] = line


########################################################################################################################
# Adapted from /home/klasfeldsj/scripts/remove_redundant.py
# Remove redundant sequences
# Input: all_files <class 'dict'>
# Output: uniq_list.fa, discard_list.fa
#
# dictionary of unique sequences
orig = {}
# write list of discarded files
d = open('discard_list.fa', 'w')
# write list of unique sequences
uniq = open('uniq_list_with_rc.fa', 'w')
# iterate through each key in the all_files dictionary
for key in all_files:
    # if the value of 'key' in all_files is in the list of values in the dictionary orig....write the file name
    # and sequence to the discard list, as this particular overrepresented sequence is already
    # accounted for by another file
    if all_files[key] in orig.values():
        string_discard = '%s\n%s\n' % (key, all_files[key])
        d.write(string_discard)
    # if the value of key in all_files is not present in the orig dictionary, write the file name and
    # corresponding sequence to the file of unique sequences for trimmomatic
    else:
        orig[key] = all_files[key]
        string_uniq = '%s\n%s\n' % (key, all_files[key])
        uniq.write(string_uniq)
d.close()
uniq.close()


########################################################################################################################
# Used these files to check that totals of each over represented seq type were adding up
# Gives you quick access to file names for adapters, rRNA, and files that received no hits in blast
# Category file counts shows the # of each file type to assure totals add up
#

if not os.path.exists('blast_summary'):
    os.makedirs('blast_summary')

# get the set of all the file names
master_list = set(master_list)
rRNA_set = set(files_with_rRNA)
no_rRNA_set = set(files_no_rRNA)

hit_set = rRNA_set.union(no_rRNA_set)
zero_hits = master_list.difference(hit_set)

with open('blast_summary/all_rRNA.txt', 'w') as f1:
    for x in rRNA_set:
        string1 = '%s\n' % x
        f1.write(string1)
f1.close()

with open('blast_summary/all_no_rRNA.txt', 'w') as f2:
    for y in no_rRNA_set:
        string2 = '%s\n' % y
        f2.write(string2)
f2.close()

with open('blast_summary/all_no_hits.txt', 'w') as f3:
    for z in zero_hits:
        string3 = '%s\n' % z
        f3.write(string3)
f3.close()

# This should probably just be a test
num_rRNA = len(rRNA_set)
num_no_rRNA = len(no_rRNA_set)
num_zero = len(zero_hits)
num_seqs_rep = num_no_rRNA + num_rRNA + num_zero
num_total_seqs = len(master_list)

with open('blast_summary/category_file_counts.txt', 'w') as f4:
    f4.write('Overrepresented Seq Type\tNumber of Seqs\n')
    string4 = 'rRNA (No Hit)\t%d\nTruSeq Adapter/Illumina PCR\t%d\nNo blastn hits\t%d\n\nNumber ' \
              'of files represented\t%d\nTotal number of files\t%d\n'\
              % (num_rRNA, num_no_rRNA, num_zero, num_seqs_rep, num_total_seqs)
    f4.write(string4)
f4.close()
