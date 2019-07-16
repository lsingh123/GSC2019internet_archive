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
import ssl
import concurrent
 
def read_in():
    sources = []
    total = 0
    with open("data/raw/all_raw_cleaned3.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            sources.append("http://" + "".join(line[1]))
        return sources

custom_context = ssl.SSLContext()
custom_context.check_hostname = False
custom_context.verify_mode = ssl.CERT_NONE
async def download_coroutine(session, url):
    await asyncio.sleep(0.1)
    with async_timeout.timeout(5):
        try:
            async with asyncio.shield(session.get(url, ssl = custom_context)) as resp:
                print("good")
                return asyncio.shield(resp.status)
        except (aiohttp.client_exceptions.ClientConnectorError, 
                aiohttp.client_exceptions.TooManyRedirects, 
                aiohttp.client_exceptions.InvalidURL) as e:
            print(e)
            return "ERROR"
        except ssl.CertificateError as e:
            print("SSL")
            return "SSLERROR"
        
def zip(list1, list2):
    results = {list1[i]: list2[i] for i in range(len(list1))}
    return results
        
                    
async def main(loop, urls):
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [asyncio.shield(download_coroutine(session, url)) for url in urls]
        codes = await asyncio.gather(*tasks)
        results = zip(urls, codes) 
        return results
 
def write_codes(codes):
    with open('data/raw/codes.csv', 'w') as outf:
        w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for url in codes:
            w.writerow([url, codes[url]])
    print("WROTE ALL CODES")
    
if __name__ == '__main__':
    sources = read_in()
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(main(loop, sources))
    print("DONE")
    write_codes(res)
