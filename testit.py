#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: Feb 27, 2017

col_list = []
for i in range(10):
    #list_str = "a.%d = ['alex']" % i
    #exec("a.%d = ['alex']" % i)

    #print(a)

    #exec("list_str%s = []" % (i))
    a = "col{0}".format(i + 1)
    print(a)
    a = []
    col_list.append(a)
    print(col_list)


