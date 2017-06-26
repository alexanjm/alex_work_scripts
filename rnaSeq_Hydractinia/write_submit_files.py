#!/bin/env python

with open('file_names.txt', 'r') as ifile:
    for i in ifile:
        i = i.strip('\n')
        print(i)
        ofile = '%s.protein_lookup.sh' % i
        with open(ofile, 'w') as of:
            of.write('#!/bin/sh\n'
                        '# protein_lookup.sh\n'
                        '#$ -N protein_lookup\n'
                        '#$ -M alexander.jones@nih.gov\n'
                        '#$ -m abes\n'
                        '#$ -j y\n'
                        '#$ -w e\n'
                        '#$ -cwd\n\n')
            o_str1 = 'for seq in $( cat %s ); do\n' % i
            o_str2 = '\tgrep "$seq" -m 1 /data/projects/MMSeqs2DB/nr_1-31-17/nr.lookup | cut -f1 | (read line_num; ' \
                     'sed "${line_num}q;d" /data/projects/MMSeqs2DB/nr_1-31-17/nr_h) >> proteins.%s.txt\n' % i
            o_str3 = 'done\n'
            of.write(o_str1)
            of.write(o_str2)
            of.write(o_str3)
        of.close()



