import csv
import cPickle as pickle


seeedOPL_CSV_bom = open('../../data/parts_lists/OPL list20141222.csv', 'r')


def csv2dict_seeed(input_csv_file):
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

seeedOPL_bom = csv2dict_seeed(seeedOPL_CSV_bom)

with open('../../data/boms/seeedOPL_bom.json', 'wb') as fp:
    pickle.dump(seeedOPL_bom, fp)

with open('../../data/boms/seeedOPL_bom.json', 'rb') as fp:
    seeedOPL_bom = pickle.load(fp)

for entry in seeedOPL_bom:
    print '------------------------------------'
    print entry
