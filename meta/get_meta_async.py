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
import socket
 
def read_in():
    sources = []
    total = 0
    with open("data/raw/all_raw_cleaned3.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            sources.append("http://" + "".join(line[1]))
            #if total > 10: break
    print("DONE READING")
    return sources

custom_context = ssl.SSLContext()
custom_context.check_hostname = False
custom_context.verify_mode = ssl.CERT_NONE
async def download_coroutine(session, url):
    with async_timeout.timeout(50):
        try:
            async with session.get(url, ssl = custom_context) as resp:
                print("good")
                return await resp.status
        except asyncio.CancelledError as e:
            print(url, "ERROR")
            raise
            return "ERROR"
        except ssl.CertificateError as e:
            print("SSL")
            return "SSLERROR"
        except ValueError as e:
            print("OHNO")
            return "VALUEERROR"
        
def zip(list1, list2):
    results = {list1[i]: list2[i] for i in range(len(list1))}
    return results
        
                    
async def main(loop, urls):
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [download_coroutine(session, url) for url in urls]
        codes = await asyncio.gather(*tasks)
        results = zip(urls, codes) 
        return results
 
def write_codes(codes):
    with open('data/raw/codes2.csv', 'w') as outf:
        w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for url in codes:
            w.writerow([url, codes[url]])
    print("WROTE ALL CODES")
    
#if __name__ == '__main__':
    #loop = asyncio.get_event_loop()
    #res = loop.run_until_complete(main(loop, sources))


from aiohttp import ClientSession

async def fetch(url, session):
    try:
        async with session.get(url, ssl = custom_context) as response:
            s = response.status
            print(s)
            return s
    except ValueError as e:
        print(e)
        return "VALUEERROR"
    except (socket.gaierror, aiohttp.client_exceptions.ClientConnectorError, 
            aiohttp.client_exceptions.ClientOSError, aiohttp.client_exceptions.ServerDisconnectedError) as e:
        print(e)
        return "CONNECTERROR"
    except concurrent.futures._base.TimeoutError as e:
        print(e)
        return "TIMEOUTERROR"

async def run(urls):
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        print(responses[0])
        return zip(urls, responses)

def print_responses(result):
    print(result)

sources = read_in()
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(sources))
responses = loop.run_until_complete(future)
write_codes(responses)