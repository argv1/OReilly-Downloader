#!/usr/bin/env python3
'''
    O'Reilly provide on their websie some free available ebooks.
    Sme links are not shown on their page anylonger, but the ebooks are still available
    The script checks if there are deadlinks, new books available and store everything in a csv file
'''

import argparse
import os
import pandas as pd
from   pathlib import Path
import re
import requests
import time

# time delay between requests 
time_delay = 1

# input and output
base_path = Path('H:\OneDrive\Programme\_current\OReilly-Downloader')  #adjust
link_file = base_path / 'links.csv'  
deprecated_urls = base_path / 'deprecated.csv'  
html_file = base_path / 'ebook_overview.html'  

def add_new(df, url_file):
    '''
        Enter new ebook links via file, one URL per line
    '''
    with open(url_file, "r", encoding="iso-8859-15") as f:
        lines = f.readlines()
        lines.sort()
    lines = sorted(list(set(lines)))
    c, n = 0, 0

    pattern0 = re.compile(r'(https://www\.oreilly\.com/.*/.*/.*/.*)\.(\bpdf\b|\bepub\b|\bmobi\b)')

    for entry in lines:
        c+=1
        # check if ebook already in df
        match =  re.search(pattern0, entry)

        # if ebook is new, check if available for download
        if match and df[df['base_url'].str.match(match.group(1))].shape[0] == 0:
            url = f"{match.group(1)}.pdf"
            r = requests.head(url)

            # politely wait
            time.sleep(time_delay)

            # if online add additional information (book_title, category, status)
            if str(r) == "<Response [200]>":
                n+=1
                pattern1 = re.compile(r'https://www\.oreilly\.com/.*/(.*)\.(\bpdf\b|\bepub\b|\bmobi\b)')
                pattern2 = re.compile(r'https://www\.oreilly\.com/(.*)/.*/.*/.*')
                
                title =  re.search(pattern1, url)  
                category =  re.search(pattern2, url)   

                new_url_entries = { "book_title": title.group(1),
                               "category": category.group(1),
                               "base_url": match.group(1),
                               "status" : "online"
                            }

                df = df.append(new_url_entries, ignore_index=True)
    print(f"{c} URLs found, {n} new, online ebooks added.\n")
    return(df)

def check_links(df):
    '''
        check if each ebook is still online, otherwise flag ebook as offline
    '''
    cleaning = False

    for idx, _ in df.iterrows():
        url = f"{df.loc[idx, 'base_url']}.pdf"
        r = requests.head(url)
        if str(r) != "<Response [200]>":
            df.loc[idx, 'status'] = "offline"
            cleaning = True
        else:
            df.loc[idx, 'status'] = "online"

        # politely wait
        time.sleep(time_delay)

    return(df, cleaning)

def create_html(html_df):
    '''
        create an html overview to download the ebooks easily
    '''
    # prep html_df
    for idx, _ in html_df.iterrows():
        html_df['pdf'] = f"<a href='{html_df.loc[idx, 'base_url']}.pdf'>pdf</a>"
        html_df['epub'] = f"<a href='{html_df.loc[idx, 'base_url']}.epub'>epub</a>"
        html_df['mobi'] = f"<a href='{html_df.loc[idx, 'base_url']}.mobi'>mobi</a>"

    html_df  = html_df[html_df['status'] == "online"]
    html_df.drop("status", axis=1, inplace=True)

    html_table = html_df.to_html(escape=False)
    with open(html_file, "w", encoding="utf-8") as f:
        for line in html_table:
            f.write(line)      

def clean_list(df):
    '''
        remove offline ebooks from links.csv and create an updated deprecated.csv 
    '''
    dep = df[df['status'] == "offline"]
    df  = df[df['status'] == "online"]

    # create deprecated_urls file if not existing
    if deprecated_urls.is_file():
        dep.to_csv(deprecated_urls, mode='a', encoding="iso-8859-15", index=False)

    else:
        dep.to_csv(deprecated_urls, encoding="iso-8859-15", index=False)

    return(df)

def main():
    # Initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', help='A = Add new urls via file, C = check links, D = create html file', type=str, required=True)   
    parser.add_argument('-f', '--file', help='Filename to mass add new urls', type=str)     
    args = parser.parse_args()
    mode = args.mode
    if args.file:
        url_file = base_path / args.file 
    elif not args.file and mode == "A" or args.file and not args.mode:
        mode = "Z"
        print("If you want to add new urls, you need to call -m A and -f FILENAME.")

    cleaning = False

    # Read csv file and create DataFrame
    df = pd.read_csv(link_file, encoding="iso-8859-15")

    if   mode == "A": df = add_new(df, url_file)
    elif mode == "C": df, cleaning = check_links(df)
    elif mode == "D": create_html(df)
    elif mode == "N": df = check_new(df)

    if cleaning: df = clean_list(df)

    df.to_csv(link_file, encoding="iso-8859-15", index=False)

if __name__ == "__main__":
    main()
