#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 12:49:40 2019

@author: lavanyasingh
"""


#TODO: figure out how to check total entries
#TODO: figure out how to check for redunant entries 
#TODO: figure out how to EDIT existing entries
#TODO: add additional metadata

import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')

from prefixes import prefixes
import helpers

HTTP_endpoint = 'http://207.241.233.126:3030/testwn/data'
q_endpoint = 'http://207.241.233.126:3030/testwn/query'
u_endpoint = 'http://207.241.233.126:3030/testwn/update'

endpoint_url = u_endpoint

#BE VERY CAREFULY WHEN EDITING THIS SHEET
#ONLY EDIT HERE AFTER THOROUGH TESTING
real_deal = '131Y_PxkJgibJ117fsQrfc79lVi6MLGWfCBBJvrdQuN8'
#USE THIS SHEET TO TEST 
test = '12yV42AFnUecXFXwaLUpz6Hqh9VpRp6gtap8x6xEAp7U'
        
spreadsheet_id = real_deal

service = helpers.initialize()

def write_meta_sources():
    query = prefixes + """
    INSERT DATA {
    GRAPH <http://worldnews/metasources> {
        wni:mediacloud wdt:P1448 "MediaCloud".
        wni:datastreamer wdt:P1448 "DataStreamer".
        wni:original wdt:P1448 "Manual".
        wni:inkdrop wdt:P1448 "InkDrop".
        wni:wikidata wdt:P1448 "WikiData".
        wni:wikipedia wdt:P1448 "Wikipedia".
        wni:abyz wdt:P1448 "ABYZNewsLinks".
        wni:onlineradiobox wdt:P1448 "OnlineRadioBox".
        wni:w3newspapers wdt:P1448 "W3Newspapers".
        wni:newscrawls wdt:P1448 "Newscrawls".
        wni:topnews wdt:P1448 "Top_News".}
    } """
    helpers.get_results(endpoint_url, query)


#countries = helpers.get_countries()

def get_country_code(name):
    try:
        return 'wd:'+countries[name.strip()]
    except KeyError as e:
        return("\"TODO\"")
        print(e)

def get_graph_spec(source):
    url = '<' + source[2] + '>'
    country_code = get_country_code(source[7].lower())
    q = """GRAPH """ + helpers.clean(url) + """ { 
    """ + url + """ wdt:P17 """ + country_code + """;
    wdt:P1448 \"""" + helpers.clean(source[0]) + """\";
    wdt:P31 \"""" + helpers.clean(source[3]) + """\";
    wdt:P37 \"""" + helpers.clean(source[6]) + """\";
    wdt:P1705 \"""" + helpers.clean(source[1]) + """\";
    wdt:P1896 wni:""" + helpers.strip_spaces(source[5]) + """;
    wnp:paywall \"""" + helpers.clean(source[4]) + """\".}
    """
    return q

def get_sources_sheet():
    raw, total = helpers.get_sources(spreadsheet_id, service)
    s = helpers.dict_to_list(raw)
    return s[1:]

def get_sources_csv(meta, path):
    res = helpers.read_csv_rows(path)
    for item in res:
        res[5] = meta
        
#takes in a list of rows
#each row is a string list with one element per cell
def dump_all(sources):
    write_meta_sources()
    counter = 0
    q = ''
    for source in sources:
        s = get_graph_spec(source)
        counter += 1
        q  += s
        if counter > 1000:
            print(counter)
            query = prefixes + """
            INSERT DATA {
            """ + q + """} """
            q = ''
            helpers.get_results(endpoint_url, query)
            counter = 0
            
if __name__ == '__main__':
    path = '/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data/newscrawls_urls_cleaned.csv'
    sources = get_sources_csv('newscrawls', path)

