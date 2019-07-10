#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 16:52:11 2019

@author: lavanyasingh
"""


import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import helpers

os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

#BE VERY CAREFULY WHEN EDITING THIS SHEET
#ONLY EDIT HERE AFTER THOROUGH TESTING
real_deal = '131Y_PxkJgibJ117fsQrfc79lVi6MLGWfCBBJvrdQuN8'
#USE THIS SHEET TO TEST 
test = '12yV42AFnUecXFXwaLUpz6Hqh9VpRp6gtap8x6xEAp7U'
        
spreadsheet_id = real_deal
    


service = initialize()


def is_bad(entry):
    entry == "TODO" or entry == 'None' or entry == 'none' or entry == '' or entry == 'na' or entry == 'NA'


#returns a dictionary of cleaned and deduped rows in url:row format
#each row is a string list with one element per cell
#also returns total number of rows
#also returns number of overlaps
def fix_sheet():
    result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range='A:H').execute()
    existing = {}
    count = 1
    overlap = 0
    numRows = result.get('values') if result.get('values')is not None else 0
    for row in numRows:
        count += 1
        try:
            url = truncate(row[2])
            new_row = []
            if url not in existing:
                for i in range(9):
                    try:
                        if i  == 2: new_row.append(url)
                        else: new_row.append(row[i])
                    except IndexError:
                        new_row.append("")                                        
            else:
                overlap +=1
                old_row = existing[url]
                for i in range(9):
                    try:
                        cell = row[i] if is_bad(old_row[i]) else old_row[i]
                        new_row.append(cell)
                    except IndexError:
                        new_row.append("") 
            existing.update({url: new_row})
        except IndexError:
            print(count)
            None
    return existing, count, overlap
    
def dict_to_list(d):
    values = []
    for item in d:
        values.append(d[item])
    return values
        
def write_fixes():
    existing, total, overlap = fix_sheet()
    print('total', total)
    print('overlap', overlap)
    #clearing the sheet
    empty = [["" for i in range(9)] for n in range(total)]
    write_values(empty)
    #writing the cleaned values
    write_values(dict_to_list(existing))


#a function to write values to a sheet
def write_values(values):
    body = {
            'values': values
    }
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range='A:J',
        valueInputOption='RAW', body=body).execute()

if __name__ == '__main__':
    write_fixes()