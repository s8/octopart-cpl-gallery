#
# Octopart CPL scraper.
# Intended to be used from command line with '>>' operator
# for example: pytho octopart_cpl_scraper_01.py >> elements.txt
#

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

root_url = 'http://octopart.com'
index_url = root_url + '/common-parts-library'

driver = webdriver.Chrome()
driver.get(index_url)
assert "Common" in driver.title
elements = driver.find_elements_by_class_name("subrow")
elements_text = []
for i in elements:
    e = []
    e.append(i.get_attribute('data-section'))
    e.append(i.get_attribute('data-manufacturer'))
    e.append(i.get_attribute('data-mpn'))

    elements_text.append(e)

driver.close