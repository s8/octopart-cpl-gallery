# sites to crawl:
# http://hackaday.com/
# http://dangerousprototypes.com/


# partlists:
# http://dangerousprototypes.com/docs/Bus_Pirate_v3.6

from bs4 import BeautifulSoup

import requests

r = requests.get('http://hackaday.com/')

r = requests.get('http://hackaday.com/about/')

cache = {'http://hackaday.com/': str(r.content)}

# print cache

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
        	print '>>> adding page: ' + str(page)
        	content = get_page(page)
        	add_page_to_index(index, page, content)
        	outlinks = get_all_links(content)
        	graph[page] = outlinks
        	union(tocrawl, outlinks)
        	crawled.append(page)
    return index, graph

def get_page(url):
	print '>>> >>> looking for url: ' + str(url)
	if url in cache:
		print '>>> >>> >>> ' + str(url) + ' >>> is in cache'
		return cache[url]
	else:
		print '>>> >>> >>> ' + str(url) + ' >>> is NOT in cache'
		page = requests.get(url).content
		cache[url] = page
		return cache[url]
    
def get_next_target(page):
    start_link = page.find('href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

# print get_next_target(str(r.content))

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

# print get_all_links(r.content)

def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
        
def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

index, graph = crawl_web('http://hackaday.com/')

