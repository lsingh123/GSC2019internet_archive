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
TIMEOUT = 10

def read_in():
    sources = []
    total = 0
    with open("data/raw/working_urls.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            try:
                if int(line[1]) > 200 and int(line[1]) < 400:
                    sources.append(line[0])
            except ValueError:
                sources.append("NOREDIRECT")
            if total > 5000: break
    print("DONE READING")
    return sources

urls = read_in()

def load_url(url, timeout):
    ans = requests.head(url, timeout=timeout)
    return ans.url

def zip(list1, list2):
    results = {list1[i]: list2[i] for i in range(len(list1))}
    return results

def write_locations(locations):
    with open('data/raw/redirects.csv', 'w') as outf:
        w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for url in locations:
            w.writerow([url, locations[url]])
    print("WROTE ALL REDIRECTS")

def get_data():
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(load_url, url, TIMEOUT) for url in urls)
        time1 = time.time()
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
            except Exception as exc:
                data = str(type(exc))
            finally:
                results.append(data)
                out.append(data)
                print(str(len(out)),end="\r")
        time2 = time.time(g)
        return time1, time2, results
    
time1, time2, results = get_data()
print(f'Took {time2-time1:.2f} s')
redirects = zip(urls, results)
write_locations(redirects)
print("DONE")
