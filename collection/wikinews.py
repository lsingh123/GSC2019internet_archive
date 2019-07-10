#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:28:44 2019

@author: lavanyasingh
"""

import csv
import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')
import helpers

os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data')


def get_sources():
    sources = []
    path = 'quarry-36817-get-all-news-sources-from-enwikinews-run382005.csv'
    with open(path, 'r', errors = 'ignore') as f:
        reader = csv.reader(f, delimiter = ',')
        next(reader)
        for line in reader:
            sources.append(line[0])
    return sources


def explore():
    raw = get_sources()
    sources = []
    count = 0
    total = 0
    for item in raw:
        url = helpers.truncate(item)
        total +=1
        if (url.find('wiki') == -1 and url.find('twitter') == -1 and 
            url.find('facebook') == -1 and url.find('google') == -1
            and url.find('linkedin') == -1 and url.find('reddit') == -1):
            if url not in sources:
                print(url)
                sources.append(url)
                count +=1
    print ('total', total)
    print ('count', count)
    return sources

def write_to_csv():
    with open('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data/wn_sources.csv', 
              'w', errors = 'ignore') as outf:
        w = csv.writer(outf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type'])
        sources = explore()
        for source in sources:
            w.writerow(['none' if i != 1 else source for i in range(5)])
           

if __name__ == '__main__':
   explore()