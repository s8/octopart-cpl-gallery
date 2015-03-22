# TODO
# * make components comparison case-insensitive: NRF51822 == nRF51822
# * make use of os.join operations
# * get rid of jsons - deal directly with csv's
# * strip out special characthers like hyphens
# * make partially-matching components match: NRF51822-QFAA-T == nRF51822
# * get rid of try-excepts
# * add quantity field so that if there's 10x the same part - it should have higher coverage rating
# make two lists - parts that match and parts that don't
# parse 10 more boms
# comment the code better
# make a googledoc with the results

import os
import io
import json
import csv


def clean_mpn(mpn):
    garbage_chars = '~!@#$%^&*()_+-={}[]|:;"<>,./?\\\' '
    # proper_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for i in garbage_chars:
        if i in mpn:
            mpn = mpn.replace(i, '')
    return mpn


def csv2dict(input_csv_file):
    """ read csv file from disk and parse it into a dictionary
        data structure implemented here is a list of dictionaries
        [
            {'mpn':'...', 'brand':'...'},
            {...},
            {...},
            ...
        ]

        refactor (if len(value) > 0 and len(key) > 0:) line
        refactor (if ('mpn' in entry.keys()):) line

        read the docs on DictReader
    """
    print ('parsing %s' % input_csv_file)
    # different strings for the same field in different csv boms
    mpn_csv_fields = ['MPN', 'Manufactuer Part number', 'Part Number']
    brand_csv_fields = ['Manufacturer', 'Manufactuer Name']
    quantity_csv_fields = ['Qty', 'Quantity']

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
                        # cleaning up special symbols
                        entry['mpn'] = clean_mpn(value)
                    if key in brand_csv_fields:
                        entry['brand'] = value
                    if key in quantity_csv_fields:
                        entry['qty'] = value

            # make sure we don't add parts with empty MPN's
            if ('mpn' in entry.keys()):
                # if part was mentioned in the list, but no quantity specified
                # we assume it is used once in the BOM
                if ('qty' not in entry.keys()):
                    entry['qty'] = 1
                dict_from_csv.append(entry)

    return dict_from_csv


def match_boms(reference_bom, target_bom):
    """ 

    bom_01 and bom_02 are lists of dictionaries with [{'brand':'...', 'mpn':'...' }] format
    find matches between two boms


    part coverage is calculated as
    (sum( part * qty )) / ()

    match examples:
        c: 1n4148  r: 1n4148ws7f
        c: ft232rl  r: ft232rlreel
        c: mmbt3904  r: mmbt3904lt1g
        c: nrf51822  r: nrf51822qfaat
    """

    matches = []
    match_part_count = 0
    total_part_count = 0
    coverage = 0.0

    # iterate over the parts in the target bom
    for target_part in target_bom:
        total_part_count += int(target_part['qty'])
        for reference_part in reference_bom:

            c = target_part['mpn'].upper()
            r = reference_part['mpn'].upper()

            # check for over- and under-specified MPN's in both lists
            if (c in r or r in c):
                matches.append(target_part)
                match_part_count += int(target_part['qty'])

    coverage = float(match_part_count / total_part_count)
    return matches, coverage, total_part_count


if __name__ == ('__main__'):
    """ open csv file, parse it into a dict and save as a json """

    data_folder = '../../data/boms/'

    seeedOPL_CSV_file = os.path.join(data_folder, 'csv/OPL list20141222.csv')
    seeed_opl = csv2dict(seeedOPL_CSV_file)

    octopartCPL_CSV_file = os.path.join(
        data_folder, 'csv/Common Parts Library BOM.csv')
    octopart_cpl = csv2dict(octopartCPL_CSV_file)

    arm_BOM_CSV_file = os.path.join(data_folder, 'csv/arm-pro-mini-bom.csv')
    arm_BOM = csv2dict(arm_BOM_CSV_file)

    arduino_BOM_CSV_file = data_folder + 'csv/arduino_bom.csv'
    arduino_BOM = csv2dict(arduino_BOM_CSV_file)

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
    arm_cpl_matches, arm_cpl_coverage, arm_total_parts = \
        match_boms(octopart_cpl, arm_BOM)
    seeed_cpl_matches, seeed_cpl_coverage, seeed_total_parts = \
        match_boms(octopart_cpl, seeed_opl)
    arduino_cpl_matches, arduino_cpl_coverage, arduino_total_parts = \
        match_boms(octopart_cpl, arduino_BOM)

    arm_opl_matches, arm_opl_coverage, arm_total_parts = \
        match_boms(seeed_opl, arm_BOM)
    octopart_opl_matches, octopart_opl_coverage, octopart_total_parts = \
        match_boms(seeed_opl, octopart_cpl)
    arduino_opl_matches, arduino_opl_coverage, arduino_total_parts = \
        match_boms(seeed_opl, arduino_BOM)

    print ("================================================================")
    print ("================  OCTOPART CPL MATCHES  ========================")
    print ("================================================================")

    print ('ArmProMini: covered {:.2f} percent of total {} parts'.format(
           (arm_cpl_coverage * 100), str(arm_total_parts)))

    print ([i['mpn'] + ' : ' + i['brand'] + ' : x' + str(i['qty'])
            for i in arm_cpl_matches])
    print ('----------------------------------')
    print ('Arduino: covered {:.2f} percent of total {} parts'.format(
           (arduino_cpl_coverage * 100), str(arduino_total_parts)))
    print ([i['mpn'] + ' : ' + i['brand'] + ' : x' + str(i['qty'])
            for i in arduino_cpl_matches])
    print ('----------------------------------')
    print ('Seeed OPL: covered {:.2f} percent of total {} parts'.format(
           (seeed_cpl_coverage * 100), str(seeed_total_parts)))
    print([i['mpn'] + ' : ' + i['brand'] + ' : x' + str(i['qty'])
           for i in seeed_cpl_matches])
    print ('----------------------------------')

    print ("================================================================")
    print ("=================    SEEED OPL MATCHES    ======================")
    print ("================================================================")
    print ('ArmProMini: covered {:.2f} percent of total {} parts'.format(
           (arm_opl_coverage * 100), str(arm_total_parts)))
    print([i['mpn'] + ' : ' + i['brand'] + ' : x' + str(i['qty']) for i in arm_opl_matches
           if 'brand' and 'mpn' in i])
    print ('----------------------------------')
    print ('Arduino: covered {:.2f} percent of total {} parts'.format(
           (arduino_opl_coverage * 100), str(arduino_total_parts)))
    print([i['mpn'] + ' : ' + i['brand'] + ' : x' + str(i['qty']) for i in arduino_opl_matches
           if 'brand' and 'mpn' in i])
    print ('----------------------------------')
    print ('Octopart CPL: covered {:.2f} percent of total {} parts'.format(
           (octopart_opl_coverage * 100), str(octopart_total_parts)))
    print([i['mpn'] + ' : ' + i['brand'] + ' : x' + str(i['qty']) for i in octopart_opl_matches
           if 'brand' and 'mpn' in i])
    print ('----------------------------------')
