#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 13:44:13 2019

@author: lavanyasingh
"""

import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')
import csv
import requests
import http.client

def get_status_code(host):
    try:
        conn = http.client.HTTPConnection(host)
        conn.request("HEAD", "/")
    except TimeoutError as e:
        print(e)
        return 408
    return conn.getresponse().status

def read_in():
    urls = []
    with open('data/raw/all_raw_cleaned2.csv', 'r') as inf:
        reader = csv.reader(inf, delimiter=',')
        for line in reader:
            urls.append("".join(line[1]))
    return urls

def get_codes(urls):
    codes = {}
    for url in urls[0:50]:
        print(url)
        codes.update({url:get_status_code(url)})
    return codes

codes = get_codes(read_in())