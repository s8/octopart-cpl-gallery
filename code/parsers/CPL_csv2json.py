import csv
import cPickle as pickle

# opening the file in the 'universal newline mode', hence the 'U' option
octopartCPL_csv_bom = open('../../data/parts_lists/Common Parts Library BOM.csv', 'rU')

def csv2dict_cpl(input_csv_file):
    """ Convert csv file into dictionary"""
    dict_from_csv = []
    csv_reader = csv.DictReader(input_csv_file)
    for line_item in csv_reader:
        entry = {}
        for item in line_item:
            key = str(item).strip()
            value = str(line_item[item]).strip()
            if key == 'MPN':
                entry['mpn'] = value
            if key == 'Manufacturer':
                entry['brand'] = value
        dict_from_csv.append(entry)
    return dict_from_csv

cpl_bom = csv2dict_cpl(octopartCPL_csv_bom)

with open ('../../data/parts_lists/cpl_bom.json', 'wb') as fp:
    pickle.dump(cpl_bom, fp)

with open ('../../data/parts_lists/cpl_bom.json', 'rb') as fp:
    cpl_bom = pickle.load(fp)

for entry in cpl_bom:
    print '------------------------------------'
    print entry