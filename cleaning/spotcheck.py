#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:47:31 2019

@author: lavanyasingh
"""

import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')

import csv
import re

def truncate_wo_slashes(url):
    url = url.strip()
    stream = re.finditer('//', url)
    try:
        url = url[next(stream).span()[1]:]
    except StopIteration:
        url = url
    www = url.find('www.')
    if www != -1:
        url = url[www+4:]
    #stream = re.finditer('/', url)
    #try:
    #    url = url[:next(stream).span()[0]]
    #except StopIteration:
    #    url = url
    stream = re.finditer('#', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    stream = re.finditer('%', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    stream = re.finditer('\?', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    stream = re.finditer('\&', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url        
    try:
        int(url.replace('.', ''))
        return ''
    except:
        None
    return url.replace('subject=', '')

def truncate(url):
    url = url.strip()
    stream = re.finditer('//', url)
    try:
        url = url[next(stream).span()[1]:]
    except StopIteration:
        url = url
    www = url.find('www.')
    if www != -1:
        url = url[www+4:]
    stream = re.finditer('/', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    stream = re.finditer('#', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    stream = re.finditer('%', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    stream = re.finditer('\?', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    stream = re.finditer('\&', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url        
    try:
        int(url.replace('.', ''))
        return ''
    except:
        None
    return url.replace('subject=', '')

def truncate_on_slashes(url):
    url = url.strip()
    stream = re.finditer('//', url)
    try:
        url = url[next(stream).span()[1]:]
    except StopIteration:
        url = url
    www = url.find('www.')
    if www != -1:
        url = url[www+4:]
    stream = re.finditer('/', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    return url.replace('subject=', '')

def count_slashes():
    count = 0
    with open('data/raw/all_raw.csv', 'r') as inf:
        reader = csv.reader(inf, delimiter=',')
        for line in reader:
            try:
                line = ''.join(line)
                url = truncate_on_slashes(''.join(line))
                if url in sources:
                    count += 1
            except IndexError:
                print('index error', ''.join(line))
    print("OVERLAPS DUE TO SLASHES", count)

def make_truncated():
    count = 0
    sources = []
    with open('data/raw/all_raw.csv', 'r') as inf:
        reader = csv.reader(inf, delimiter=',')
        for line in reader:
            count += 1
            try:
                line = ''.join(line)
                url = truncate(''.join(line))
                if url not in sources:
                    sources.append(url)
            except IndexError:
                print('index error', ''.join(line))
            if count % 5000 == 0: print(count)
    return sources

sources = make_truncated()

def check_overlaps():
    sources = []
    count = 0
    with open('data/raw/all_raw.csv', 'r') as inf:
        reader = csv.reader(inf, delimiter=',')
        for line in reader:
            try:
                url = truncate(''.join(line))
                if url in sources:
                    count += 1 
                    print("original:", ''.join(line))
                    print("truncated", url)
                else:
                    sources.append(url)
            except IndexError:
                print('index error', ''.join(line))
    print("OVERLAPS", count)
    
def test():
    sources = []
    count = 0
    with open('data/raw/all_raw.csv', 'r') as inf:
        reader = csv.reader(inf, delimiter=',')
        next(reader)
        line = (next(reader))
        print(type(''.join(line)), ''.join(line))


                
        