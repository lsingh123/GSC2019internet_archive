#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 11:07:05 2019

@author: lavanyasingh
"""

# consolidate all the current data into a single deduped, cleaned CSV
# goal is to push from that CSV to fuseki

import os
import csv
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive')
import helpers



def write_cleaned(pathin, pathout):
    #sources = helpers.read_sources(pathin)
    #sources = read_usnpl()
    sources = read_us()
    with open(pathout, 'w') as f:
        w = csv.writer(f, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type', 'title native language',
                    'paywall', 'metasource', 'state', 'town', 'wikipedia name', 'redirects?',
                    'wikipedia link'])
        for item in sources:
            w.writerow(item)

def read_lion():
    sources, urls = [], []
    total, uq = 0, 0
    with open('data/lion.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            url = helpers.truncate(line[1])
            print(url)
            if url not in urls:
                uq += 1
                urls.append(url)
                sources.append(['United States', url, line[0], 'English', 'Newspaper', line[0], '',
                               'lion', line[5], line[4], '', '', ''])
        print(total, uq)
        return sources

#reads in from a text file of URLS and returns a cleaned and deduped list of CSV ROWS
def read_in(path):
    sources = []
    total, uq = 0, 0
    with open(path, 'r', errors = 'ignore') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            row = ['', helpers.truncate(line[0]), '', '', '', '', '', '', '', '', '', '']
            if row not in sources: 
                uq += 1
                sources.append(row)
            if total % 1000 == 0: print(helpers.truncate(line[0]))
    print (path, total, uq)
    return sources

def read_us():
    sources, urls = [], []
    total, uq = 0, 0
    with open('data/us_news.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            url = helpers.truncate(line[2])
            print(url)
            if url not in urls:
                uq += 1
                urls.append(url)
                sources.append(['United States', url, line[1], 'English', line[3], line[1], '',
                               'original', line[0], '', '', '', ''])
        print(total, uq)
        return sources

write_cleaned('data/gdelt', 'data/cleaned/us_news_cleaned.csv')


def read_usnpl():
    sources, urls = [], []
    total, uq = 0, 0
    with open('data/usnpl_wiki_list.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            url = helpers.truncate(line[3])
            if total % 1000 == 0: print(url)
            if url not in urls:
                uq += 1
                urls.append(url)
                # additional entries: [state, town, wikipedia name, redirects?(Y/N), wikipedia link]
                sources.append(['United States', url, line[2], 'English', 'Newspaper', line[2], '',
                               'USNPL', line[0], line[1], line[4], line[6], line[7]])
        print (total, uq)
        return sources



def sheet_sources():
    sources = []
    with open('data/sheet_raw.csv', 'r', errors = 'ignore') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for line in reader:
            row = [line[7], line[2], line[0], line[6], line[3], line[1], line[4], line[5], "", "", "", "", ""]
            sources.append(row)
    with open('data/cleaned/sheet_cleaned.csv', 'w') as f:
        w = csv.writer(f, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type', 'title native language',
                    'paywall', 'metasource', 'state', 'town', 'wikipedia name', 'redirects?',
                    'wikipedia link'])
        for item in sources:
            w.writerow(item)

