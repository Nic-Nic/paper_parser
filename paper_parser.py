# Copyright (C) 2020 Nicolàs Palacio
#
# Contact: nicolas.palacio@bioquant.uni-heidelberg.de
#
# GNU-GLPv3:
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# A full copy of the GNU General Public License can be found on
# http://www.gnu.org/licenses/.
#
# Article URL parser
# ==================
#
# The following script parses all files in all subfolders of the
# specified main directory (e.g. Slack archive files) and extracts any
# URL related/pointing to a scientific article.
# DISCLAIMER: Performance of the extraction is highly dependent on the
# provided excluder and includer keywords below

import os
import re

#==================================# INPUT #==================================#
maindir = 'slack_archive'
outfile = 'articles.txt'
exclude = ['github', 'slack', 'twitter', 'youtube', 'youtu.be', 'google',
           'stackoverflow']
exclude_endswith = ['.png', '.jpg', '.jpeg', '.ico']
kwords = ['article', 'rxiv.org', 'doi.org', 'embopress.org', 'cell.com',
          'pnas.org', 'acs.org', 'sciencemag.org', 'nature.com',
          'springer.com', 'full', 'fulltext', 'ncbi.nlm.nih.gov', 'mdpi.com',
          'mcponline.org', 'sciencedirect.com', 'springer', 't.co/']
#=============================================================================#

urls = set()

channeldirs = [i for i in os.listdir(maindir) if '.' not in i]

# Find ANY URL (e.g. embedded tweets, replies, etc)
# -> parsing JSONs as plain text
for channeldir in channeldirs:
    filenames = os.listdir(os.path.join(maindir, channeldir))

    for filename in filenames:
        with open(os.path.join(maindir, channeldir, filename), 'r') as f:
            # Removing escape character
            plaintxt = f.read().replace('\\', '')
            # Extracting urls
            extracted = [url.split('>')[0] for url
                         in re.findall('(https?://[^\s]+)', plaintxt)]
            urls.update(extracted)

# Cleaning for weird characters at end of URL
urls = list(urls)
checkup = [1]
forbidden = '";),.>'
while sum(checkup) > 0:
    for i, url in enumerate(urls):
        for char in forbidden:
            if url.endswith(char):
                url = url[:-1]
        urls[i] = url
    checkup = [sum([url.endswith(char) for char in forbidden]) for url in urls]

# Removing duplicates
urls = list(set(urls))

# Removing what's surely not an article
urls = [url for url in urls
        if (sum([i in url for i in exclude]) == 0
            and sum([url.endswith(i) for i in exclude_endswith]) == 0)]

# Selecting URLs containing keywords
selected = [url for url in urls if sum([i in url for i in kwords]) > 0]

# Save the URL list
with open(outfile, 'w') as f:
    f.write('\n'.join(selected))
