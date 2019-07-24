#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 15:21:19 2019

@author: lavanyasingh
"""

import requests
url = "http://newslink.pk"
ans = requests.head(url)
print(ans.status)
print(ans.history)