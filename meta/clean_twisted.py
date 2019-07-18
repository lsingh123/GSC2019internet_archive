#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 17:07:44 2019

@author: lavanyasingh
"""

import treq
from twisted.internet import task, reactor
import csv

filename = 'test.csv'
 
def read_in():
    sources = []
    total = 0
    with open("data/raw/all_raw_cleaned3.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            sources.append("http://" + "".join(line[1]))
            if total > 10: break
    print("DONE READING")
    return sources

def writeToFile(content):
    with open(filename, 'ab') as f:
        f.write(content)

def everyMinute(urls):
    for url in urls:
        d = treq.get(url)
        d.addCallback(treq.code)
        d.addCallback(writeToFile)

#----- Main -----#            
sites = read_in()

repeating = task.LoopingCall(everyMinute, sites)
repeating.start(60)
