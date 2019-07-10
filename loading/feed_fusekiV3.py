#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 11:28:34 2019

@author: lavanyasingh
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 12:49:40 2019

@author: lavanyasingh
"""


import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')

from prefixes import prefixes
import helpers
import urllib.parse

q_endpoint = 'http://lavanya-dev.us.archive.org:3030/testwn/query'
u_endpoint = 'http://lavanya-dev.us.archive.org:3030/testwn/update'

endpoint_url = u_endpoint

def write_meta_sources():
    query = prefixes + """
    INSERT DATA {
    GRAPH <http://worldnews/metasources> {
        wni:mediacloud wdt:P1448 "MediaCloud".
        wni:datastreamer wdt:P1448 "DataStreamer".
        wni:original wdt:P1448 "Original".
        wni:inkdrop wdt:P1448 "InkDrop".
        wni:wikidata wdt:P1448 "WikiData".
        wni:wikipedia wdt:P1448 "Wikipedia".
        wni:abyz wdt:P1448 "ABYZNewsLinks".
        wni:onlineradiobox wdt:P1448 "OnlineRadioBox".
        wni:w3newspapers wdt:P1448 "W3Newspapers".
        wni:newscrawls wdt:P1448 "Newscrawls".
        wni:topnews wdt:P1448 "Top_News".
        wni:gdelt wdt:P1448 "GDELT".
        wni:newsgrabber wdt:P1448 "Newsgrabber".
        wni:wikinews wdt:P1448 "Wikinews".
        wni:usnpl wdt:P1448 "USNPL".}
    } """
    helpers.send_query(endpoint_url, query)
    print('successfully wrote meta sources')

countries = helpers.get_countries()

#takes a raw country name and returns wikidata country code if it exists
def get_country_code(name):
    try:
        return 'wd:'+ countries[helpers.strip_spaces(name).lower()]
    except KeyError as e:
        return("\'TODO\'")
        print(e)

def get_graph_spec(source):
    if helpers.is_bad(source[1]): 
        print(source[1])
        return ''
    if source[1].find('.') == -1: return ''
    url = '<http://' + urllib.parse.quote(source[1]) + '>'
    url_item = '<http://' + urllib.parse.quote(source[1]) + '/item>' 
    q = """GRAPH """ + url + """ { 
    """ + url_item + """ wdt:P1896 \'""" + urllib.parse.quote(source[1]) + """\'"""
    #country
    if not helpers.is_bad(source[0]):
        country_code = get_country_code(source[0])
        if not helpers.is_bad(country_code):
            q += """;
            wdt:P17 """ + country_code + """ """
        else:
            q += """;
            wdt:P17 \'""" + helpers.clean(source[0]) + """\' """
    #title
    if not helpers.is_bad(source[2]):
        q += """;
            wdt:P1448 \'""" + helpers.clean(source[2]) + """\' """
    #language
    if not helpers.is_bad(source[3]):
        q += """;
            wdt:P37 \'""" + helpers.clean(source[3]) + """\' """
    #type
    if not helpers.is_bad(source[4]):f
        q += """;
            wdt:P31 \'""" + helpers.clean(source[4]) + """\' """
    #title (native language)
    if not helpers.is_bad(source[5]):
        q += """;
            wdt:P1704 \'""" + helpers.clean(source[5]) + """\' """    
    #paywall
    if not helpers.is_bad(source[6]):
        q += """;
            wnp:paywalled \'""" + helpers.clean(source[6]) + """\' """
    #metasource
    if not helpers.is_bad(source[7]):
        q += """;
            wnp:metasource wni:""" + helpers.strip_spaces(source[7]).lower()  
    #state
    if not helpers.is_bad(source[8]):
        q += """;
            wdt:P131 \'""" + helpers.clean(source[8]) + """\' """
    #town
    if not helpers.is_bad(source[9]):
        q += """;
            wdt:P131 \'""" + helpers.clean(source[9]) + """\' """
    #wikipedia name
    if not helpers.is_bad(source[10]):
        q += """;
            wnp:wikipedia-name \'""" + helpers.clean(source[10]) + """\' """
    #redirects?
    if not helpers.is_bad(source[11]):
        q += """;
            wnp:redirect \'""" + helpers.clean(source[11]) + """\' """
    #wikipedia link
    if not helpers.is_bad(source[12]):
        q += """;
            wnp:wikipedia-page \'""" + urllib.parse.quote(source[12]) + """\'"""
    q += """.}
        """  
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
            query = prefixes + """
            INSERT DATA {
            """ + q + """} """
            q = ''
            try:
                helpers.send_query(endpoint_url, query)
            except:
                with open('data/logfile', 'w') as f:
                    f.write(query)
                return "yikes"
    print("DONE")

if __name__ == '__main__':
    sources = helpers.read_in('data/cleaned/all.csv')
    dump_all(sources)
   #print(get_graph_spec(['United States of America','thehill.com','The Hill	', 'English', 'Newspaper', 'The Hill',	'No', 'USNPL', 
#                     'DC', 'Washington', 'The Hill'	, '', 'https://en.wikipedia.org/wiki/The_Hill']))
   #write_meta_sources()


