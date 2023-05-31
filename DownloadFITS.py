import os
import requests
from bs4 import BeautifulSoup

# The URL of the directory containing the files.
url = "https://archive.stsci.edu/missions/tess/ffi/s0020/2020/001/1-1/"

# Make a request to the website
r = requests.get(url)
r.raise_for_status()

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(r.text, 'html.parser')

# Find all links on the webpage
links = soup.find_all('a')

# Download the .fits files
for link in links:
    href = link.get('href')
    if href.endswith('.fits') and ('ffic' in href):
        # Complete the URL if it's a relative URL
        if not href.startswith('http'):
            href = url + href
        # Send a new request to download the file
        r = requests.get(href, stream=True)
        r.raise_for_status()

        # Write the file
        with open(os.path.join("FITS2020", href.split('/')[-1]), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)