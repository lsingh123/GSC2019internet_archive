#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 17:12:07 2019

@author: lavanyasingh
"""

import csv
import os
os.chdir("/Users/lavanyasingh/Desktop/GSC2O19internet_archive/")

def read_in():
    sources = []
    total = 0
    with open("data/raw/codes3.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            sources.append((line[0], line[1]))
    print("DONE READING")
    return sources

def analyze(sources):
    codes = {}
    for source in sources:
        if source[1] in codes:
            codes[source[1]]+= 1
        else:
            codes.update({source[1]:1})
    return codes

def write_analysis(sources):
    results = {}
    total, uq = 0, 0
    for source in sources:
        total += 1
        code = source[1]
        try:
            code = int(code)
            if code < 400:
                uq += 1
                results.update({source[0]:code})
        except ValueError:
            results.update({source[0]:"BROKEN"})
    print(total, uq)
    return results

res = write_analysis(read_in())

def write_results():
    with open('data/raw/working_urls.csv', 'w') as outf:
        w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for url in res:
            w.writerow([url, res[url]])
    print("DONE WRITING")

write_results()