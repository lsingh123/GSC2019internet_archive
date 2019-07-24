#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 11:18:10 2019

@author: lavanyasingh
"""
import concurrent.futures
import requests
import time
import os
os.chdir("/Users/lavanyasingh/Desktop/GSC2O19internet_archive/")
import csv
from bs4 import BeautifulSoup


out = []
CONNECTIONS = 100
TIMEOUT = 30

def read_in():
    sources = []
    total = 0
    with open("data/raw/all_raw_cleaned3.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            sources.append("http://" + "".join(line[1]))
            #if total == 109917: print(line[1])
    print("DONE READING")
    return sources

urls = read_in()

def load_url(url, timeout):
    ans = requests.get(url, timeout=timeout)
    html = ans.text
    title, desc = get_title_desc(html)
    return [url, title, desc]

def get_title_desc(html):
    soup = BeautifulSoup(html, features = "html.parser")
    h = soup.head
    try:
        title = h.find(attrs={"property": "og:title"})['content']
    except TypeError:
        try:
            title = h.find("title").text
        except TypeError:
            title = ""
    except Exception:
        title = ""
    try:
        desc = h.find(attrs={"property": "og:description"})['content']
    except TypeError:
        try:
            desc = h.find(attrs = {"name":"description"})['content']
        except TypeError:
            desc = ""
    except Exception:
        desc = ""
    return title, desc

def write_meta(meta):
    with open('data/raw/meta1.csv', 'w') as outf:
        w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for url in meta:
            if type(url) == str:
                w.writerow([url])
            else:
                w.writerow(url)
    print("WROTE ALL META")

def get_data():
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(load_url, url, TIMEOUT) for url in urls)
        time1 = time.time()
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
            except Exception as e:
                data = str(repr(e))
            finally:
                results.append(data)
                out.append(data)
                print(str(len(out)),end="\r")
        time2 = time.time()
        return time1, time2, results
    
time1, time2, results = get_data()
print(f'Took {time2-time1:.2f} s')
write_meta(results)
print("DONE")
