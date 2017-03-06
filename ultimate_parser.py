#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: Feb 27, 2017

# import os
import sys
import argparse


def get_delimiter():
    with open(in_args.input_file, 'r') as ifile:
        first_line = ifile.readline()
        #print('arg', in_args.in_delim)
        if in_args.in_delim is None:
            if '\t' in first_line:
                delim_str = '\t'
            else:
                delim_str = ','
        else:
            if in_args.in_delim == 't':
                delim_str = '\t'
            else:
                delim_str = ','
        #print('delimiter', delim_str)
        num_dels = first_line.count(delim_str)
    ifile.close()
    return delim_str, num_dels


def out_file_name():
    if in_args.out_file is True:
        out_file_name = in_args.out_file
    else:
        out_file_name = in_args.input_file + '.parsed'
    print(out_file_name)
    return out_file_name


def get_num_cols():
    col_name_list = []
    for i in range(num_dels + 1):
        list_str = "col{0}".format(i + 1)
        #print('list', list_str)
        list_str = []
        col_name_list.append(list_str)
    return col_name_list


def read_infile():
    with open(in_args.input_file, 'r') as ifile:
        for line in ifile:
            line = line.rstrip('\n').split(delim_str)
            for i in range(num_dels + 1):
                cols[i].append(line[i])
    return cols


def write_outfile(columns):
    out_str = ''
    with open(ofile_name, 'w') as ofile:
        i = 0
        for x in range(len(cols[0])):
            # print(col1[x])
            # out_str = ''
            if columns != None:
                #print('whatttt', columns)
                column_nums = columns.strip().split(',')
                #print('?', column_nums[0])
            else:
                column_nums = range(num_dels + 1)
            #print('dels', num_dels)
            #print('cols', len(column_nums))
            for y in column_nums:
                y = int(y) - 1
                if in_args.parse is False:
                    out_delim = delim_str
                else:
                    if in_args.in_delim is None:
                        if delim_str == '\t':
                            out_delim = ','
                        else:
                            out_delim = '\t'
                    else:
                        if in_args.in_delim == 't':
                            out_delim = ','
                        else:
                            out_delim = '\t'
                # print('out delimiter', out_delim)
                out_str_col = '%s' % (cols[y][x])
                out_str_delim = out_str_col + out_delim
                # print(out_str_delim)
                if i < len(column_nums) - 1:
                    print('num_test', len(column_nums)-1)
                    print('i_test', i)
                    i += 1
                    out_str += out_str_delim
                    # print('one', out_str)
                else:
                    out_str += out_str_delim.rstrip(out_delim) + '\n'
                    i = 0
                    # print('two', out_str)
        # this is final output in tabular form -- still need to re-put headers
        print(out_str)
        ofile.write(out_str)


if __name__ == '__main__':
    args = sys.argv
    parser = argparse.ArgumentParser(description='GOAL: Parse anything and everything however you would like')
    parser.add_argument('input_file', help='transdecoder file')
    parser.add_argument('-d', '--in_delim', help='input delimiter')
    #still need sort functionality
    parser.add_argument('-s', '--sort', help='sort column <#> by <method> (ascending, descending, alphabetical')
    #outfile functionality? not sure
    parser.add_argument('-o', '--out_file', help='output file')
    parser.add_argument('-c', '--column', help='columns #s (1-?) to write to output')
    # still no header functionality
    parser.add_argument('-hd', '--header', default='y', help='header? <y or n>')
    parser.add_argument('-p', '--parse', help='parse -- convert delimiter', action='store_true')
    in_args = parser.parse_args()

    delim_str, num_dels = get_delimiter()
    #print('dels', num_dels)

    cols = get_num_cols()
    #print('cols', cols)

    cols_list = read_infile()
    #print('cols list', cols_list)

    ofile_name = out_file_name()

    write_outfile(in_args.column)


    print('true', in_args.column)
    print(in_args.parse)


