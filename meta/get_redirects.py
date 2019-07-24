#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:41:18 2019

@author: lavanyasingh
"""

import concurrent.futures
import requests
import time
import os
os.chdir("/Users/lavanyasingh/Desktop/GSC2O19internet_archive/")
import csv


out = []
CONNECTIONS = 100
TIMEOUT = 30

def read_in():
    sources = []
    total = 0
    with open("data/raw/working_urls.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            try:
                if int(line[1]) == 301 or int(line[1]) == 308 or int(line[1]) == 303:
                    sources.append(line[0])
            except ValueError:
                None
            #if total > 1000: break
    print("DONE READING")
    return sources

def load_url(url, timeout):
    ans = requests.head(url, timeout=timeout)
    return url, ans.url


def get_data():
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(load_url, url, TIMEOUT) for url in urls)
        time1 = time.time()
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
            except Exception as exc:
                data = ("", "ERROR")
            finally:
                results.append(data)
                out.append(data)
                print(str(len(out)),end="\r")
        time2 = time.time()
        return time1, time2, results

def write_locations(locations):
    with open('data/raw/redirects.csv', 'w') as outf:
        w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for url in locations:
            w.writerow([url[0], url[1]])
    print("WROTE ALL REDIRECTS")
    
urls = read_in()
time1, time2, results = get_data()
print(f'Took {time2-time1:.2f} s')
write_locations(results)
print("DONE")

