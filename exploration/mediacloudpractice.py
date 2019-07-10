#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 16:33:58 2019

@author: lavanyasingh
"""

import mediacloud.api
key = '6e5564bc0c07edb1c307a8a7a34adbcb19a6d27c3d202987a1426a9066341308'
mc = mediacloud.api.MediaCloud(key)

res = mc.media(1)

res2 = mc.mediaList(0, 20, "New York Times")
nyt = [x for x in res2 if x['name'] == "New York Times"][0]
nm = nyt['name']

res3 = mc.storyPublic(1)
ap = res3['ap_syndicated']

res4 = mc.storyCount("obama")
c = res4['count']

res5 = mc.tagList(0, 5, 20, 1, "news")

res6 = mc.tagSetList(0)
coll = res6[3]
print(coll["description"])
print(coll['tag_sets_id'])

res7 = mc.tagList(last_tags_id = 0, tag_sets_id = 5, public_only = True)

s = mc.stats()

res8 = mc.storyList(solr_query = "tags_id_stories:8879214")


# all of this is looking for STORIES related to the given tag id 
arubaSources = mc.mediaList(tags_id = 8880303)

arubaSourcesSOLR = mc.mediaList(q = "tags_id_stories:8880303")

usSources = mc.mediaList(tags_id = 34412183)

usSourcesSOLR = mc.mediaList(q = "tags_id_stories:8878461")

usStories = mc.storyList(solr_query = "tags_id_stories:8878461")

sources = set([x['media_name'] for x in usStories])

print(sources)

import csv 
#playing with source list
with open ('Sample+Source+List+CSV.csv', 'r', errors = 'ignore') as f :
    reader = csv.reader(f, delimiter=',')
    names = (next(reader))
    f.seek(0)
    length = sum(1 for line in reader)

# source tags for each country 
last_proc_tag = 0
countries = set()
while True : 
    fetched = mc.tagList(tag_sets_id = 1935, last_tags_id = last_proc_tag, rows = 100)
    cfetched = [(tag['label'], tag['tags_id']) for tag in fetched]
    c = set(cfetched)
    countries = countries.union(c)
    if len(fetched) < 100: break 
    last_proc_tag = cfetched[-1][1]

countries = list(countries)


def get_media(tag) : 
    last_proc_id = 0
    sources = []
    while True : 
        fetched = mc.mediaList(tags_id = tag, rows = 100, last_media_id = last_proc_id)
        sources.extend(fetched)
        if len(fetched) < 100: break
        last_proc_id = fetched[-1]['media_id']
    return sources

media = []
for c in countries : 
    media.extend(get_media(c[1]))


# story tags for each country - DIFFERENT FROM SOURCE TAGS (i checked)
import os
os.getcwd()
os.chdir('/Users/lavanyasingh/Desktop/internet_archive')
import csv


with open('country-geo-tags.csv') as f :
    reader = csv.reader(f, delimiter = ',')
    for line in reader:
        print(line[0])

#grabbing lots of tags
last_proc_id = 0
tags = []
count = 0
while count < 50 :
    fetched = mc.tagList(rows = 100, last_tags_id = last_proc_id)
    tags.extend(fetched)
    if len(fetched) < 100: break
    last_proc_id = tags[-1]['tags_id']
    count += 1
    
    
    
