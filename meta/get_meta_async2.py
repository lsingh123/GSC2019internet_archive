#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 17:19:27 2019

@author: lavanyasingh
"""

import asyncio
from aiohttp import ClientSession
import concurrent
import socket
import aiohttp
import csv
import ssl
import os
os.chdir("/Users/lavanyasingh/Desktop/GSC2O19internet_archive/")
import sys

custom_context = ssl.SSLContext()
custom_context.check_hostname = False
custom_context.verify_mode = ssl.CERT_NONE
async def fetch(url, session):
    try:
        async with session.get(url, ssl = custom_context) as response:
            s = (response.status)
            print(s)
            return s
    except ValueError as e:
        #print(e)
        return "VALUEERROR"
    except (socket.gaierror, aiohttp.client_exceptions.ClientConnectorError, 
            aiohttp.client_exceptions.ClientOSError, aiohttp.client_exceptions.ServerDisconnectedError) as e:
        #print(e)
        return "CONNECTERROR"
    except concurrent.futures._base.TimeoutError as e:
        #print(e)
        return "TIMEOUTERROR"
    except aiohttp.http_exceptions.LineTooLong as e:
        #print(e)
        return "LINETOOLONGERROR"
    except aiohttp.client_exceptions.TooManyRedirects as e:
        #print(e)
        return "TOOMANYREDIRECTSERROR"
    except aiohttp.client_exceptions.ClientResponseError as e:
        #print(e)
        return "CLIENTRESPONSEERROR"
    except Exception as e:
        print(url, e)
        return("hm")
        raise

async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        s = await fetch(url, session)

async def run(urls):
    tasks = []
    ignore_aiohttp_ssl_eror(asyncio.get_running_loop())
    # create instance of Semaphore
    sem = asyncio.Semaphore(1024)

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
        data = zip(urls, res)
        return data

def write_codes(codes):
    with open('data/raw/codes2.csv', 'w') as outf:
        w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for url in codes:
            w.writerow([url, codes[url]])
    print("WROTE ALL CODES")

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

SSL_PROTOCOLS = (asyncio.sslproto.SSLProtocol,)
try:
    import uvloop.loop
except ImportError:
    pass
else:
    SSL_PROTOCOLS = (*SSL_PROTOCOLS, uvloop.loop.SSLProtocol)
    
def ignore_aiohttp_ssl_eror(loop):
    """Ignore aiohttp #3535 / cpython #13548 issue with SSL data after close

    There is an issue in Python 3.7 up to 3.7.3 that over-reports a
    ssl.SSLError fatal error (ssl.SSLError: [SSL: KRB5_S_INIT] application data
    after close notify (_ssl.c:2609)) after we are already done with the
    connection. See GitHub issues aio-libs/aiohttp#3535 and
    python/cpython#13548.

    Given a loop, this sets up an exception handler that ignores this specific
    exception, but passes everything else on to the previous exception handler
    this one replaces.

    Checks for fixed Python versions, disabling itself when running on 3.7.4+
    or 3.8.

    """
    if sys.version_info >= (3, 7, 4):
        return

    orig_handler = loop.get_exception_handler()

    def ignore_ssl_error(loop, context):
        if context.get("message") in {
            "SSL error in data received",
            "Fatal error on transport",
        }:
            # validate we have the right exception, transport and protocol
            exception = context.get('exception')
            protocol = context.get('protocol')
            if (
                isinstance(exception, ssl.SSLError)
                and exception.reason == 'KRB5_S_INIT'
                and isinstance(protocol, SSL_PROTOCOLS)
            ):
                if loop.get_debug():
                    asyncio.log.logger.debug('Ignoring asyncio SSL KRB5_S_INIT error')
                return
        if orig_handler is not None:
            orig_handler(loop, context)
        else:
            loop.default_exception_handler(context)

    loop.set_exception_handler(ignore_ssl_error)


def zip(list1, list2):
    results = {list1[i]: list2[i] for i in range(len(list1))}
    return results

loop = asyncio.get_event_loop()
sources = read_in()
future = asyncio.ensure_future(run(sources))
res = loop.run_until_complete(future)
write_codes(res)