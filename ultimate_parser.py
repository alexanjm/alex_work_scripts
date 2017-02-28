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
    parser.add_argument('-id', '--in_delim', help='input delimiter')
    parser.add_argument('-od', '--out_delim', help='output delimiter')
    parser.add_argument('-s', '--sort', help='sort column <#> by <method> (ascending, descending, alphabetical')
    parser.add_argument('-o', '--out_file', help='output file')
    parser.add_argument('-c', '--column', help='columns #s (1-?) to write to output')
    parser.add_argument('-hd', '--header', default='y', help='header? <y or n>')
    in_args = parser.parse_args()

    with open(in_args.input_file, 'r') as ifile:
        first_line = ifile.readline()
        print('arg', in_args.in_delim)
        if in_args.in_delim is None:
            print('None')
            if '\t' in first_line:
                delim_str = '\t'
            else:
                delim_str = ','
        else:
            print('some')
            if in_args.in_delim == 't':
                delim_str = '\t'
            else:
                delim_str = ','
        print('delimiter', delim_str)
        num_dels = first_line.count(delim_str)
    ifile.close()
    # print('delimiter is', delim_str)

    if in_args.header == 'y':
        first_line = first_line.split(delim_str)
        # print(first_line)
        for i in range(num_dels + 1):
            exec("col%d = []" % (i + 1))

        with open(in_args.input_file, 'r') as ifile:
            for line in ifile:
                line = line.rstrip('\n').split(delim_str)
                # print('line', line)
                for i in range(num_dels + 1):
                    exec("col%d.append(line[%d])" % (i + 1, i))
                    # print('i is:', i)

    if in_args.out_file is True:
        ofile_name = in_args.out_file
    else:
        ofile_name = in_args.input_file + '.parsed'
    print(ofile_name)
    out_str = ''
    with open(ofile_name, 'w') as ofile:
        for x in range(len(col1)):
            # print(col1[x])
            # out_str = ''
            for y in range(1, num_dels+2):
                exec("a = col{0}".format(y))
                if delim_str == '\t':
                    out_delim = ','
                else:
                    out_delim = '\t'
                # print('out delimiter', out_delim)
                out_str_col = '%s' % (a[x])
                out_str_delim = out_str_col + out_delim
                # print(out_str_delim)
                if y < (num_dels + 1):
                    out_str = out_str + out_str_delim
                    # print('one', out_str)
                else:
                    out_str = out_str + out_str_delim.rstrip(out_delim) + '\n'
                    # print('two', out_str)
        # this is final output in tabular form -- still need to re-put headers
        print(out_str)
        ofile.write(out_str)
