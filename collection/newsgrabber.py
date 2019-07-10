#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 12:05:57 2019

@author: lavanyasingh
"""

import os 
import csv
import helpers
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data/')

pref = '/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data/services'
paths = os.listdir(pref)

def get_sources():
    with open('newsgrabber_sources.csv', 
              'w', errors = 'ignore') as outf:
        w = csv.writer(outf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type'])
        sources = []
        for path in paths:
            with open(pref + '/' + path, 'r', errors = 'ignore') as inf:
                count = 0
                while count < 4:
                    count += 1
                    line = inf.readline()
                    if not line: break
                url = line.split('\'')[1]
                sources.append(url)
        return sources

def write_to_csv():
    sources = get_sources()
    with open('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data/newsgrabber_sources.csv', 
              'w', errors = 'ignore') as outf:
        w = csv.writer(outf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type'])
        for source in sources:
            print(helpers.truncate(source))
            w.writerow(['none' if i != 2 else helpers.truncate(source) for i in range(5)])

if __name__ == '__main__':
    write_to_csv()
    print('hi')
                   

