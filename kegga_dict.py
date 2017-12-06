#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: June 6th, 2017


# GOAL ###


import argparse


def kegga_dict(id_dict_file):
    id_dict = {}

    with open(id_dict_file, 'r') as ifile:
        for line in ifile:
            elements = line.strip('\n').split(',')
            id_dict[elements[0]] = elements[1]
            print(elements[1])
    print(id_dict)
    print(len(id_dict.keys()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('in_file', help='Input file 1')

    in_args = parser.parse_args()

    kegga_dict(in_args.in_file)