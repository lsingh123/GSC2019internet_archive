#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 14:44:36 2019

@author: lavanyasingh
"""


import aiohttp
import asyncio
import async_timeout
import csv
import os
os.chdir("/Users/lavanyasingh/Desktop/GSC2O19internet_archive/")
 
def read_in():
    sources = []
    total = 0
    with open("data/raw/all_raw_cleaned.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            sources.append("http://" + line[1])
            if total > 100: return sources
            
 
async def download_coroutine(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as resp:
            print("check2")
            #re = await response.read()
           # head = re[0:1024]
            print(resp.status)
            return resp.status
    

                    
async def main(loop, urls):
    #urls = ["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
    #    "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
    #    "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
    #    "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
    #   "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"]
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [download_coroutine(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        print("check7")
        #print(results[0])
 
 
if __name__ == '__main__':
    sources = read_in()
    loop = asyncio.get_event_loop()
    print("check1")
    loop.run_until_complete(main(loop, sources))