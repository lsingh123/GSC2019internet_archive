#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 11:08:07 2019

@author: lavanyasingh
"""

import csv
import sys
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from truncate import truncate

def fix_csv(path_old, path_new):
    sources = []
    count = 0 
    uq = 0 
    with open(path_old, 'r') as inf:
        reader = csv.reader(inf, delimiter = ",")
        next(reader)
        with open(path_new, 'w') as outf:
            w = csv.writer(outf, delimiter=',', quotechar='"', 
                           quoting=csv.QUOTE_MINIMAL)
            w.writerow(['country', 'source url', 'title', 'language', 'type'])
            for line in reader:
                count +=1
                url = truncate(line[1])
                if count % 100 == 0: print(url)
                if url not in sources:
                    uq +=1
                    sources.append(url)
                    w.writerow([line[0], url, line[2], line[3], line[4]])
    print('count', count)
    print ('uq', uq)
                
    
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

#BE VERY CAREFULY WHEN EDITING THIS SHEET
real_deal = '131Y_PxkJgibJ117fsQrfc79lVi6MLGWfCBBJvrdQuN8'
#USE THIS SHEET TO TEST 
test = '12yV42AFnUecXFXwaLUpz6Hqh9VpRp6gtap8x6xEAp7U'
        
spreadsheet_id = test
    
def initialize():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           #print('hi')
           creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    service = build('sheets', 'v4', credentials=creds)
    return service

service = initialize()

#so this solution is technically fine BUT it exceeds the API quota
#so instead I'm going to do a batch read an dump
def fix_sheet_old():
    result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range='A:H').execute()
    existing_urls = []
    count = 1
    numRows = result.get('values') if result.get('values')is not None else 0
    for row in numRows:
        count += 1
        print(count)
        url = row[2]
        cleaned = truncate(url)
        if cleaned not in existing_urls:
            existing_urls.append(cleaned)
            write_row(count, [[cleaned]])
        else:
            highlight_row(count)

def write_row(r, values):
    body = {
            'values': values
    }
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range='C'+str(r)+':C'+str(r),
        valueInputOption='RAW', body=body).execute()

def highlight_row(r):
    requests = [
        {
        "repeatCell": {
        "range": {
          "sheetId": 0,
          "startRowIndex": r,
          "endRowIndex": r
        },
        "cell": {
          "userEnteredFormat": {
            "backgroundColor": {
              "red": 0.5,
              "green": 0.0,
              "blue": 0.0
            }
        }
            },
       "fields": '*'
        }
        }
      ]
    body = {
    'requests': requests
    }
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body).execute()

def is_bad(entry):
    entry == "TODO" or entry == 'None' or entry == 'none' or entry == '' or entry == 'na' or entry == 'NA'

#returns a dictionary of cleaned and deduped rows in url:row format
#each row is a string list with one element per cell
#also returns overlapping cells in url:range format (range is an int)
def fix_sheet_old():
    result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range='A:H').execute()
    existing = {}
    overlap_range = {}
    count = 1
    numRows = result.get('values') if result.get('values')is not None else 0
    for row in numRows:
        count += 1
        url = truncate(row[2])
        if url not in existing:
            cleaned_row = [url if i == 2 else row[i] for i in range(row)]
            existing.append({url: cleaned_row})
        else:
            old_row = existing[url]
            new_row = [row[i] if is_bad(old_row[i]) else old_row[i] for i in range(row)] 
            existing.update({url: new_row})
            overlap_range.update({url: count})
    return existing, overlap_range
    
            
if __name__ == '__main__':
    fix_csv(sys.argv[1], sys.argv[2])