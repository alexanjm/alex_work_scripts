#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: May 31, 2017


input_file = '/Users/jonesalm/Documents/playground/regen_hydractinia_related/annotation/hydra_blast_sofia/transdecoder_Hech_hydraNR.results'
with open(input_file, 'r') as ifile:
    for line in ifile:
        line = line.rstrip('\n')
        elements = line.split('\t')
        print(elements[0])