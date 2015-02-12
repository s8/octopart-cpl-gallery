# refactored example code from https://octopart.com/api/docs/v3/bom-quickstart

import csv
import json
import urllib
from decimal import Decimal

csv_file = open('../../data/boms/arduino_bom.csv', 'r')
api_key = ''

line_items = []
queries = []
hits = 0


def load_csv(input_file):
    """ Convert csv file into line items and queries
        This code assumes a file format similar to the one on the
        Arduino BOM"""

    csv_reader = csv.DictReader(input_file)
    for line_item in csv_reader:
        # Skip line items without part numbers and manufacturers
        if not line_item['Part Number'] or not line_item['Manufacturer']:
            continue
        line_items.append(line_item)
        queries.append({'mpn': line_item['Part Number'],
                        'brand': line_item['Manufacturer'],
                        'reference': len(line_items) - 1})
    return line_items, queries


def match_bom(bom):
    """ Send queries to REST API for part matching. """

    results = []
    for i in range(0, len(bom), 20):
        # Batch queries in groups of 20, query limit of
        # parts match endpoint
        batched_queries = bom[i: i + 20]
        url = 'http://octopart.com/api/v3/parts/match?queries=%s' \
            % urllib.quote(json.dumps(batched_queries))
        url += '&apikey=' + api_key
        data = urllib.urlopen(url).read()
        response = json.loads(data)

        # Record results for analysis
        results.extend(response['results'])
    return results


def price_bom(bom):
    """ Analyze results sent back by Octopart API
        Price BOM """

    hits = 0
    total_avg_price = 0
    for result in bom:
        line_item = line_items[result['reference']]
        if len(result['items']) == 0:
            print "Did not find match on line item %s" % line_item
            continue
        # Get pricing from the first item for desired quantity
        quantity = Decimal(line_items[result['reference']]['Qty'])
        prices = []
        for offer in result['items'][0]['offers']:
            if 'USD' not in offer['prices'].keys():
                continue
            price = None
            for price_tuple in offer['prices']['USD']:
                # Find correct price break
                if price_tuple[0] > quantity:
                    break
                # Cast pricing string to Decimal for precision
                # calculations
                price = Decimal(price_tuple[1])
            if price is not None:
                prices.append(price)

        if len(prices) == 0:
            print "Did not find pricing on line item %s" % line_item
            continue
        avg_price = quantity * sum(prices) / len(prices)
        total_avg_price += avg_price
        hits += 1
    return total_avg_price, hits


if __name__ == '__main__':
    line_items, queries = load_csv(csv_file)
    octopart_results = match_bom(queries)
    print "Found %s line items in BOM." % len(line_items)
    print '---------------------------'
    print octopart_results
    print '---------------------------'
    total_avg_price, hits = price_bom(octopart_results)
    print "Matched on %.2f of BOM, total average price is USD %.2f" % (
        hits / float(len(line_items)), total_avg_price)
