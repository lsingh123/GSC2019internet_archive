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

def dict_to_array(d):
    data = {}
    for mini_d in d:
        for key in mini_d:
            data.update({mini_d[key]:int(key.replace(",", ""))})
    return data
            
with open('newssitesPOC.json') as json_file:
    data = json.load(json_file)
    for key in data:
        if key.find("top") != -1:
            d = data[key]
            data[key]  = dict_to_array(d)
            print(data[key])
    
with open('newssites_cleaned2.json', 'w') as outfile:
    json.dump(data, outfile)