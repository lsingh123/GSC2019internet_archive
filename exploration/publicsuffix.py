#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 14:12:06 2019

@author: lavanyasingh
"""

import publicsuffix
psl_file = publicsuffix.fetch()
psl = publicsuffix.PublicSuffixList(psl_file)
x = psl.get_public_suffix("www.example.com")
print(x)