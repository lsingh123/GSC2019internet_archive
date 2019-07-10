#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 10:09:53 2019

@author: lavanyasingh
"""

import os 
import csv

pref = '/Users/lavanyasingh/Downloads/archive_org-news-dump'
paths = os.listdir(pref)

def get_sources():
    with open('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data/ds_sources.csv', 
              'w', errors = 'ignore') as outf:
        w = csv.writer(outf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type'])
        sources = []
        count = 0
        uq = 0 
        for path in paths:
            print('path', path)
            with open(pref + '/' + path, 'r') as inf:
                while True:
                    line = inf.readline()
                    if not line: break
                    count += 1
                    if line not in sources:
                        w.writerow(['None', line, 'None', 'None', 'None'])
                        sources.append(line)
                        uq +=1
                        
    print('total', count)
    print('deduped', uq)


if __name__ == '__main__':
    get_sources()
                    
            
                    
        