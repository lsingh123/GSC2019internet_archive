#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 10:47:54 2019

@author: lavanyasingh
"""

from franz.openrdf.connect import ag_connect
from franz.openrdf.repository.repository import Repository
from franz.openrdf.sail.allegrographserver import AllegroGraphServer


AGRAPH_HOST = 'http://10.30.67.138'
AGRAPH_PORT = '10035'
AGRAPH_USER = 'test'
AGRAPH_PASSWORD = 'xyzzy'

print("Connecting to AllegroGraph server --",
      "host:'%s' port:%s" % (AGRAPH_HOST, AGRAPH_PORT))
server = AllegroGraphServer(AGRAPH_HOST, AGRAPH_PORT,
                            AGRAPH_USER, AGRAPH_PASSWORD)

with ag_connect('test', create=True, clear=True) as conn:
    print('Statements:', conn.size())

