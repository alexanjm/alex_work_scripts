#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: Feb 27, 2017

# import os
import sys
import argparse

# test_c = 3
# for x in range(test_c):
#     list_name = str(x)
#     list_name = []
#     print(list_name)
# one.append('alex')
# print(one)

# for x in cols:
#     print(x)
#     x = []
#     print(x)
#     x.append('yay')


if __name__ == '__main__':
    args = sys.argv
    parser = argparse.ArgumentParser(description='GOAL: Parse anything and everything however you would like')
    parser.add_argument('input_file', help='transdecoder file')
    parser.add_argument('-id', '--in_delim', default='c', help='input delimiter')
    parser.add_argument('-od', '--out_delim', default='t', help='output delimiter')
    parser.add_argument('-s', '--sort', help='sort column <#> by <method> (ascending, descending, alphabetical')
    parser.add_argument('-o', '--out_file', help='output file')
    parser.add_argument('-c', '--column', help='columns #s (1-?) to write to output')
    parser.add_argument('-hd', '--header', default='y', help='header? <y or n>')
    in_args = parser.parse_args()

    with open(in_args.input_file, 'r') as ifile:
        first_line = ifile.readline()
        print(first_line)
        if in_args.in_delim == 't':
            delim_str = '\t'
        else:
            delim_str = ','
        num_dels = first_line.count(delim_str)

        if in_args.header == 'y':
            first_line = first_line.split(delim_str)
            for i in range(num_dels + 1):
                exec("col%d = []" % (i + 1))
            print(col1)
            print(col2)
            print(col3)
            print(col4)
            for line in ifile:
                line = line.rstrip('\n').split(delim_str)
                for i in range(num_dels + 1):
                    exec("col%d.append(line[%d])" % (i + 1, i))
    print(col1)
    print(col2)
    print(col3)
    print(col4)
    if in_args.out_file == True:
        ofile_name = in_args.out_file
    else:
        ofile_name = in_args.input_file + '.parsed'
    print(ofile_name)
    with open(ofile_name, 'w') as ofile:
        for x in range(len(col1)):
            print(col1[x])
            out_str = '%s\t%s\t%s\t%s\n' % (col1[x], col2[x], col3[x], col4[x])
            ofile.write(out_str)







