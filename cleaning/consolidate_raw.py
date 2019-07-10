#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:27:48 2019

@author: lavanyasingh
"""

import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')

import csv

def get_meta(path):
    return path.split('.')[0].replace('data/', '')

def us_news():
    with open('data/us_news.csv', 'r') as inf:
        reader = csv.reader(inf, delimiter=',')
        next(reader)
        with open('data/raw/all_raw.csv', 'a+') as outf:
            w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for line in reader:
                w.writerow(['United States', line[2], line[1], 'English', line[3], line[1], 
                            '', 'original', line[0], '', '', '', ''])

def formatted(path):
    with open(path, 'r') as inf:
        reader = csv.reader(inf, delimiter=',')
        next(reader)
        with open('data/raw/all_raw.csv', 'a+') as outf:
            w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for line in reader:
                row = line + ['' for n in range(9)]
                row[7] = get_meta(path) 
                w.writerow(row)
    print("DONE WITH ", path)
        

def usnpl():
    with open('data/usnpl_wiki_list.csv', 'r') as inf:
        reader = csv.reader(inf, delimiter=',')
        next(reader)
        with open('data/raw/all_raw.csv', 'a+') as outf:
            w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for line in reader:
                w.writerow(['United States', line[3], line[2], 'English', 'Newspaper', line[2],
                   '', 'usnpl', line[0], line[1], line[4], line[6], line[7]])
                
def txt(path):
    with open(path, 'r') as inf:
        with open('data/raw/all_raw.csv', 'a+') as outf:
            w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for line in inf:
                row = [line if n == 1 else '' for n in range(12)]
                row[7] = get_meta(path)
                w.writerow(row)
    print ("DONE WITH ", path)

def lion():
    with open('data/lion.csv', 'r') as inf:
        reader = csv.reader(inf, delimiter=',')
        next(reader)
        with open('data/raw/all_raw.csv', 'a+') as outf:
            w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for line in reader:
                w.writerow(['United States', line[1], line[0], 'English', '', line[0],
                   '', 'lion', line[5], line[4], '', '', ''])


if __name__ == '__main__':
    us_news()
    usnpl()
    lion()
    formatted('data/wikinews.csv')
    formatted('data/wikidata.csv')
    txt('data/topnews')
    formatted('data/newsgrabber.csv')
    txt('data/newscrawls')
    formatted('data/mediacloud.csv')
    formatted('data/inkdrop.csv')
    txt('data/gdelt')
    formatted('data/datastreamer.csv')
    