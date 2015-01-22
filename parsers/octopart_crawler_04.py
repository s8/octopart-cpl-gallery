# 1. crawl pages and build page index and grap
# 2. rank pages according tso the amount of mentioned terms
# 3. if parts lists are available as .sch or .csv - download them and attempt to parse
# 4. if page rank is high, but not automatically parseable - put it into "to be parsed manually" dictionary
# 5. compare parsed lists against the CPL and generate several ratings according to the availability and price
# 6. generate a project entry for the gallery.


# rate BOMs against the parts list
def rate_bom(bom, common_parts_list):
	bom_rating = {'price rating':0, 'availability rating':0}
	return bom_rating

# try to parse a BOM
def parse_bom(parts_list):
	
	parsed_list = 'empty parsed list'
	if csv:
		parsed_list = parse_csv(parts_list)
	if sch:
		parsed_list = parse_sch(parts_list)


	return parsed_list

#  find and return BOMS from the apge.
def get_boms(page):
	
	boms_list = {'empty boms list':0}

	return boms_list

def get_all_links(page):
	links_list = []
	return links_list

def union(list1, list2):
	for i in list2:
		if i not in list1:
			list1.append(i)

# crawl from the seed url
def crawl_url(seed_url, depth):
	to_crawl = [seed]
	crawled = []
	page_index = {} # {'empty index':0}
	page_graph = {} # {'empty graph':0}
	page_rating = {} # {'empty rating':0}
	boms = {} # 

	while to_crawl:
		page = to_crawl.pop()
		if page not in crawled:
			content = requests.get(page).text
			boms[page] = get_boms(page)
			outlinks = get_all_links(page)
			graph[page] = outlinks
			union(to_crawl, outlinks)
			crawled.append(page)

	return page_index, page_graph, page_rating, boms


def publish_documentation(pictures, parts_list, rating, url):
	page = 'empty page'
	return page



