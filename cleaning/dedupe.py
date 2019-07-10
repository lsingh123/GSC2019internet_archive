#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 11:59:11 2019

@author: lavanyasingh
"""

import csv
import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')
import helpers


def dedupe(path_in, path_out):
    sources = helpers.read_list(path_in)
    with open(path_out, mode = 'w') as f:
        count = 0
        w = csv.writer(f, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type'])
        for entry in sources:
            count+=1
            w.writerow(['', entry, '', '', ''])
    return count
    
#dedupe('data/newscrawls_urls', 'data/newscrawls_urls_cleaned.csv')

