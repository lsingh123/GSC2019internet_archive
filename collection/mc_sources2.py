#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:03:17 2019

@author: lavanyasingh
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:21:42 2019

@author: lavanyasingh
"""
import mediacloud.api
import csv
import os


os.getcwd()
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data')

key = '6e5564bc0c07edb1c307a8a7a34adbcb19a6d27c3d202987a1426a9066341308'
mc = mediacloud.api.MediaCloud(key)


def get_media():
    sources = []
    last_proc_id = 0
    count = 0 
    with open('mc_sources_meta.csv', mode = 'w') as f:
        w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type'])
        while last_proc_id < 1000000000:
            fetched = mc.mediaList(rows = 100, last_media_id = last_proc_id)
            for item in fetched:
                count +=1
                #each item will definitely have a title and url
                title = item['name']
                url = item['url']
                #items may or may not have languages, types, and countries
                #so we check for Nonetypes to avoid a type error
                lang, t, country = None, None, None
                if item['metadata']['language'] != None: lang = item['metadata']['language']['label']
                if item['metadata']['pub_country'] != None: country = item['metadata']['pub_country']['label']
                if item['metadata']['media_type'] != None: t = item['metadata']['media_type']['label']
                source = {'title': title, 'url': url, 
                                'country': country, 'language': lang, 'type': t}
                if source in sources: 
                    print("YIKES")
                    break
                sources.append(source)
                w.writerow([source['country'], source['url'], source['title'], 
                        source['language'], source['type']])
            if len(fetched) < 100: break
            last_proc_id = fetched[-1]['media_id']
            print(count)
    return sources

get_media()

#write all mc sources to a csv
def write_countries():
    media = get_media()
    with open('mc_sources_meta.csv', mode = 'w') as f:
        w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['country', 'source url', 'title', 'language', 'type'])
        for source in media:
            w.writerow([source['country'], source['url'], source['title'], 
                        source['language'], source['type']])


    
        
    
