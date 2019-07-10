#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:51:45 2019

@author: lavanyasingh
"""

import csv
import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')
import helpers


def read_in(path):
    sources = []
    total, uq = 0, 0
    with open(path, 'r', errors = 'ignore') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for line in reader:
            total += 1
            row = ['United States', helpers.truncate(line[3]), line[2], 'English', 'Newspaper', line[4],
                   line[0], line[1], line[7]]
            if row not in sources: 
                uq += 1
                sources.append(row)
    print ('total', total)
    print ('unique', uq)
    return sources
    
def write_out(path_out):
    sources = read_in('data/usnpl_wiki_list.csv')
    with open(path_out, mode = 'w') as f:
        count = 0
        w = csv.writer(f, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type', 'wikipedia title', 'state', 'town', 'wikipedia link'])
        for entry in sources:
            count+=1
            w.writerow(['', entry, '', '', '', '', '', ''])
    return count

write_out('data/usnpl.csv')