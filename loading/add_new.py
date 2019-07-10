#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 10:30:59 2019

@author: lavanyasingh
"""

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
        wni:usnpl wdt:P1448 "USNPL".
        wni:lion wdt:P1448 "LION Publishers"}
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
    q = ''
    if helpers.is_bad(source[1]): 
        print(source[1])
        return q
    if source[1].find('.') == -1: return q
    url = '<http://' + urllib.parse.quote(source[1]) + '>'
    url_item = '<http://' + urllib.parse.quote(source[1]) + '/item>' 
    graph = """ GRAPH """ + url 
    #url
    q += ("INSERT { " + graph + " {" + url_item + " wdt:P1896 \'" + 
            urllib.parse.quote(source[1]) + """\' }}
            WHERE {FILTER (NOT EXISTS {""" + graph + "{ ?item wdt:P1896 ?url}})} ;" )
    #country
    if not helpers.is_bad(source[0]):
        country_code = get_country_code(source[0])
        if not helpers.is_bad(country_code):
            c = country_code
        else:
            c = helpers.clean(source[0])
        q += (" INSERT { " + graph + " {" + url_item + " wdt:P17 \'" + c + """\' }}
        WHERE {FILTER (NOT EXISTS {""" + graph + "{ ?item wdt:P17 ?country}})} ;" )
    #title
    if not helpers.is_bad(source[2]):
        q += (" INSERT { " + graph + " {" + url_item + " wdt:P1448 \'" + helpers.clean(source[2]) + """\' }}
        WHERE {FILTER (NOT EXISTS {""" + graph + "{ ?item wdt:P1448 ?title}})} ;" )
    #language
    if not helpers.is_bad(source[3]):
        q += (" INSERT { " + graph + " {" + url_item + " wdt:P37 \'" + helpers.clean(source[3]) + """\' }}
        WHERE {FILTER (NOT EXISTS {""" + graph + "{ ?item wdt:P37 ?lang}})} ;" )
    #type
    if not helpers.is_bad(source[4]):
        q += (" INSERT { " + graph + " {" + url_item + " wdt:P31 \'" + helpers.clean(source[4]) + """\' }}
        WHERE {FILTER (NOT EXISTS {""" + graph + "{ ?item wdt:P31 ?type}})} ;" )
    #title (native language)
    if not helpers.is_bad(source[5]):
        q += (" INSERT { " + graph + " {" + url_item + " wdt:P1704 \'" + helpers.clean(source[5]) + """\' }}
        WHERE {FILTER (NOT EXISTS {""" + graph + "{ ?item wdt:P1448 ?title_native}})} ;" )
    #paywall
    if not helpers.is_bad(source[6]):
        q += (" INSERT { " + graph + " {" + url_item + " wnp:paywalled \'" + helpers.clean(source[6]) + """\' }}
        WHERE {FILTER (NOT EXISTS {""" + graph + "{ ?item wnp:paywalled ?pw}})} ;" )
    #metasource
    if not helpers.is_bad(source[7]):
        q += (" INSERT { " + graph + " {" + url_item + " wnp:metasource wni:" + 
        helpers.strip_spaces(source[7]).lower()   + """ }}
        WHERE {FILTER (NOT EXISTS {""" + graph + "{ ?item wnp:metasource ?ms}})} ;" )
    #state
    if not helpers.is_bad(source[8]):
        q += (" INSERT { " + graph + " {" + url_item + " wdt:P131 \'" + helpers.clean(source[8]) + """\' }}
        WHERE {FILTER (NOT EXISTS {""" + graph + "{ ?item wdt:P131 ?state}})} ;" )
    #wikipedia name
    if not helpers.is_bad(source[10]):
        q += (" INSERT { " + graph + " {" + url_item + " wnp:wikipedia-name \'" + helpers.clean(source[10]) + """\' }}
        WHERE {FILTER (NOT EXISTS {""" + graph + "{ ?item wnp:wikipedia-name ?wp_name}})} ;" )
    #redirects?
    if not helpers.is_bad(source[11]):
        q += (" INSERT { " + graph + " {" + url_item + " wnp:redirect \'" + helpers.clean(source[11]) + """\' }}
        WHERE {FILTER (NOT EXISTS {""" + graph + "{ ?item wnp:redirect ?rd}})} ;" )
    #wikipedia link
    if not helpers.is_bad(source[12]):
        q += (" INSERT { " + graph + " {" + url_item + " wnp:wikipedia-page \'" + helpers.clean(source[12]) + """\' }}
        WHERE {FILTER (NOT EXISTS {""" + graph + "{ ?item wnp:wikipedia-page ?wp_page}})} ;" )
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
    print("DONE")

if __name__ == '__main__':
   print(get_graph_spec(['United States of America','thehill.com','The Hill	', 'English', 'Newspaper', 'The Hill',	'No', 'USNPL', 
                     'DC', 'Washington', 'The Hill'	, '', 'https://en.wikipedia.org/wiki/The_Hill']))


