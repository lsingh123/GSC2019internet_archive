#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 14:14:37 2019

@author: lavanyasingh
"""

import csv 
import os

os.getcwd()
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data')

# a manual workaround while I figure out the google sheets API

def read_wd_sources(path):
    sources = []
    with open(path, 'r', errors = 'ignore') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for line in reader:
            sources.append({'country':line[0], 'url': line[1]})
    return sources

def remove_overlaps(old_urls, new):
    for source in new:
        if source['url'] in old_urls:
            new.remove(source)
    return new

def get_old(path):
    urls = []
    with open(path, 'r', errors = 'ignore') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for line in reader:
            urls.append(line[2])
    return urls

def write_sources(path):
    sources = remove_overlaps(get_old('ia_sources.csv'), read_wd_sources('wd_sources.csv'))
    count = 0
    with open(path, 'w') as f:
        w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url'])
        for source in sources:
            count +=1
            w.writerow([source['country'], source['url']])
    print(count)

write_sources('wd_sources_overlaps_removed.csv')