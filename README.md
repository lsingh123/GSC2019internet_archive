# GSCO19internet_archive

## Fuseki Starter Kit

https://docs.google.com/document/d/1rY32moyAVndtINysWYF5c5rhRtSX6OyTH5rkGc6vzoQ/edit#

## Conventions:

**CSV's** that we write to have the following columns: ['country', 'source url', 'title', 'language', 'type']

**ROW**: Title, Title (english not available), URL, Type, Paywall, Source, Language, Country

**TRUNCATED URLS** are in the form [optional].domain.TLD.[optional]

An entry **ISBAD** if it is empty, None, NA, or TODO

**SPREADSHEET_ID**: test = test sheet, real_deal = the real sheet

## Dependencies

**Python**

Media Cloud:

``` pip install mediacloud ```

Matplotlib:

``` pip install matplotlib ```

Venn:

``` pip install matplotlib_venn ```

**Java**

https://github.com/google/guava

http://opencsv.sourceforge.net/

*Open CSV has its own dependencies and transitive dependencies (dependencies of the dependencies)*

## Collections

These scripts collect media sources from various metasources indicated in the
file name. To run each script:

``` python filename ```

The data will be stored in csv files in the data folder with 5 columns:
country, url, title, language, type

### Writing to Sheet

To write to the Google Sheet, use `write_to_sheet.py`. This script dedupes at the time of writing.

**IMPORTANT NOTE** Please do not write directly to the official World News Sources sheet. Test your code on the copy sheet. To switch between the two, just set the `spreadsheet_id` variable to either `test` or `real_deal`

To run this script:

```python write_to_sheet.py input_filename sourcename```

## Visualizations

These scripts create various visualizations of news source data.

### Compare

`compareV3.py` and `compareV4.py` generate venn diagrams of overlaps between various metasources. **Note** these scripts are incredibly messy and need to be more rigorously tested. 

`compareV2.py` generates bar graphs of counts of sources per country. Also messy, no longer in use but included for reference.

## Meta

These scripts handle metadata and cleaning.

### Clean

These scripts go back to the Google Sheet and clean and dedupe the data. 

**IMPORTANT NOTE** Please do not write directly to the official World News Sources sheet. Test your code on the copy sheet. To switch between the two, just set the `spreadsheet_id` variable to either `test` or `real_deal`

## Helpers

`helpers.py` contains helper functions. `truncate(url)` takes in an URL as an argument and returns a canonicalized version of the URL. **Please do not write your own canonicalization function.** Use this function instead. Other helper functions in this file perform various string cleaning operations, read data in various formats from a CSV, and read/write to a Google Sheet.

## Exploration

These scripts are me getting more familiar with various tools. If you would like to explore/get familiar with the various APIs we use, please use this folder to store your scripts.
