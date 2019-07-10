#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 15:41:28 2019

@author: lavanyasingh
"""

import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')

from prefixes import prefixes
import helpers

HTTP_endpoint = 'http://localhost:3030/d/data'
q_endpoint = 'http://localhost:3030/d/query'
u_endpoint = 'http://localhost:3030/d/update'

endpoint_url = u_endpoint

#BE VERY CAREFULY WHEN EDITING THIS SHEET
#ONLY EDIT HERE AFTER THOROUGH TESTING
real_deal = '131Y_PxkJgibJ117fsQrfc79lVi6MLGWfCBBJvrdQuN8'
#USE THIS SHEET TO TEST 
test = '12yV42AFnUecXFXwaLUpz6Hqh9VpRp6gtap8x6xEAp7U'
        
spreadsheet_id = real_deal

service = helpers.initialize()

def write_test():
    query = prefixes + """
    INSERT DATA
    {
     <http://worldnews/nytimes.com> wdt:P17 "United States" .
    }"""
    helpers.get_results(endpoint_url, query)

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


def get_countries():
    endpoint_url = "https://query.wikidata.org/sparql"
    query = prefixes + """
    SELECT ?item ?itemLabel
    WHERE 
    {
      {?item wdt:P31 wd:Q6256} UNION
      {?item wdt:P31 wd:Q3624078} UNION
      {?item wdt:P31 wd:Q33837} UNION
      {?item wdt:P31 wd:Q27561} UNION
      {?item wdt:P31 wd:Q82794}.
      SERVICE wikibase:label  { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    } """
    
    cResults = helpers.get_results(endpoint_url, query)
    
    cRes = cResults['results']['bindings']
        
    codes = {}
    
    for item in cRes:
        codes[(item['itemLabel']['value']).lower()] = helpers.get_id(item['item']['value'])
            
    return codes

#TODO: figure out how to adjust country query/what we are missing
def get_country_code(name):
    try:
        return 'wd:'+countries[name.strip()]
    except KeyError as e:
        return("\"TODO\"")
        print(e)

def test():
    raw, total = helpers.get_sources(spreadsheet_id, service)
    s = helpers.dict_to_list(raw)
    countries = get_countries()
    source = s[1]
    url = '<http://worldnews/' + source[2] + '>'
    country_code = get_country_code(source[7].lower(), countries)
    query = prefixes + """
    INSERT DATA {
    GRAPH """ + url + """ { 
            """ + url + """ wdt:P17 wd:""" + country_code + """;
                            wdt:P1448 \"""" + source[0] + """\";
                            wdt:P31 \"""" + source[3] + """\";
                            wdt:P37 \"""" + source[6] + """\";
                            wdt:P1705 \"""" + source[1] + """\";
                            wdt:P1896 wni:""" + helpers.strip_spaces(source[5]) + """;
                            wn:paywall \"""" + source[4] + """\".}
    } """
    helpers.get_results(endpoint_url, query)

#SLOW
def dump_all_old():
    raw, total = helpers.get_sources(spreadsheet_id, service)
    s = helpers.dict_to_list(raw)
    for source in s[1:]:
        url = '<http://worldnews/' + source[2] + '>'
        country_code = get_country_code(source[7].lower(), countries)
        query = prefixes + """
        INSERT DATA {
        GRAPH """ + url + """ { 
                """ + url + """ wdt:P17 """ + country_code + """;
                                wdt:P1448 \"""" + source[0] + """\";
                                wdt:P31 \"""" + source[3] + """\";
                                wdt:P37 \"""" + source[6] + """\";
                                wdt:P1705 \"""" + source[1] + """\";
                                wdt:P1896 \"""" + source[5] + """\";
                                wn:paywall \"""" + source[4] + """\".}
        } """
        helpers.get_results(endpoint_url, query)
        

def get_graph_spec(source):
    global counter 
    url = '<http://worldnews/' + source[2] + '>'
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


#takes in a list of rows
#each row is a string list with one element per cell
# Title, Title (english not available), URL, Type, Paywall, Source, Language, Country
def dump_all(sources):
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


res = helpers.read_csv_rows('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data/newscrawls_urls_cleaned.csv')
dump_all(res)