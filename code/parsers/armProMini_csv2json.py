import csv
import cPickle as pickle


arm_pro_mini_CSV_bom = open('../../data/boms/arm-pro-mini-bom.csv', 'rU')


def csv2dict_arduino(input_csv_file):
    """ Convert csv file into dictionary"""
    dict_from_csv = []
    csv_reader = csv.DictReader(input_csv_file)
    for line_item in csv_reader:
        entry = {}
        for item in line_item:
            key = str(item).strip()
            value = str(line_item[item]).strip()
            if key == 'Manufactuer Part number':
                entry['mpn'] = value
            if key == 'Manufactuer Name':
                entry['brand'] = value
        dict_from_csv.append(entry)
    return dict_from_csv

arm_pro_mini_bom = csv2dict_arduino(arm_pro_mini_CSV_bom)

with open('../../data/boms/arm_pro_mini_bom.json', 'wb') as fp:
    pickle.dump(arm_pro_mini_bom, fp)

with open('../../data/boms/arm_pro_mini_bom.json', 'rb') as fp:
    arm_pro_mini_bom = pickle.load(fp)

for entry in arm_pro_mini_bom:
    print '------------------------------------'
    print entry
