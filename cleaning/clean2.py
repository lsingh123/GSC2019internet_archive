#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 10:08:08 2019

@author: lavanyasingh
"""


import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')
import csv
import re
import helpers
import tldextract

def clean(url):
    url = url.replace("www.", "")
    stream = re.finditer('%', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    stream = re.finditer('%', url)
    return url

def read_in():
    urls, rows, domains = [], [], []
    total, uq = 0, 0
    with open('data/raw/all_raw_cleaned2.csv', 'r') as inf:
        reader = csv.reader(inf, delimiter=',')
        for line in reader:
            total += 1
            url = clean(''.join(line[1]))
            o = tldextract.extract(url)
            domain = o.subdomain + o.domain
            if total % 10000 == 0: print(total, url, domain)
            if url not in urls:
                urls.append(url)
                if domain not in domains:
                    domains.append(domain)
                    uq += 1
                    line[1] = clean("".join(line[1]))
                    rows.append(line)
    print(total, uq)
    return rows
    
def write_out():
    rows = read_in()
    total = 0
    with open('data/raw/all_raw_cleaned3.csv', 'w') as outf:
        w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for row in rows:
            total += 1
            w.writerow(row)
    print("DONE", total)

write_out()