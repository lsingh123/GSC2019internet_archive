#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:41:18 2019

@author: lavanyasingh
"""

import pandas as pd
import concurrent.futures
import requests
import time
import os
os.chdir("/Users/lavanyasingh/Desktop/GSC2O19internet_archive/")
import csv


out = []
CONNECTIONS = 100
TIMEOUT = 5

def read_in():
    sources = []
    total = 0
    with open("data/raw/all_raw_cleaned3.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            sources.append("http://" + "".join(line[1]))
            #if total > 100: break
    print("DONE READING")
    return sources

urls = read_in()

def load_url(url, timeout):
    try:
        ans = requests.head(url, timeout=timeout, allow_redirects = True)
        redirect = "None"
        if ans.history != []:
            redirect = ans.url
        return url, ans.status_code, redirect
    except Exception:
        return url, "ERROR", "ERROR"

def write_codes(codes):
    with open('data/raw/codes9.csv', 'w') as outf:
        w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for url in codes:
            if url == "ERROR":
                row = ["ERROR", "ERROR", "ERROR"]
            else:
                row = url
            w.writerow(row)
    print("WROTE ALL CODES")

def get_data():
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(load_url, url, TIMEOUT) for url in urls)
        time1 = time.time()
        for future in concurrent.futures.as_completed(future_to_url):
            data = future.result()
            results.append(data)
            out.append(data)
            print(str(len(out)),end="\r")
        time2 = time.time()
        return time1, time2, results
    
time1, time2, results = get_data()
print(f'Took {time2-time1:.2f} s')
write_codes(results)
print("DONE")
