#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 14:35:37 2019

@author: lavanyasingh
"""


import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')

import csv
import helpers

def get_dmoz():
    with open('data/dmoz_links_by_category.txt', 'r') as inf:
        reader = csv.reader(inf, delimiter='\t')
        with open('data/raw/dmoz_processed.csv', 'w') as outf:
            w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for line in reader:
                row = ['', line[1], '', '', '', '', '', "dmoz"]
                w.writerow(row + ['' for n in range(10)])        
            

get_dmoz()