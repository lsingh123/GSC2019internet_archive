#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:27:51 2019

@author: lavanyasingh
"""

# modified fetch function with semaphore
import asyncio
from aiohttp import ClientSession
import csv
import os
os.chdir("/Users/lavanyasingh/Desktop/GSC2O19internet_archive/")

async def fetch(url, session):
    async with session.get(url) as response:
        s = response.status
        print(s)
        return s

def read_in():
    sources = []
    total = 0
    with open("data/raw/all_raw_cleaned3.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            sources.append("http://" + "".join(line[1]))
            if total > 1: break
    print("DONE READING")
    return sources

async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session)


async def run(urls):
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for url in urls:
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url, session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        res = await responses
        print(res)

loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run(read_in()))
loop.run_until_complete(future)