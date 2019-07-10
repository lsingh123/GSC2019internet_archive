#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:18:16 2019

@author: lavanyasingh
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 12:44:51 2019

@author: lavanyasingh
"""

import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')
import urllib
import csv
import re

def truncate(url):
    url = urllib.parse.unquote(url.strip())
    stream = re.finditer('//', url)
    try:
        url = url[next(stream).span()[1]:]
    except StopIteration:
        url = url
    www = url.find('www.')
    if www != -1:
        url = url[www+4:]
    if url.find('subject=') != -1:
        return ''
    return url
        
def test(path):
    stream = re.finditer('/', path)
    try: 
        next(stream)
        path = path[next(stream).span()[0]:]
    except StopIteration:
        path = path
    return path

def test1(path):
    path = path.split('/')[1]
    print(path)

        
def make_truncated():
    total, uq = 0, 0
    sources = {}
    with open('data/raw/all_raw.csv', 'r') as inf:
        reader = csv.reader(inf, delimiter=',')
        for line in reader:
            total += 1
            try:
                line = ''.join(line)
                url_raw = truncate(''.join(line))
                o = urllib.parse.urlparse('http://www.' + url_raw)
                url = o.netloc
                if url not in sources:
                    uq += 1
                    sources.update({url:[]})
                else:
                    try:
                        path = '/' + o.path.split('/')[1]
                    except IndexError:
                        path = path
                    if path not in sources[url] and path != '/':
                        sources[url].append(path)
            except ValueError as e:
                print(e, url)
            if total % 10000 == 0: print(total, url, sources[url])
        print("TOTAL", total)
        print("UNIQUE", uq)
    return sources

#sources = make_truncated()

