#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 10:21:23 2019

@author: lavanyasingh
"""

import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')
import helpers
import csv

def read_cc():
    with open("data/common_crawl.txt", "r") as f:
        sources = set()
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            sources.add(line[1])
    print("CC", len(sources))
    return sources

def read_all():
    sources = []
    with open("data/raw/all_raw_cleaned3.csv", "r") as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            sources.append(line[1])
    print(len(sources))
    return sources

def remove_dups():
    cc = read_cc()
    sources = set(read_all())
    old = len(sources)
    sources |= cc
    print("UQ", len(sources)-old)
    '''
    unique = []
    for el in cc:
        if el not in sources:
            unique.append(el)
    print("DEDUPED", len(unique))'''

remove_dups()