#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: Feb 27, 2017

# import os
import sys
import argparse


def get_delimiter(in_file, in_delim):
    with open(in_file, 'r') as ifile:
        first_line = ifile.readline()
        second_line = ifile.readline()
        # first_length = len(first_line.split('\t'))
        # second_length = len(second_line.split('\t'))
        # print('arg', in_args.in_delim)
        if in_delim is None:
            if '\t' in first_line:
                delim_str = '\t'
            else:
                delim_str = ','
        else:
            if in_delim == 't':
                delim_str = '\t'
            else:
                delim_str = ','
        # print('delimiter', delim_str)
        num_dels = second_line.count(delim_str)
    ifile.close()
    return delim_str, num_dels


def get_out_file_name(in_file, out_file, parsed, sorted):
    out_file_name = in_file
    if out_file is not None:
        out_file_name = out_file
    else:
        if parsed is True:
            out_file_name = out_file_name + '.parsed'
        if sorted is not None:
            out_file_name = out_file_name + '.sorted'
        if parsed is False and sorted is None:
            out_file_name = out_file_name + '.out'

    return out_file_name


def get_num_cols(col_nums):
    col_name_list = []
    for i in range(col_nums + 1):
        list_str = "col{0}".format(i + 1)
        # print('list', list_str)
        list_str = []
        col_name_list.append(list_str)
    return col_name_list


def read_infile(input_file, delim, col_nums, columns_list):
    with open(input_file, 'r') as ifile:
        #print(col_nums)
        for line in ifile:
            line = line.rstrip('\n').split(delim)
            for i in range(col_nums + 1):
                try:
                    columns_list[i].append(line[i])
                except IndexError:
                    columns_list[i].append('Column Name')
    # It will do the following correction every time - however if 'Column Name' already exists at the front of the
    # file it will remain there -- can potentially put this into an if statement or if an error is raised
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

##make different input for different types of sorting -sort_asc -sort_desc -- easier
def sort_file(column_lists, sort_input):
    for i in range(len(column_lists)):
        for j in range(len(column_lists[0])):
            number = column_lists[i][j]
            try:
                new_num = float(number)
                column_lists[i][j] = new_num
            except ValueError:
                pass

    in_sort = sort_input.split(',')
    # try:
    col_sort = int(in_sort[0]) - 1
    # except ValueError:
    #     print("ERROR: Please se")
    sort_method = in_sort[1].strip()
    if sort_method == 'r':
        sorted_cols = sorted(column_lists, key=lambda my_sort_cols: my_sort_cols[col_sort], reverse=True)
    else:
        sorted_cols = sorted(column_lists, key=lambda my_sort_cols: my_sort_cols[col_sort])

    return sorted_cols


def write_outfile(columns,  ofile_name, final_cols, num_dels, in_parse, delim_str, input_delim):
    out_str = ''
    with open(ofile_name, 'w') as ofile:
        i = 0
        for x in range(len(final_cols[0])):
            # print(col1[x])
            # out_str = ''
            if columns is not None:
                # print('whatttt', columns)
                column_nums = columns.strip().split(',')
                # print('?', column_nums[0])
            else:
                column_nums = range(1, num_dels + 2)
            # print('dels', num_dels)
            # print('cols', len(column_nums))
            for y in column_nums:
                y = int(y) - 1
                if in_parse is False:
                    out_delim = delim_str
                else:
                    if input_delim is None:
                        if delim_str == '\t':
                            out_delim = ','
                        else:
                            out_delim = '\t'
                    else:
                        if input_delim == 't':
                            out_delim = ','
                        else:
                            out_delim = '\t'
                # print('out delimiter', out_delim)
                out_str_col = '%s' % (final_cols[y][x])
                out_str_delim = out_str_col + out_delim
                # print(out_str_delim)
                if i < len(column_nums) - 1:
                    # print('num_test', len(column_nums)-1)
                    # print('i_test', i)
                    i += 1
                    out_str += out_str_delim
                    # print('one', out_str)
                else:
                    out_str += out_str_delim.rstrip(out_delim) + '\n'
                    i = 0
                    # print('two', out_str)
        # this is final output in tabular form -- still need to re-put headers
        ofile.write(out_str)
    ofile.close()
    return ofile_name


def main():
    #args = sys.argv
    #print('these args', args)
    parser = argparse.ArgumentParser(description='GOAL: Parse anything and everything however you would like')
    parser.add_argument('input_file', help='transdecoder file')
    parser.add_argument('-d', '--in_delim', help='input delimiter')
    parser.add_argument('-sa', '--sort_asc', help='sort column <#> by ascending order (Default sort method)')
    parser.add_argument('-sd', '--sort_desc', help='sort column <#> by descending order')
    # outfile functionality? not sure
    parser.add_argument('-o', '--out_file', help='output file')
    parser.add_argument('-c', '--column', help='columns #s (1-?) to write to output')
    parser.add_argument('-hd', '--header',  help='-hd flag implies file has header -- default is no header',
                        action='store_true')
    parser.add_argument('-p', '--parse', help='parse -- convert delimiter', action='store_true')
    in_args = parser.parse_args()

    delim_str, num_dels = get_delimiter(in_args.input_file, in_args.in_delim)

    empty_cols = get_num_cols(num_dels)

    cols_list = read_infile(in_args.input_file, delim_str, num_dels, empty_cols)
    sorting = [in_args.sort_asc, in_args.sort_desc]

    if sorting[1] is not None:
        sort_by = '%s,r' % sorting[1]
    elif sorting[0] is not None:
        sort_by = '%s,a' % sorting[0]
    else:
        sort_by = None
    try:
        if sort_by is not None:
            transposed = transpose_list(cols_list)

            if in_args.header is True:
                header_line = transposed[0]
                transposed.remove(header_line)
                transposed_list_no_header = sort_file(transposed, sort_by)
                transposed_list = [header_line] + transposed_list_no_header
                # print(transposed_list)
            else:
                transposed_list = sort_file(transposed, sort_by)

            cols_list = transpose_list(transposed_list)

    except TypeError:
        print("ERROR: Do you need to specify this file has a header? --> use flag -hd")
        raise SystemExit

    ofile_name = get_out_file_name(in_args.input_file, in_args.out_file, in_args.parse, sort_by)

    output = write_outfile(in_args.column, ofile_name, cols_list, num_dels, in_args.parse, delim_str, in_args.in_delim)

    return output


if __name__ == '__main__':

    main_output = main()
    # return main_output
    print(main_output)
