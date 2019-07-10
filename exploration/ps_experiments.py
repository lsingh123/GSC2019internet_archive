#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 16:00:34 2019

@author: lavanyasingh
"""

# import zstandard as z

# path = 'TU_verified_2019-05-22.ndjson.zst'

# with open(path, 'rb') as fh:
#   dctx = z.ZstdDecompressor()
#    reader = dctx.stream_reader(fh)
#    while True:
#       chunk = reader.read(16384)
#        if not chunk: break
#       print(chunk)

#import ndjson

#with open('TU_verified_2019-05-22.ndjson') as f : 
#   data = ndjson.load(f)
 
#text = ndjson.dumps(data)
#test = text[0:5]
    
import os.path, io
import multiprocessing as mp
import ujson as json

n_chunks = 12  # Number of processes to use -- will split the file up into this many pieces
filename = 'data/TU_verified_2019-05-22.ndjson'
urlStart = 'https://twitter.com/intent/user?user_id='


def worker(start,end):
    res = []
    f = io.open(filename,'r',encoding='utf-8')
    counter = 0
    f.seek(start)
    total_len = 0
    for line in f:
        counter+=1
        j = json.loads(line)
        res.append(get_url(j))
        total_len += len(line)
        if (total_len+start) >= end: break
    print(res[0])
    
def analyzeLine(line):
    line

def get_url(line):
    return urlStart + line['id_str']
    
def get_urls(data):
    ids = [x['id'] for x in data]
    urls = [urlStart + str(x) for x in ids]
    return urls
    

def find_newline_pos(f,n):
    f.seek(n)
    c = f.read(1)
    while c != '\n' and n > 0:
        n-=1
        f.seek(n)
        c = f.read(1)
    return(n)

def prestart():
    fsize = os.path.getsize(filename)
    pieces = []   # Holds start and stop position of each chunk
    initial_chunks=list(range(0,fsize,int(fsize/n_chunks)))[:-1]
    f = io.open(filename,'r',encoding='utf-8')
    pieces = sorted(set([find_newline_pos(f,n) for n in initial_chunks]))
    pieces.append(fsize)
    args = zip([x+1 if x > 0 else x for x in pieces],[x for x in pieces[1:]])
    return(args)

args = prestart()

workers = [mp.Process(target=worker, args=(start,end)) for start,end in list(args)]

for worker in workers:
   worker.start()

def reader(file):
    res = []
    f = io.open(file,'r',encoding='utf-8')
    counter = 0
    for line in f:
        counter+=1
        j = json.loads(line)
        res.append(j)
    return res

def trump():
    trump = reader('realdonaldtrump_tweets.ndjson')
    print(trump[0])




    

