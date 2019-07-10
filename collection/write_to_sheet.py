#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:50:46 2019

@author: lavanyasingh
"""

import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
import helpers



SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

#BE VERY CAREFULY WHEN EDITING THIS SHEET
real_deal = '131Y_PxkJgibJ117fsQrfc79lVi6MLGWfCBBJvrdQuN8'
#USE THIS SHEET TO TEST 
test = '12yV42AFnUecXFXwaLUpz6Hqh9VpRp6gtap8x6xEAp7U'
        
spreadsheet_id = real_deal
    
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

#returns existing source URLS and number of populated rows
def existing_sources():
    result = service.spreadsheets().values().get(
            spreadsheetId=test, range='A:H').execute()
    existing_urls = []
    count = 1
    numRows = result.get('values') if result.get('values')is not None else 0
    for row in numRows:
        try:
            existing_urls.append(row[2])
        except IndexError as e:
            print(e)
        count+=1
    return existing_urls, count

def remove_overlaps(old_urls, new):
    good = []
    count = 0 
    for item in new:
        if item['url'] not in old_urls:
            count +=1
            good.append(item)
    print('unique new sources', count)
    return good

def write_sheet(path, metasource):
    values = []
    existing, r = existing_sources()
    sources = helpers.read_sources(path)
    for entry in sources:
        values.append([entry['title'], 'TODO', entry['url'], entry['type'],
                       'TODO', metasource, entry['language'], entry['country']])
    body = {
            'values': values
    }
    service.spreadsheets().values().update(
        spreadsheetId=test, range='A'+str(r)+':H',
        valueInputOption='RAW', body=body).execute()

if __name__ == '__main__':
    path = sys.argv[1]
    source = sys.argv[2]
    write_sheet(path, source)