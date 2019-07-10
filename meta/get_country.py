#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:19:27 2019

@author: lavanyasingh
"""

#in this script I will check for country suffixes to URLs from news sources
import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')
import csv 
from bs4 import BeautifulSoup
import requests
import helpers
import tldextract

path = 'data/cleaned/all.csv'

def get_cc():
    page = 'https://icannwiki.org/Country_code_top-level_domain'
    countries = {}
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    data = table.find_all('tr')[1:]
    for row in data:
        items = row.find_all('td')
        code = items[0].find('a')['title'][1:]
        country = items[1].contents[0]
        countries[code] = country
    return countries

countries = get_cc()

def find_cc(url):
    tld = tldextract.extract(url)[2]
    if tld.find('.') != -1:
        tld = tld[tld.find('.')+1:]
    if tld in countries:
        return countries[tld]
    return None

def assign_cc():
    sources = helpers.read_in(path)
    count, total = 0, 0
    for source in sources:
        total += 1
        country = find_cc(source[1])
        if country != None: 
            count +=1
            source[0] = country
    print(count, total)
    return sources

def write_cc():
    sources = assign_cc()
    with open(path, "w", errors = "ignore") as f:
        w = csv.writer(f, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type', 'title native language',
                    'paywall', 'metasource', 'state', 'town', 'wikipedia name', 'redirects?',
                    'wikipedia link'])
        for item in sources:
            w.writerow(item)
    print("DONE")


write_cc()
