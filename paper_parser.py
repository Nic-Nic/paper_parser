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
    filenames = os.listdir(channeldir)

    for filename in filenames:
        with open(os.path.join(channeldir, filename), 'r') as f:
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
