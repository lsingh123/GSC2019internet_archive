#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:08:12 2019

@author: lavanyasingh
"""

import csv 

def clean_file():
    with open('World News Sources - World News Sources.csv', mode = "r") as source:
        with open('ia_sources.csv', mode = "w") as output:
            r = csv.reader(source, delimiter = ',')
            print(next(r))
            w = csv.writer(output, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            w.writerow(['country', 'source url'])
            for line in r:
                w.writerow([line[7], line[2]])
                
#run this line to clean the csv        
clean_file()