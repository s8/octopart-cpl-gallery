import csv
import cPickle as pickle


arduino_csv_bom = open('../../data/boms/arduino_bom.csv', 'r')

def csv2dict_arduino(input_csv_file):
    """ Convert csv file into dictionary"""
    dict_from_csv = []
    csv_reader = csv.DictReader(input_csv_file)
    for line_item in csv_reader:
        entry = {}
        for item in line_item:
            key = str(item).strip()
            value = str(line_item[item]).strip()
            if key == 'Part Number':
                entry['mpn'] = value
            if key == 'Manufacturer':
                entry['brand'] = value
        dict_from_csv.append(entry)
    return dict_from_csv

arduino_bom = csv2dict_arduino(arduino_csv_bom)

with open ('../../data/boms/arduino_bom.json', 'wb') as fp:
    pickle.dump(arduino_bom, fp)

with open ('../../data/boms/arduino_bom.json', 'rb') as fp:
    arduino_bom = pickle.load(fp)

for entry in arduino_bom:
    print '------------------------------------'
    print entry