#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 13:53:17 2019

@author: lavanyasingh
"""


import os
os.chdir("/Users/lavanyasingh/Desktop/GSC2O19internet_archive/")
import csv


def read_in():
    sources = []
    total = 0
    with open("data/raw/codes5.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            try:
                if int(line[1]) == 301 or int(line[1]) == 308 or int(line[1]) == 303:
                    sources.append(line[0])
            except ValueError:
                None
            #if total > 1000: break
    print("DONE READING")
    return sources