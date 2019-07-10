#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:28:45 2019

@author: lavanyasingh
"""

from SPARQLWrapper import SPARQLWrapper, JSON
import csv
import os

os.getcwd()
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data')

endpoint_url = "https://query.wikidata.org/sparql"

# P31: instance of 
# Q11032: newspaper
# P17: country (property)
# Q6256: country (item)
# Q3624078: sovereign state
# Q3024240: historical country

def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def get_id(url):
    id = url.split("/")
    return id[len(id)-1]

def get_countries():
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
        codes[item['itemLabel']['value']] = get_id(item['item']['value'])
            
    return codes 

def get_states ():
    query = """
    SELECT ?item ?itemLabel
    WHERE 
    {
      ?item wdt:P31 wd:Q3624078;
      FILTER not exists {?item wdt:P31 wd:Q3024240}.
      SERVICE wikibase:label  { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }"""
    
    sResults = get_results(endpoint_url, query)
    
    sRes = sResults['results']['bindings']
        
    codes = {}
    
    for item in sRes:
        codes[item['itemLabel']['value']] = get_id(item['item']['value'])
            
    return codes 

def get_sources(id):
    query = """
    SELECT ?item ?itemLabel ?url
    WHERE 
    {
      ?item wdt:P31 wd:Q11032;
            wdt:P17 wd:""" + id + """;
            wdt:P856 ?url.
      SERVICE wikibase:label  { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }"""
    
    results = get_results(endpoint_url, query)
    
    res = results['results']['bindings']
    
    sources = []
        
    for thing in res: 
        sources.append(thing['url']['value'])
    
    return sources

def check():
    countries = get_countries()
    states = get_states()
    count = 0
    for item in states:
        if item not in countries: count +=1
    return count

def get_all_sources():
    countries = {**get_countries(), **get_states()}
    sources = {}
    for country in countries:
        print("1" + country)
        sources[country] = get_sources(countries[country])
    return sources

    
def write_sources():
    path = 'wd_sources.csv'  
    country_sources = get_all_sources()
    with open(path, mode = 'w') as f:
        count = 0
        w = csv.writer(f, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url'])
        for country in country_sources:
            print("2" + country)
            count += 1
            for url in country_sources[country]:
                w.writerow([country, url])
 
write_sources()
