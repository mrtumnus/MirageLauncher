#!/bin/python
# Author:   Elliott Partridge
# Date:     2017-03-28
"""Python launcher script for Mirage Realms MMORPG"""

import os
from urllib.request import urlopen, URLError, HTTPError, Request
from datetime import datetime, timedelta

mirage_url = 'http://www.miragerealms.co.uk/downloads/Mirage.jar'
mirage_file = os.path.basename(mirage_url)

# From http://stackoverflow.com/a/4028894/973624
def get_url(url):
    """Download a URL resource"""
    # Open the url
    try:
        f = urlopen(url)
        print ("Downloading " + url)

        # Open our local file for writing
        with open(os.path.basename(url), "wb") as local_file:
            local_file.write(f.read())

    # Handle errors
    except HTTPError as e:
        print ("HTTP Error:", e.code, url)
    except URLError as e:
        print ("URL Error:", e.reason, url)

def get_url_info(url):
    """Retrieve headers for a URL"""
    # Get URL headers only
    # derived from http://stackoverflow.com/a/4421485/973624
    request = Request(url)
    request.get_method = lambda : 'HEAD'
    response = urlopen(request)
    
    return response.info()
    
def get_url_mtime(url):
    """Get the Last-Modified header for a URL as a datetime"""
    url_info = get_url_info(url)
    
    # Parse Last-Modified time
    # https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    mod_time_str = url_info['Last-Modified']
    mod_time = datetime.strptime(mod_time_str, '%a, %d %b %Y %H:%M:%S %Z')
    
    return mod_time
    

if __name__ == "__main__":
    # Check if file exists
    if os.path.isfile(mirage_file):
        # Get modification times
        url_mtime = get_url_mtime(mirage_url)
        file_mtime = datetime.utcfromtimestamp(os.path.getmtime(mirage_file))
        
        # Check if URL time is newer than file (with some wiggle room)
        if (url_mtime > file_mtime + timedelta(0,30)):
            print('New version detected')
            # URL is newer - download and replace file
            get_url(mirage_url)
        else:
            print('File up to date')
    else:
        # File does not exists
        print('File does not exist')
        # URL is newer - download and replace file
        get_url(mirage_url)
        
    # Launch program
    os.system('start ' + mirage_file)
