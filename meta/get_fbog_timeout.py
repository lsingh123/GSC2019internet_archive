#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 10:04:44 2019

@author: lavanyasingh
"""

import concurrent.futures
import requests
import time
import os
os.chdir("/Users/lavanyasingh/Desktop/GSC2O19internet_archive/")
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
import os

out = []
CONNECTIONS = 100
TIMEOUT = 30


def read_in():
    sources = []
    total = 0
    with open("data/raw/all_raw_cleaned3.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            sources.append("http://" + "".join(line[1]))
            if total > 10: break
    print("DONE READING")
    return sources

urls = read_in()

    
chromedriver = '/Users/lavanyasingh/Desktop/headless/chromedriver'
#os.environ['webdriver.chrome.driver'] = chromedriver
#driver = webdriver.Chrome(chromedriver)
chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'    
driver = webdriver.Chrome(executable_path=chromedriver,  options=chrome_options)  
        
def get_html_selenium(url):
    driver.get(url)
    innerHTML = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    return innerHTML

def get_html(url, timeout):
    ans = requests.get(url, timeout=timeout)
    html = ans.text
    return html

def load_url(url):
    print(url)
    html = get_html_selenium(url)
    title, desc = get_title_desc(html)
    print(title, desc)
    return [url, title, desc]

def get_title_desc(html):
    soup = BeautifulSoup(html, features = "html.parser")
    h = soup.head
    try:
        title = h.find(attrs={"property": "og:title"})['content']
    except TypeError:
        try:
            title = h.find("title").text
        except AttributeError:
            title = ""
    except Exception:
        title = ""
    try:
        desc = h.find(attrs={"property": "og:description"})['content']
    except TypeError:
        try:
            desc = h.find(attrs = {"name":"description"})['content']
        except TypeError:
            desc = ""
    except Exception:
        desc = ""
    return title, desc

def write_meta(meta):
    with open('data/raw/meta4.csv', 'w') as outf:
        w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for url in meta:
            if type(url) == str:
                w.writerow([url])
            else:
                w.writerow(url)
    print("WROTE ALL META")

def get_data():
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(load_url, url) for url in urls)
        time1 = time.time()
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
            except Exception as e:
                data = str(repr(e))
            finally:
                results.append(data)
                out.append(data)
                print(str(len(out)),end="\r")
            if len(data) % 1000 == 0: 
                write_meta(results)
                results = []
        write_meta(results)
        time2 = time.time()
        return time1, time2
    
time1, time2 = get_data()
print(f'Took {time2-time1:.2f} s')

