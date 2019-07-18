#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 15:21:19 2019

@author: lavanyasingh
"""

import requests
url = "http://independent.ng"
ans = requests.head(url)
print(ans.url)