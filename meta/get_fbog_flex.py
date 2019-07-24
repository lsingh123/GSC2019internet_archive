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
import wrapt



class FBOGCrawler():
    CONNECTIONS = 100
    TIMEOUT = 30

    def read_in(self):
        sources = []
        total = 0
        with open("data/raw/all_raw_cleaned3.csv", 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for line in reader:
                total += 1
                sources.append("http://" + "".join(line[1]))
                if total > 20: break
        print("DONE READING")
        return sources
    
    def __init__(self):
        self.chromedriver = '/Users/lavanyasingh/Desktop/headless/chromedriver'
        self.chrome_options = Options()  
        self.chrome_options.add_argument("--headless")  
        self.chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'    
        self.driver = webdriver.Chrome(executable_path=self.chromedriver,  options=self.chrome_options)  
    
    @wrapt.synchronized
    @staticmethod
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
            print(url)
            html = self.get_html_selenium(url)
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
    
    def write_meta(self, meta):
        with open('data/raw/meta4.csv', 'w') as outf:
            w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for url in meta:
                if type(url) == str:
                    w.writerow([url])
                else:
                    w.writerow(url)
        print("WROTE ALL META")

    def main(self, urls):
        results = []
        out = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.CONNECTIONS) as executor:
            future_to_url = (executor.submit(self.get_url, url) for url in urls)
            time1 = time.time()
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    data = future.result()
                except Exception as e:
                    data = str(e)
                finally:
                    results.append(data)
                    out.append(data)
                    print(str(len(out)),end="\r")
                '''if len(data) % 1000 == 0: 
                    write_meta(results)
                    results = []'''
            #self.write_meta(results)
            time2 = time.time()
            return time1, time2, out
    
if __name__ == '__main__':  
    crawler = FBOGCrawler()
    urls = crawler.read_in()
    time1, time2, out = crawler.main(urls)
    crawler.write_meta(out)
    #crawler.write_meta(res)
    crawler.driver.close()
    print(f'Took {time2-time1:.2f} s')
