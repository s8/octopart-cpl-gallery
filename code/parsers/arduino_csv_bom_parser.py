import csv
import json
import cPickle as pickle

arduino_csv_bom = open('../../data/boms/arduino_bom.csv', 'r')

line_items = []
queries = []
hits = 0


def load_csv(input_csv_file):
    """ Convert csv file into line items and queries
        This code assumes a file format similar to the one on the
        Arduino BOM"""

    csv_reader = csv.DictReader(input_csv_file)
    for line_item in csv_reader:
        # Skip line items without part numbers and manufacturersm
        if not line_item['Part Number'] or not line_item['Manufacturer']:
            continue
        line_items.append(line_item)
        queries.append({'mpn': line_item['Part Number'],
                        'brand': line_item['Manufacturer'],
                        'reference': len(line_items) - 1})
    return line_items, queries

# lines, queries = load_csv(arduino_csv_bom)

# with open ('arduino_bom.json', 'wb') as fp:
#     pickle.dump(lines, fp)

with open ('arduino_bom.json', 'rb') as fp:
    arduino_bom = pickle.load(fp)

for entry in arduino_bom:
    print '------------------------------------'
    print entry
    
# for line in lines:
#     print '---------------'
#     print line

# print '#########################################################'

# for query in queries:
#     print '---------------'
#     print query

