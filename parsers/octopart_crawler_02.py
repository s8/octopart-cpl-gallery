x# sites to crawl:
# http://hackaday.com/
# http://dangerousprototypes.com/


# partlists:
# http://dangerousprototypes.com/docs/Bus_Pirate_v3.6

import requests
import os
import time
from bs4 import BeautifulSoup

# hackaday_cache = 'hackaday_cache.txt'
url = 'hackaday.com'

def get_cache_age(cache_file):
	current_time = time.time()
	last_updated = os.path.getmtime(cache_file)
	return current_time - last_updated

def update_cache(cache_file):
	cache = open(cache_file, 'w')
	r = requests.get("http://" + url)
	data = r.text
	soup = BeautifulSoup(data)

	for link in soup.find_all('a'):
		cache.write(link.get('href'))
		cache.write('\n')

	cache = open(cache_file, 'r')

	return cache

def gimme_cache(url):

	new_cache = False
	cache_file = url + '.txt'
	
	try:
		cache = open(cache_file, 'r')
	except IOError:
		cache = open(cache_file, 'w')
		new_cache = True

	cache_age = get_cache_age(cache_file)

	if cache_age > 300 or new_cache:
		new_cache = False		
		cache = update_cache(cache_file)


	else:
		print 'the cache is %s second YOUNG' % round(cache_age, 1)

	return cache

print gimme_cache(url)

