#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: Feb 27, 2017

# import os
# import sys
import argparse


# Get input/output delimiters
# Can sense if input delimiter is a tab or comma, otherwise will accept custom delimiters
def get_delimiter(in_file, in_delim):
    with open(in_file, 'r') as ifile:
        first_line = ifile.readline()
        second_line = ifile.readline()
        if in_delim is None:
            if '\t' in first_line:
                delim_str = '\t'
            else:
                delim_str = ','
        else:
            delim_str = in_delim
            delim_str = str(delim_str)

        num_dels = second_line.count(delim_str)
        first_length = len(first_line.split(delim_str))
        second_length = len(second_line.split(delim_str))
        diff = first_length - second_length
    ifile.close()
    return delim_str, num_dels, diff


# If outfile name given use that, otherwise, add .parsed or .sorted depending on actions
def get_out_file_name(in_file, out_file, parsed, is_sorted):
    out_file_name = in_file
    if out_file is not None:
        out_file_name = out_file
    else:
        if parsed is True:
            out_file_name += '.parsed'
        if is_sorted is not None:
            out_file_name += '.sorted'
        if parsed is False and is_sorted is None:
            out_file_name += '.parsed'

    return out_file_name


# Automatically calculate how many columns are in the input file
def get_num_cols(col_nums):
    col_name_list = []
    for i in range(col_nums + 1):
        list_str = "col{0}".format(i + 1)
        list_str = []
        col_name_list.append(list_str)
    return col_name_list

# Read input file
def read_infile(input_file, delim, col_nums, columns_list, diff):
    with open(input_file, 'r') as ifile:
        for line in ifile:
            line = line.rstrip('\n').split(delim)
            for i in range(col_nums + 1):
                try:
                    columns_list[i].append(line[i])
                except IndexError:
                    columns_list[i].append('Column Name')
    # It will do the following correction every time - however if 'Column Name' already exists at the front of the
    # file it will remain there -- can potentially put this into an if statement or if an error is raised
    if diff != 0:
        col_titles = []
        for x in columns_list:
            col_titles.append(x[0])
        idx = col_titles.index('Column Name')
        new_col_titles = col_titles[idx:] + col_titles[:idx]
        z = 0
        for y in columns_list:
            y[0] = new_col_titles[z]
            z += 1

    ifile.close()
    return columns_list


# Determines which method to sort by
def how_to_sort(asc, desc):
    sorting = [asc, desc]

    if sorting[1] is not None:
        sort_by = [sorting[1], True]
    elif sorting[0] is not None:
        sort_by = [sorting[0], False]
    else:
        sort_by = None

    return sort_by


# Data is read in by rows, this converts it to column contents
def transpose_list(column_list):
    transposed = [[column_list[j][i] for j in range(len(column_list))] for i in range(len(column_list[0]))]

    return transposed


# def remove_header(transposed_list, header):
#     if header is True:
#         header_line = transposed_list[0]
#         transposed_list.remove(header)
#
#         return transposed_list, header_line
#     else:
#         return transposed_list, None

#  Final function to call sorting function -- takes contents, sorting method and header as input
def sorting_commands(cols_contents, sorting_input, header_arg):
    transposed = transpose_list(cols_contents)
    if header_arg is True:
        header_line = transposed[0]
        transposed.remove(header_line)
        transposed_list_no_header = sort_file(transposed, sorting_input)
        transposed_list = [header_line] + transposed_list_no_header
    else:
        transposed_list = sort_file(transposed, sorting_input)

    cols_list = transpose_list(transposed_list)

    return cols_list


# Sorting function
def sort_file(column_lists, sort_input):
    for i in range(len(column_lists)):
        for j in range(len(column_lists[0])):
            number = column_lists[i][j]
            try:
                new_num = float(number)
                column_lists[i][j] = new_num
            except ValueError:
                pass

    col_sort = sort_input[0] - 1
    sort_method = sort_input[1]
    sorted_cols = sorted(column_lists, key=lambda my_sort_cols: my_sort_cols[col_sort], reverse=sort_method)

    return sorted_cols


# Write the new output file
def write_outfile(columns,  ofile_name, final_cols, num_dels, in_parse, delim_str, input_delim, output_delim):
    out_str = ''
    with open(ofile_name, 'w') as ofile:
        i = 0
        for x in range(len(final_cols[0])):
            if columns is not None:
                column_nums = columns.strip().split(',')
            else:
                column_nums = range(1, num_dels + 2)
            for y in column_nums:
                y = int(y) - 1
                if in_parse is False:
                    out_delim = delim_str
                elif output_delim is not None:
                    out_delim = output_delim
                elif input_delim is None and output_delim is None:
                    if delim_str == '\t':
                        out_delim = ','
                    else:
                        out_delim = '\t'
                else:
                    out_delim = '\t'
                out_str_col = '%s' % (final_cols[y][x])
                out_str_delim = out_str_col + out_delim
                if i < len(column_nums) - 1:
                    i += 1
                    out_str += out_str_delim
                else:
                    out_str += out_str_delim.rstrip(out_delim) + '\n'
                    i = 0
        ofile.write(out_str)
    ofile.close()
    return ofile_name


def main():
    # args = sys.argv
    parser = argparse.ArgumentParser(description='GOAL: Parse anything and everything however you would like')
    parser.add_argument('input_file', help='File to be parsed.')
    parser.add_argument('-p', '--parse', help='Convert files to comma separated, tab separated or even custom '
                                              'delimiters. Default = False', action='store_true')
    parser.add_argument('-hd', '--header',  help='<-hd> File contains a header?. Default = False.',
                        action='store_true')
    parser.add_argument('-c', '--column', help='<int,int(...)> Column numbers to output.')
    parser.add_argument('-sa', '--sort_asc', help='<int> Sort column in ascending order by this column number.',
                        type=int)
    parser.add_argument('-sd', '--sort_desc', help='<int> Sort column in descending order by this column number.',
                        type=int)
    # outfile functionality? not sure
    parser.add_argument('-o', '--out_file', help='Output file location.')
    parser.add_argument('-id', '--idel', help='<str> Custom input delimiter.', type=str)
    parser.add_argument('-od', '--odel', help='<str> Custom output delimiter.', type=str)
    in_args = parser.parse_args()

    delim_str, num_dels, diff_cols = get_delimiter(in_args.input_file, in_args.idel)

    empty_cols = get_num_cols(num_dels)

    cols_list = read_infile(in_args.input_file, delim_str, num_dels, empty_cols, diff_cols)

    sorting = how_to_sort(in_args.sort_asc, in_args.sort_desc)

    if sorting is not None:
        try:
            cols_list = sorting_commands(cols_list, sorting, in_args.header)
        except TypeError:
            print("ERROR: Do you need to specify this file has a header? --> use flag -hd")
            raise SystemExit

    ofile_name = get_out_file_name(in_args.input_file, in_args.out_file, in_args.parse, sorting)
    # Print in and out delimtiters to see if program is working correctly
    print('in', in_args.idel)
    print('out', in_args.odel)
    output = write_outfile(in_args.column, ofile_name, cols_list, num_dels, in_args.parse, delim_str, in_args.idel, in_args.odel)

    return output


if __name__ == '__main__':

    main_output = main()
    # print file name so user can see where the file is
    print(main_output)
