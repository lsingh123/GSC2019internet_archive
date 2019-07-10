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
import matplotlib.pyplot as plt

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

def visualize():
    data = [len(sources[url]) for url in sources]
    data = list(filter(lambda x: x<10 and x > 0, data))
    
    plt.hist(data, bins = range(min(data), max(data) + 1, 1))
    #plt.hist(data, histtype="step")
    #plt.show()
    return data

useful = {url:paths for url,paths in sources.items() if len(paths) < 10 }
print(useful['www.'])
import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')

from prefixes import prefixes
import helpers
import urllib.parse
import csv


q_endpoint = 'http://lavanya-dev.us.archive.org:3030/testwn/query'
u_endpoint = 'http://lavanya-dev.us.archive.org:3030/testwn/update'

endpoint_url = u_endpoint

def get_meta(path):
    pieces = path.split('_')
    return pieces[0]

def get_graph_spec(info):
    url_raw, metasource = info[0], info[1]
    q = ''
    if helpers.is_bad(url_raw): 
        print(url_raw)
        return q
    if url_raw.find('.') == -1: return q
    url = '<http://' + urllib.parse.quote(url_raw) + '>'
    url_item = '<http://' + urllib.parse.quote(url_raw) + '/item>'
    graph = """ GRAPH """ + url 
    ms = helpers.strip_spaces(metasource)
    q = "INSERT {"  + graph + "{" + url_item + "wnp:metasource wni:" + ms + """}}
    WHERE {FILTER (EXISTS {""" + graph + """{?s ?p ?o} } && 
    NOT EXISTS {""" + graph + "{ ?item wnp:metasource wni:" + ms + "}})};"
    return q

#takes in a list of rows
#each row is a string list with one element per cell
def dump_all():
    counter = 0
    q = ''
    sources = get_mc()
    for source in sources:
        s = get_graph_spec(source)
        counter += 1
        q  += s
        if counter % 1000 == 0:
            print(counter)
            query = prefixes + q
            q = ''
            try:
                helpers.send_query(endpoint_url, query)
            except:
                with open('data/logfile', 'w') as f:
                    print('whoops')
                    f.write(query)
                return "yikes"
    print("DONE")
    
def get_mc():
    urls = helpers.read_csv_list('data/mc_sources_meta.csv')
    return [[url, 'mediacloud'] for url in urls]
    

def get_sources():
    sources = []
    pref = '/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data/cleaned'
    paths = os.listdir(pref)
    total = 0
    paths.remove('.DS_Store')
    paths.remove('all.csv')
    for path in paths:
        with open('data/cleaned/' + path, 'r') as inf:
            reader = csv.reader(inf, delimiter=',')
            next(reader)
            for item in reader:
                total += 1
                url = helpers.truncate(item[1])
                if path != 'sheet_cleaned.csv': 
                    meta = get_meta(path)
                else:
                    meta = item[7]
                sources.append([url, meta])
    print("total", total)
    return sources
    


