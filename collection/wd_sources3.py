#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:54:44 2019

@author: lavanyasingh
"""

from SPARQLWrapper import SPARQLWrapper, JSON
import os
import csv


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
     

def write_sources():
    query = """SELECT ?item ?itemLabel ?country ?countryLabel ?url
       WHERE
       {
         {?item wdt:P31 wd:Q11032;
               wdt:P856 ?url} UNION
         {?item wdt:P31 wd:Q1153191;
               wdt:P856 ?url} UNION
         {?item wdt:P31 wd:Q1110794;
                wdt:P856 ?url}.
         OPTIONAL { ?item wdt:P495 ?country }.
         SERVICE wikibase:label  { bd:serviceParam wikibase:language
    "[AUTO_LANGUAGE],en". }
       }"""
    results = get_results(endpoint_url, query)
    res = results['results']['bindings']
    path = 'wd_sources.csv'  
    with open(path, mode = 'w') as f:
        count = 0
        w = csv.writer(f, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type'])
        for item in res:
            count += 1
            try: 
                country = item['countryLabel']['value']
            except KeyError:
                country = 'None'
            title, url = item['itemLabel']['value'], item['url']['value']
            w.writerow([country, url, title, "None", "None"])
        print(count)
          
if __name__ == '__main__':
    write_sources()

