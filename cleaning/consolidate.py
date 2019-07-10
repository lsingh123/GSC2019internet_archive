#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 12:04:29 2019

@author: lavanyasingh
"""

import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')

import csv
import helpers

def get_meta(path):
    pieces = path.split('_')
    return pieces[0]

def get_sources():
    sources = {}
    pref = '/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data/cleaned'
    paths = os.listdir(pref)
    paths.remove('.DS_Store')
    for path in paths:
        total =  0
        with open('data/cleaned/' + path, 'r') as inf:
            reader = csv.reader(inf, delimiter=',')
            next(reader)
            for item in reader:
                if item[1].find('subject=') != -1:
                    None 
                else:
                    total += 1
                    url = helpers.truncate(item[1])
                    item[1] = url
                    val = check_sources(list(sources.keys()), url, path)
                    if val != -1:
                        for i in range(len(item)):
                            if not helpers.is_bad(item[i]):
                                sources[val][i] = item[i]
                        if len(url) < len(val): sources[val][1] = url
                    else:
                        item += ['' for i in range(10)]
                        if (item[0] == "United States" or
                        item[0].lower() == "us" or item[0].lower() == "usa") : 
                            item[0] == "United States of America"
                        if path != 'sheet_cleaned.csv': 
                            item[7] = get_meta(path)
                        sources.update({url: item})
                if total % 2500 == 0: print(path, total)
        print(path, total)
    return sources

def check_sources(sources, url, path):
    if url in sources: 
        return url
    pieces_u = url.split('.')
    if len(pieces_u) < 3: return -1
    for item in sources:
        pieces_i = item.split('.')
        overlap, out = [], []
        for i in range(len(pieces_i)):
            if pieces_i[i] == pieces_u[i]: 
                overlap.append(i)
            else:
                out.append(i)
            if len(out) == 1:
                try:
                    int(out[0])
                    return -1
                except:
                    return item
    return -1
            
def write_all():
    sources = get_sources()
    total = 0
    with open('data/cleaned/all.csv', 'w') as outf:
        w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type', 'title native language',
                    'paywall', 'metasource', 'state', 'town', 'wikipedia name', 'redirects?',
                    'wikipedia link'])
        for item in sources.values():
            total += 1
            w.writerow(item)
        if total % 5000 == 0: print('spot', item)
    print("ALL", total)


write_all()