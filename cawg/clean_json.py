#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 17:16:58 2019

@author: lavanyasingh
"""

import json

def flip_dict(d):
    for key in d:
        value = d[key]
    return {value:int(key.replace(",", ""))}
    

with open('newssitesPOC.json') as json_file:
    data = json.load(json_file)
    for key in data:
        if key.find("top") != -1:
            d = data[key]
            data[key]  = [flip_dict(mini_d) for mini_d in d]
            #print(data[key])
    print(data)
    
with open('newssites_cleaned.json', 'w') as outfile:
    json.dump(data, outfile)