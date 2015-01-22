# 1. go to the page
# 2. collect all links
# 3. check the contents against the keyword dictionary
# 4. rank the pages according to keyword contents
# 5. group external links in a separate dictionary

# sites to crawl:
# http://hackaday.com/
# http://hackaday.io/
# http://dangerousprototypes.com/
# http://www.theledart.com/
# http://www.instructables.com/
# http://arduino.cc/
# https://github.com/
# http://people.ece.cornell.edu/land/courses/ece4760/
# http://fabacademy.org/archive/
# http://seeedstudio.com
# http://www.weirdlab.fr/
# http://fw.hardijzer.nl/

# other sites of interest:

# kickstarter projects:
# https://www.kickstarter.com/projects/mossmann/hackrf-an-open-source-sdr-platform


# partlists:
# http://dangerousprototypes.com/docs/Bus_Pirate_v3.6
# https://greatscottgadgets.com/tc13badge/tc13badge-kit-parts.pdf

# BOM's
# https://github.com/mossmann/hackrf/blob/master/doc/hardware/hackrf-one-bom.csv
# https://docs.google.com/spreadsheets/d/11RTZvoxy8NDVNH0rqRNsO86LkCeCrhs6zsusw9pf6KE/edit#gid=46576701

# KiCad .sch documents with BOM's
# https://github.com/greatscottgadgets/ubertooth/blob/master/hardware/broccoli/broccoli.sch

import requests
import os
import time
import json
from bs4 import BeautifulSoup

url = 'hackaday.com'

large_cache = {}

def get_cache_age(cachepath):
	current_time = time.time()
	last_updated = os.path.getmtime(cachepath)
	return current_time - last_updated

def scrape_page(url,):
	data = requests.get(url).text

def update_cache(url):
	cache = {}
	data = requests.get("http://" + url).text
	soup = BeautifulSoup(data)

	for link in soup.find_all('a'):
		cache[link.get('href')] = '<<<nothing here yet>>>'

	return cache

def get_cache(url):
	
	max_age = 300
	cache_path = url + '.cache.json'
	
	try:
		cache_file = open(cache_path, 'r')
		cache_age = get_cache_age(cache_path)
	except IOError:
		cache_age = max_age + 1


	if cache_age > max_age:
		print "+++ REFRESHING CACHE +++"
		cache_file = open(cache_path, 'w')
		cache = update_cache(url)
		json.dump(cache, cache_file)
	else:
		cache = json.load(cache_file)

	return cache

def get_all_links(content):
	links = []
	soup = BeautifulSoup(content)
	for link in soup.find_all('a'):
		lins.append(link)
	return links


# def add_page_to_index(index, url, content):
#     words = content.split()
#     for word in words:
#         add_to_index(index, word, url)

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            # content = get_page(page)
            content = requests.get(page).text

            # add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph


cache = get_cache(url)

for i in cache:
	if 'http://hackaday.com' in i:
		print i