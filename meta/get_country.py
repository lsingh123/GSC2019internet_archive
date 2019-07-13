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
import urllib
from prefixes import prefixes

path = 'data/raw/all_raw_cleaned.csv'

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


#sources = assign_cc()


q_endpoint = 'http://lavanya-dev.us.archive.org:3030/testwn/query'
u_endpoint = 'http://lavanya-dev.us.archive.org:3030/testwn/update'

endpoint_url = u_endpoint

countries = helpers.get_countries()

#takes a raw country name and returns wikidata country code if it exists
def get_country_code(name):
    try:
        return 'wd:'+ countries[helpers.strip_spaces(name).lower()]
    except KeyError as e:
        return("\'TODO\'")
        print(e)

def get_graph_spec(source):
    q = ''
    if helpers.is_bad(source[1]): 
        print(source[1])
        return q
    if source[1].find('.') == -1: return q
    url = '<http://' + urllib.parse.quote(source[1]) + '>'
    url_item = '<http://' + urllib.parse.quote(source[1]) + '/item>' 
    graph = """ GRAPH """ + url 
    #url
    q += ("DELETE WHERE" + graph + """ {?item wdt:P17 ?country.}};
          INSERT DATA { """ + graph + "{" + url_item + " wdt:P17 """ + urllib.parse.quote(source[1]) + """\' }} 
          WHERE """ + match + ";" )
    #country
    if not helpers.is_bad(source[0]):
        country_code = get_country_code(source[0])
        if not helpers.is_bad(country_code):
            c = country_code
        else:
            c = helpers.clean(source[0])
        match = "{" + graph + "{ ?item wdt:P17 ?country}}"
        q += ("DELETE" + match + """
          INSERT { """ + graph + " {" + url_item + " wdt:P17 " + c + """ }} 
          WHERE """ + match + ";" )
    return q


#takes in a list of rows
#each row is a string list with one element per cell
def dump_all(sources):
    counter = 0
    q = ''
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
                    f.write(query)
                return "yikes"
    try:
        query = prefixes + q
        helpers.send_query(endpoint_url, query)
    except:
        with open('data/logfile', 'w') as f:
            f.write(query)
            return "yikes"
    print("DONE")

if __name__ == '__main__':
  write_meta_sources()
  sources = helpers.read_in('data/cleaned/all.csv')
  dump_all(sources)

