#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 14:23:11 2019

@author: lavanyasingh
"""

import csv
import os
os.chdir("/Users/lavanyasingh/Desktop/GSC2O19internet_archive/")

def read_in():
    total = 0
    with open("data/raw/all_raw_cleaned.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        with open("data/spotcheck.csv", 'w') as outf:
            w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for line in reader:
                total += 1
                if total % 100 < 4 : 
                    w.writerow([line[1]])
    print("DONE", total)



def print_out():
    total = 0
    with open("data/raw/all_raw_cleaned.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            if (total - 1) % 100 < 4 == 0: 
                print(line[1])
    print("DONE", total)
    
print_out()

read_in()