#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 14:00:24 2019

@author: lavanyasingh
"""

from SPARQLWrapper import SPARQLWrapper, JSON
import os
import csv

#TODO: Run this

os.getcwd()
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data')

endpoint_url = "https://query.wikidata.org/sparql"

# P31: instance of 
# Q11032: newspaper
# P17: country (property)
# Q6256: country (item)
# Q3624078: sovereign state
# Q3024240: historical country
# P495: country of origin

def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def get_id(url):
    id = url.split("/")
    return id[len(id)-1]

def get_code_list(d):
    codes = []
    for item in d:
        if item['country_code'] != None:
            codes.append(item['country_code'])
    return codes

#wayyyyy too inefficient
def get_countries(d):
    
    for item in d:
        if item['country_code'] != None:
            query = """
            SELECT ?label 
            WHERE 
            {
              wd:""" + item['country_code'] + """ rdfs:label ?label.
              FILTER (langMatches( lang(?label), "EN" )) 
              SERVICE wikibase:label  { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
            """
            results = get_results(endpoint_url, query)
            res = results['results']['bindings']
            item['country'] = res[0]['label']['value']
    return d

def get_all_countries():
    query = """
    SELECT ?item ?itemLabel
    WHERE 
    {
      ?item wdt:P31 wd:Q6256;
      FILTER not exists {?item wdt:P31 wd:Q3024240}.
      SERVICE wikibase:label  { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }"""
    
    cResults = get_results(endpoint_url, query)
    
    cRes = cResults['results']['bindings']
        
    codes = {}
    
    for item in cRes:
        codes[get_id(item['item']['value'])] = item['itemLabel']['value']
            
    return codes 

def get_sources():
    query = """
    SELECT ?item ?itemLabel ?country ?url ?itemDescription
    WHERE 
    {
      {?item wdt:P31/wdt:P279* wd:Q11032;
            wdt:P856 ?url} UNION
      {?item wdt:P31/wdt:P279* wd:Q1153191;
            wdt:P856 ?url} UNION
      {?item wdt:P31/wdt:P279* wd:Q1110794;
             wdt:P856 ?url} UNION
      {?item wdt:P31/wdt:P279* wd:Q2305295; 
             wdt:P856 ?url} UNION
      {?item wdt:P31/wdt:P279* wd:Q192283;
             wdt:P856 ?url} UNION
      {?item wdt:P31/wdt:P279* wd:Q1193236; 
             wdt:P856 ?url}.
      OPTIONAL { ?item wdt:P495 ?country }.
      SERVICE wikibase:label  { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }"""
    
    results = get_results(endpoint_url, query)
    
    res = results['results']['bindings']
        
    sources = []
    
    for item in res: 
        try: 
            sources.append({'title': item['itemLabel']['value'], 'url': item['url']['value'], 
            'country_code': get_id(item['country']['value'])})
        except KeyError:
            sources.append({'title': item['itemLabel']['value'], 'url': item['url']['value'], 
            'country_code': None})
    
    return sources

def source_countries():
    s = get_sources()
    c = get_all_countries()
    for item in s:
        print(item)
        try:
            if item['country_code'] in c:
                item['country'] = c[item['country_code']]
        except KeyError:
            item['country'] = None
    return s


def write_sources():
    path = 'wd_sources.csv'  
    sources = source_countries()
    with open(path, mode = 'w') as f:
        count = 0
        w = csv.writer(f, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url'])
        for entry in sources:
            count+=1
            if entry['country'] is None:
                w.writerow(["NONE", entry['url'], entry['title']])
            else:
                w.writerow([entry['country'], entry['url'], entry['title']])
    return count

if __name__ == '__main__':
    write_sources()