#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 10:04:44 2019

@author: lavanyasingh
"""

import requests
import os
os.chdir("/Users/lavanyasingh/Desktop/GSC2O19internet_archive/")
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
import os
import multiprocessing
import time


class FBOGCrawler():
    PROCESSES = 5
    TIMEOUT = 30
    n = 10

    def read_in(self):
        sources = []
        total = 0
        with open("data/raw/all_raw_cleaned3.csv", 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for line in reader:
                total += 1
                sources.append("http://" + "".join(line[1]))
                #if total > 100: break
        print("DONE READING")
        return sources
    
    def __init__(self):
        self.results = []
        self.chromedriver = '/Users/lavanyasingh/Desktop/headless/chromedriver'
        self.chrome_options = Options()  
        self.chrome_options.add_argument("--headless")  
        self.chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'    
        self.driver = webdriver.Chrome(executable_path=self.chromedriver,  options=self.chrome_options)  
    
        
    def get_html_selenium(self, url):
        self.driver.get(url)
        innerHTML = self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        return innerHTML
    
    def get_html(self, url):
        ans = requests.get(url, timeout=self.TIMEOUT)
        html = ans.text
        return html
    
    def get_description(self, head):
        try:
            return head.find(attrs={"property": "og:description"})['content']
        except TypeError:
            pass
        try:
            return head.find(attrs = {"name":"description"})['content']
        except TypeError:
            return ""
    
    def get_url(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, features = "html.parser")
        h = soup.head
        desc = self.get_description(h)
        if desc == "":
            lock.acquire()
            html = self.get_html_selenium(url)
            lock.release()
            soup = BeautifulSoup(html, features = "html.parser")
            h = soup.head
            desc = self.get_description(h)
        try: 
            locale = h.find(attrs={"property": "og:locale"})['content']
        except TypeError:
            locale = ""
        try:
            title = h.find(attrs={"property": "og:title"})['content']
        except TypeError:
            try:
                title = h.find("title").text
            except TypeError:
                title = ""
        except Exception:
            raise
            title = ""
        return url, title, desc, locale
    
    def get_url_safe(self, url):
        try:
            return self.get_url(url)
        except KeyboardInterrupt:
            print("KEYBOARDINTERRUPT", len(self.results))
        except Exception as e:
            return url, str(e)
    
    def write_meta(self, meta):
        with open('data/raw/meta5.csv', 'w') as outf:
            w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for url in meta:
                w.writerow(list(url))
        print("WROTE ALL META")
        
    def log_result(self, result):
        self.results.append(result)
        print(str(len(self.results)),end="\r")
        
    def main(self, urls, crawler):
        num_workers = multiprocessing.cpu_count()
        l = multiprocessing.Lock()
        pool = multiprocessing.Pool(processes = num_workers, initializer = init, initargs=(l,))
        for url in urls:
            pool.apply_async(get_urls, args = (url,), callback = self.log_result)
        pool.close()
        pool.join()
        return self.results

def init(l):
        global lock
        lock = l
        
def get_urls(urls):
    return crawler.get_url_safe(urls)

crawler = FBOGCrawler()
    
if __name__ == '__main__':  
    urls = crawler.read_in()
    print("hello")
    time1 = time.time()
    res = crawler.main(urls, crawler)
    time2 = time.time()
    print(f'Took {time2-time1:.2f} s')
    crawler.write_meta(res)
    #print(res)
    crawler.driver.close()
    print("DONE")
