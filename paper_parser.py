import os
import re
import json

maindir = '.'

urls = set()

channeldirs = [i for i in os.listdir(maindir) if '.' not in i]

for channeldir in channeldirs:
    filenames = os.listdir(channeldir)

    for filename in filenames:
        with open(os.path.join(channeldir, filename), 'r') as f:
            data = json.load(f)

        # Bless nested list comprehensions and regex
        urls.update([url for thread in data for url in
                     re.findall("(https?://[^\s]+)", thread['text'])
                     if 'http' in thread['text']])

# Cleaning for weird characters at end of URL
urls = list(urls)
checkup = [1]
forbidden = ';),.>'

while sum(checkup) > 0:
    for i, url in enumerate(urls):
        for char in forbidden:
            if url.endswith(char):
                url = url[:-1]
        urls[i] = url
    checkup = [sum([url.endswith(char) for char in forbidden]) for url in urls]

kwords = ['article',
          'rxiv.org',
          'doi.org',
          'embopress.org',
          'cell.com',
          'pnas.org',
          'acs.org',
          'sciencemag.org',
          'nature.com',
          'springer.com', ]
