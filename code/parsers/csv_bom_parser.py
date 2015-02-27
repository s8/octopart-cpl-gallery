# TODO
# make components comparison case-insensitive
# NRF51822-QFAA-T == nRF51822

import io
import json
import csv


def save_json(filename, data):
    """ serialize dictionary into json and save it to disk
    """
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))


def load_json(filename):
    """ read json file from disk into a dictionary
    """
    with io.open(filename, encoding='utf-8') as f:
        return json.loads(f.read())


def csv2dict(input_csv_file):
    """ read csv file from disk and parse it into a dictionary
        data structure implemented here is a list of dictionaries
        [
            {'mpn':'...', 'brand':'...'},
            {...},
            {...},
            ...
        ]
    """
    # different strings for the same field in different csv boms
    mpn_csv_fields = ['MPN', 'Manufactuer Part number', 'Part Number']
    brand_csv_fields = ['Manufacturer', 'Manufactuer Name']

    with io.open(input_csv_file, 'r', encoding='utf-8') as f:
        dict_from_csv = []
        csv_reader = csv.DictReader(f)
        for line_item in csv_reader:
            entry = {}
            for item in line_item:
                key = str(item).strip()
                value = str(line_item[item]).strip()
                if len(value) > 0 and len(key) > 0:
                    if key in mpn_csv_fields:
                        entry['mpn'] = value
                    if key in brand_csv_fields:
                        entry['brand'] = value
            if len(entry) > 0:
                dict_from_csv.append(entry)
        return dict_from_csv


def match_boms(bom_01, bom_02):
    """ find matches between two boms """
    matches = []
    coverage = 0.0
    for part_01 in bom_01:
        for part_02 in bom_02:
            try:
                if part_01['mpn'] == part_02['mpn']:
                    matches.append(part_01)
            except KeyError:
                continue
    coverage = float(len(matches)) / len(bom_02)
    return matches, coverage


if __name__ == ('__main__'):
    """ open csv file, parse it into a dict and save as a json """

    data_folder = '../../data/boms/'

    seeedOPL_CSV_file = data_folder + 'csv/OPL list20141222.csv'
    seeedOPL_JSON_file = data_folder + 'formatted_jsons/seeedOPL.json'
    save_json(seeedOPL_JSON_file, csv2dict(seeedOPL_CSV_file))
    seeed_opl = load_json(seeedOPL_JSON_file)

    octopartCPL_CSV_file = data_folder + 'csv/Common Parts Library BOM.csv'
    octopartCPL_JSON_file = data_folder + 'formatted_jsons/octopartCPL.json'
    save_json(octopartCPL_JSON_file, csv2dict(octopartCPL_CSV_file))
    octopart_cpl = load_json(octopartCPL_JSON_file)

    arm_BOM_CSV_file = data_folder + 'csv/arm-pro-mini-bom.csv'
    arm_BOM_JSON_file = data_folder + 'formatted_jsons/arm-pro-mini-bom.json'
    save_json(arm_BOM_JSON_file, csv2dict(arm_BOM_CSV_file))
    arm_BOM = load_json(arm_BOM_JSON_file)

    arduino_BOM_CSV_file = data_folder + 'csv/arduino_bom.csv'
    arduino_BOM_JSON_file = data_folder + 'formatted_jsons/arduino_bom.json'
    save_json(arduino_BOM_JSON_file, csv2dict(arduino_BOM_CSV_file))
    arduino_BOM = load_json(arduino_BOM_JSON_file)

    print ("================================================================")
    print ('octopart: ' + str(len(octopart_cpl)) + ' elements')
    print ("----------------------------------------------------------------")
    print (octopart_cpl)

    print ("================================================================")
    print ('seeed: ' + str(len(seeed_opl)) + ' elements')
    print ("----------------------------------------------------------------")
    print (seeed_opl)

    print ("================================================================")
    print ('arm: ' + str(len(arm_BOM)) + ' elements')
    print ("----------------------------------------------------------------")
    print (arm_BOM)

    print ("================================================================")
    print ('arduino: ' + str(len(arduino_BOM)) + ' elements')
    print ("----------------------------------------------------------------")
    print (arduino_BOM)

    # Match three boms against CPL
    arm_cpl_matches, arm_cpl_coverage = \
        match_boms(octopart_cpl, arm_BOM)
    seeed_cpl_matches, seeed_cpl_coverage = \
        match_boms(octopart_cpl, seeed_opl)
    arduino_cpl_matches, arduino_cpl_coverage = \
        match_boms(octopart_cpl, arduino_BOM)

    arm_opl_matches, arm_opl_coverage = \
        match_boms(seeed_opl, arm_BOM)
    octopart_opl_matches, octopart_opl_coverage = \
        match_boms(seeed_opl, octopart_cpl)
    arduino_opl_matches, arduino_opl_coverage = \
        match_boms(seeed_opl, arduino_BOM)

    print ("================================================================")
    print ("================  OCTOPART CPL MATCHES  ========================")
    print ("================================================================")
    print ('ArmProMini: covered %.2f percent of parts' %
           (arm_cpl_coverage * 100))
    print ([i['mpn'] + ' : ' + i['brand'] for i in arm_cpl_matches])
    print ('----------------------------------')
    print ('Arduino: covered %.2f percent of parts' %
           (arduino_cpl_coverage * 100))
    print ([i['mpn'] + ' : ' + i['brand'] for i in arduino_cpl_matches])
    print ('----------------------------------')
    print ('Seeed OPL: covered %.2f percent of parts' %
           (seeed_cpl_coverage * 100))
    print([i['mpn'] + ' : ' + i['brand'] for i in seeed_cpl_matches])
    print ('----------------------------------')

    print ("================================================================")
    print ("=================    SEEED OPL MATCHES    ======================")
    print ("================================================================")
    print ('ArmProMini: covered %.2f percent of parts' %
           (arm_opl_coverage * 100))
    print([i['mpn'] + ' : ' + i['brand'] for i in arm_opl_matches
          if 'brand' and 'mpn' in i])
    print ('----------------------------------')
    print ('Arduino: covered %.2f percent of parts' %
           (arduino_opl_coverage * 100))
    print([i['mpn'] + ' : ' + i['brand'] for i in arduino_opl_matches
          if 'brand' and 'mpn' in i])
    print ('----------------------------------')
    print ('Octopart CPL: covered %.2f percent of parts' %
           (octopart_opl_coverage * 100))
    print([i['mpn'] + ' : ' + i['brand'] for i in octopart_opl_matches
          if 'brand' and 'mpn' in i])
    print ('----------------------------------')
