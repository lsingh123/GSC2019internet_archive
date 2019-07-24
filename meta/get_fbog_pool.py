#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 13:40:05 2019

@author: lavanyasingh
"""


from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import csv
import os
os.chdir("/Users/lavanyasingh/Desktop/GSC2O19internet_archive/")
from requests_html import HTMLSession
import traceback

def read_in():
    sources = []
    total = 0
    with open("data/raw/all_raw_cleaned3.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            sources.append("http://" + "".join(line[1]))
            if total > 10: break
    print("DONE READING")
    return sources

urls = read_in()
session = HTMLSession()

def get_title_desc(url):
    r = session.get(url, timeout=30)
    r.html.render(timeout = 30)
    html = r.html.html
    soup = BeautifulSoup(html, features = "html.parser")
    h = soup.head
    try:
        title = h.find(attrs={"property": "og:title"})['content']
    except TypeError:
        try:
            title = h.find("title").text
        except AttributeError:
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
    return url, title, desc

def load_url(url):
    try:
        return get_title_desc(url)
    except Exception as e:
        return(url, "ERROR", "ERROR")
        traceback.print_exc()


def write_meta(meta):
    with open('data/raw/meta4.csv', 'w') as outf:
        w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for url in meta:
            if type(url) == str:
                w.writerow([url])
            else:
                w.writerow(url)
    print("WROTE ALL META")

p = Pool(processes=3)
res = p.map(load_url, urls)
p.close()
p.join()
print(res)
session.close()
