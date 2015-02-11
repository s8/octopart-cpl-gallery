import json
import urllib

queries = [
    {'mpn': 'SN74S74N',
     'reference': 'line1'},
    {'sku': '67K1122',
     'reference': 'line2'},
    {'mpn_or_sku': 'SN74S74N',
     'reference': 'line3'},
    {'brand': 'Texas Instruments',
     'mpn': 'SN74S74N',
     'reference': 'line4'}
    ]

url = 'http://octopart.com/api/v3/parts/match?queries=%s' \
    % urllib.quote(json.dumps(queries))
url += '&apikey=EXAMPLE_KEY'

data = urllib.urlopen(url).read()
response = json.loads(data)

# print request time (in milliseconds)
print response['msec']

# print mpn's
for result in response['results']:
    print "Reference: %s" % result['reference']
    for item in result['items']:
        print item['mpn']
