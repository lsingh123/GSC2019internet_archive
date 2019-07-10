#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 14:44:36 2019

@author: lavanyasingh
"""




import aiohttp
import asyncio
import async_timeout
 
 
async def download_coroutine(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            re = await response.read()
            head = re[0:1024]
            return head
 
 
async def main(loop):
    urls = ["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"]
 
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [download_coroutine(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        print(results[0])
 
 
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))