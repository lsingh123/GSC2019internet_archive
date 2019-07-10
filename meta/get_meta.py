#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 10:30:49 2019

@author: lavanyasingh
"""

import requests, re, csv, os
from contextlib import closing
from html.parser import HTMLParser
from bs4 import BeautifulSoup


#BAD DO NOT USE
def read_page_old(url):
    CHUNKSIZE = 1024
    redes = re.compile('<meta property="og:description"[^>]*>', re.IGNORECASE | re.DOTALL)
    retitle = re.compile('<meta[.]property="og:title"[.]>', re.IGNORECASE | re.DOTALL)
    rebody = re.compile('<body', re.IGNORECASE | re.DOTALL)
    buffer = ""
    meta = {'url':url}
    with closing(requests.get(url, stream=True)) as res:
        for chunk in res.iter_content(chunk_size=CHUNKSIZE, decode_unicode=True):
            buffer = "".join([buffer, chunk])
            match_t = retitle.search(buffer)
            match_d = redes.search(buffer)
            match_b = rebody.search(buffer)
            if match_t:
                content = match_t.group().split('"')
                print(content)
                meta['title'] = content
            if match_d:
                content = match_d.group().split('"')[1]
                print(content)
                meta['description'] = content
            if match_b:
                try: b = meta['title']
                except KeyError: meta['title'] = ""
                try: b = meta['description']
                except KeyError: meta['description'] = ""
                break
    return meta


def read_page(url):
    CHUNKSIZE = 1024
    meta = {'url':url}
    with closing(requests.get(url, stream=True)) as res:
        for chunk in res.iter_content(chunk_size=CHUNKSIZE, decode_unicode=True):
            soup = BeautifulSoup(chunk, 'html.parser')
            #we only care about metadata
            metas = soup.find_all('meta')
            for tag in metas:
                try: 
                    if tag['property'] == 'og:title': 
                        meta['title'] = tag['content']
                    if tag['property'] == 'og:description': 
                        meta['description'] = tag['content']
                    if tag['property'] == 'og:locale':
                        meta['locale'] == tag['content']
                except KeyError:
                    None
                # we have all the info we need
                if len(meta) == 4: break
            body = soup.find('body')
            #we've gone too far-hit the body of the page
            if body: 
                try: b = meta['title']
                except KeyError: meta['title'] = ""
                try: b = meta['description']
                except KeyError: meta['description'] = ""
                try: b = meta['locale']
                except KeyError: meta['locale'] = ""
                break
    return meta
 
#read all sources in from a CSV in [source list] format
def get_sources(path):
    with open(path, "r", errors = "ignore") as f:
        reader = csv.reader(f, delimiter = ",")
        next(reader)
        sources = []
        for line in reader:
            sources.append(line[1])
    return sources

def wiki_md():
    sources = get_sources('data/wd_sources_overlaps_removed.csv')
    meta = []
    for url in sources:
        try:
            m = read_page(url)
            print(m)
            meta.append(m)
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, 
                requests.exceptions.TooManyRedirects) as e:
            print(e)
        except requests.exceptions.Timeout as e:
            try:
                m = read_page(url)
                print(m)
                meta.append(m)
            except requests.exceptions.Timeout:
                print(e)
        #TODO clean URLs
        except (requests.exceptions.URLrequired, requests.exceptions.InvalidSchema) as e:
            print(e)
    return meta

wiki_md()
            
