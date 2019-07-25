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
import tldextract
import re

def read_cc():
    with open("data/common_crawl.txt", "r") as f:
        sources = set()
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            sources.add(helpers.truncate(line[1]))
    print("CC", len(sources))
    return sources

def read_all():
    sources = []
    with open("data/raw/all_raw_cleaned3.csv", "r") as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            sources.append(helpers.truncate(line[1]))
    print(len(sources))
    return sources

def clean(url):
    url = url.replace("www.", "")
    stream = re.finditer('%', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    return url

def remove_dups():
    cc = read_cc()
    sources = set(read_all())
    old = len(sources)
    sources |= cc
    print("UQ", len(sources)-old)
    
def remove_dups2():
    domains, good = set(), []
    cc = read_cc()
    sources = set(read_all())
    sources |= cc
    for item in sources:
        url = clean(item)
        o = tldextract.extract(url)
        domain = o.subdomain + o.domain
        if domain not in domains:
            domains.add(domain)
            good.append(item)
    return domains, good

def write_spotcheck():
    domains, good = remove_dups2()
    with open("data/spotcheck.csv", 'w') as outf:
        w = csv.writer(outf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        total = 0 
        for url in good:
            total += 1
            if total % 500 == 0:
                w.writerow([url])

write_spotcheck()