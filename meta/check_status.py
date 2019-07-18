#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:35:41 2019

@author: lavanyasingh
"""


import csv
import os
import requests
import socket

def write_codes(codes):
    with open('data/raw/codes2.csv', 'w') as outf:
        w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for url in codes:
            w.writerow([url, codes[url]])
    print("WROTE ALL CODES")

def read_in():
    sources = []
    total = 0
    with open("data/raw/all_raw_cleaned3.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            sources.append("http://" + "".join(line[1]))
            if total > 5000: break
    print("DONE READING")
    return sources

def fetch(urls):
    codes = []
    for url in urls:
        try:
            r = requests.get(url)
            s = r.status_code
            print(r)
            codes.append(s)
        except (TimeoutError, socket.timeout) as e:
            print(url, e)
            codes.append("TIMEOUTERROR")
    #print(codes)
    
os.chdir("/Users/lavanyasingh/Desktop/GSC2O19internet_archive/")
f = open("data/raw/all_raw_cleaned3.csv", 'r')
fetch(read_in())