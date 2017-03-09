#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on: Mar 6, 2017

from alex_work_scripts import ultimate_parser
import pytest
# import os
import sys


def test_delimiters():
    out1 = ultimate_parser.get_delimiter('tests/test_commas.txt', None)
    out2 = ultimate_parser.get_delimiter('tests/test_tabs.txt', None)
    print(out1)
    print(out2)
    output = [out1[0], out2[0]]
    result = [',', '\t']

    assert output == result


def test_manual_delimiter1():
    output = ultimate_parser.get_delimiter('tests/test_commas.txt', ',')

    assert output[0] == ','


def test_manual_delimiter2():
    output = ultimate_parser.get_delimiter('tests/test_tabs.txt', '\t')

    assert output[0] == '\t'


def test_ofile_name_default():
    infile = 'tests/test_commas.txt'
    out_name = ultimate_parser.get_out_file_name(infile, None, True, None)
    result = infile + '.parsed'

    assert out_name == result


def test_ofile_name_input():
    infile = 'tests/test_commas.txt'
    ofile = 'tests/this_is_a_test.txt'
    out_name = ultimate_parser.get_out_file_name(infile, ofile, True, None)

    assert out_name == ofile


def test_get_num_cols():
    number_delims = 2
    output = ultimate_parser.get_num_cols(number_delims)
    result = [[], [], []]
    assert output == result


def test_read_infile():
    column_contents = ultimate_parser.read_infile('tests/test_commas.txt', ',', 2, [[], [], []], 0)
    result = [['alex', '1', '4'], ['ryan', '2', '5'], ['kimani', '3', '6']]

    assert column_contents == result


def test_write_outfile():
    ofile = 'tests/test_commas.txt.parsed'
    cols_list = [['alex', '1', '4'], ['ryan', '2', '5'], ['kimani', '3', '6']]
    output = ultimate_parser.write_outfile(None, ofile, cols_list, 2, True, ',', None, None)
    result = ['alex\tryan\tkimani', '1\t2\t3', '4\t5\t6']
    lines = []
    with open(output, 'r') as ofile:
        for line in ofile:
            line = line.strip('\n')
            lines.append(line)

    assert lines == result


def test_write_outfile_input_delims_columns_parse():
    ofile = 'tests/test_commas.txt.parsed'
    cols_list = [['alex', '1', '4'], ['ryan', '2', '5'], ['kimani', '3', '6']]
    output = ultimate_parser.write_outfile('3,1', ofile, cols_list, 2, True, ',', None, None)
    result = ['kimani\talex', '3\t1', '6\t4']
    lines = []
    with open(output, 'r') as ofile:
        for line in ofile:
            line = line.strip('\n')
            lines.append(line)

    assert lines == result


def test_sort_ascending_no_header():
    transposed_list = [['alex', '1', '1'], ['zeke', '291', '-9'], ['peter', '12', '92'], ['kimani', '2', '-4']]
    sort_input = [3, False]

    sorted_list = [['zeke', 291.0, -9.0], ['kimani', 2.0, -4.0], ['alex', 1.0, 1.0], ['peter', 12.0, 92.0]]
    output = ultimate_parser.sort_file(transposed_list, sort_input)

    assert sorted_list == output


def test_diff_col_nums():
    delimiter_string, number_delimiters, diff_columns = ultimate_parser.get_delimiter('tests/bad_header.txt', None)

    assert diff_columns == -1

    column_contents_list = ultimate_parser.read_infile('tests/bad_header.txt', '\t', 2, [[], [], []], diff_columns)

    result = [['Column Name', 'alex', 'ryan', 'kimani'], ['age', '24', '22', '23'], ['weight', '195', '190', '160']]

    assert column_contents_list == result


def test_main(monkeypatch):
    monkeypatch.setattr(sys, "argv", ['ultimate_parser', 'tests/sorted_test_header.txt', '-p', '-hd', '-sd', '3'])
    ofile = ultimate_parser.main()
    o_name = 'tests/sorted_test_header.txt' + '.parsed' + '.sorted'

    assert ofile == o_name

    result = ['one,two,three', 'peter,12.0,92.0', 'alex,1.0,1.0', 'kimani,2.0,-4.0', 'zeke,291.0,-9.0']
    lines = []
    results = []
    with open(o_name, 'r') as ofile:
        for line in ofile:
            line = line.strip('\n')
            lines.append(line)
    for x in result:
        results.append(x)

    assert lines == results


