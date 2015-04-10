# TODO
# * make components comparison case-insensitive: NRF51822 == nRF51822
# * make use of os.join operations
# * get rid of jsons - deal directly with csv's
# * strip out special characthers like hyphens
# * make partially-matching components match: NRF51822-QFAA-T == nRF51822
# * get rid of try-excepts
# * add quantity field so that if there's 10x the same part - it should have higher coverage rating
# * make two lists - parts that match and parts that don't
# * refactor (if len(value) > 0 and len(key) > 0:) line
# * refactor (if ('mpn' in entry.keys()):) line

# parse 10 more boms
# comment the code better
# make a googledoc with the results

import os
import io
import pprint
import re
import json
import csv

DATA_FOLDER = '../data/boms/'

# CSV file paths
SEEED_FILE = os.path.join(DATA_FOLDER, 'csv/OPL list20141222.csv')
OCTOPART_FILE = os.path.join(DATA_FOLDER, 'csv/Common Parts Library BOM.csv')
ARDUINO_FILE = os.path.join(DATA_FOLDER, 'csv/arduino_bom.csv')
ARM_FILE = os.path.join(DATA_FOLDER, 'csv/arm-pro-mini-bom.csv')


def clean_mpn(mpn):
    ''' remove non-alphanumeric characters from MPN field '''
    garbage_chars = '~!@#$%^&*()_+-={}[]|:;"<>,./?\\\' '

    for i in garbage_chars:
        if i in mpn:
            mpn = mpn.replace(i, '')
    return mpn


def csv2dict(input_csv_file):
    ''' read csv file from disk and parse it into an array of dictionaries
        [{'mpn':'...', 'brand':'...', 'qty':'...'},{...},...,{...}]
    '''
    print ('parsing {}'.format(input_csv_file))
    # different strings for the same field in different csv boms
    MPN_FIELDS = ['mpn', 'manufactuer part number', 
        'manufacturer part number', 'part number', 'part#', 'part #']
    BRAND_FIELDS = ['manufacturer', 'manufactuer name', 'manu', 'man']
    QTY_FIELDS = ['qty', 'quantity']

    with io.open(input_csv_file, 'r', encoding='utf-8') as f:
        dict_from_csv = []
        csv_reader = csv.DictReader(f)
        for line_item in csv_reader:
            entry = {}
            for item in line_item:
                key = item.strip().lower()
                value = line_item[item].strip()
                # sort the randomly-named csv entries into a neat dictionary
                if value:
                    if key in MPN_FIELDS: entry['mpn'] = clean_mpn(value)
                    elif key in BRAND_FIELDS: entry['brand'] = value
                    elif key in QTY_FIELDS: entry['qty'] = value

            # if part was mentioned in the list, but no quantity specified
            # we assume it is used once
            if 'qty' not in entry.keys(): entry['qty'] = 1

            # we only need parts with MPN explicitly stated
            if 'mpn' in entry.keys(): dict_from_csv.append(entry)
                
    return dict_from_csv


def match_boms(reference_bom, target_bom):
    '''
    part coverage is calculated as:
    total count of all matched parts / total count of parts in BOM

    over- and under-specified MPN's are matched
    match examples:
        c: 1n4148  r: 1n4148ws7f
        c: ft232rl  r: ft232rlreel
        c: mmbt3904  r: mmbt3904lt1g
        c: nrf51822  r: nrf51822qfaat
    '''

    # matching results data structure
    results = {
        'matches':[],
        'matches_count':0,
        'non-matches':[],
        'coverage':0,
        'total_parts':0
    }

    # iterate over the parts in the target BOM
    for target_part in target_bom:
        # make a total part count for the BOM
        results['total_parts'] += int(target_part['qty'])

        for reference_part in reference_bom:

            # store mpns in separate variables for concise comparison
            t = target_part['mpn'].upper()
            r = reference_part['mpn'].upper()

            # check for over- and under-specified MPN's in both lists
            if (t in r or r in t):
                # if match found - put it to the matched list 
                results['matches'].append(target_part)
            else:
                # if no match found - put it to the non-match list
                if target_part not in results['non-matches']:
                    results['non-matches'].append(target_part)

    # calculate coverage from total part count in the BOM

    parts_covered = sum([int(i['qty']) for i in results['matches']])
    results['coverage'] =  parts_covered / results['total_parts']

    return results

def print_results(name, matches):
    ''' print detailed results of matching procedure '''

    pp = pprint.PrettyPrinter(indent=4)

    print ('{}: covered {:.2f} percent from the total of {} parts'
        .format(
            name,
            matches['coverage'] * 100, 
            str(matches['total_parts'])
           )
        )
    print ('>>>> matched parts >>>>')
    pp.pprint(matches['matches'])
    print ('>>>> not matched parts >>>>')
    pp.pprint(matches['non-matches'])
    print ('----------------------------------')


if __name__ == ('__main__'):

    # read files into dictionaries
    seeed_opl = csv2dict(SEEED_FILE)
    octopart_cpl = csv2dict(OCTOPART_FILE)

    arm_BOM = csv2dict(ARM_FILE)
    arduino_BOM = csv2dict(ARDUINO_FILE)

    arm_IN_cpl = match_boms(octopart_cpl, arm_BOM)
    seeed_IN_cpl = match_boms(octopart_cpl, seeed_opl)
    arduino_IN_cpl = match_boms(octopart_cpl, arduino_BOM)

    arm_IN_opl = match_boms(seeed_opl, arm_BOM)
    cpl_IN_opl = match_boms(seeed_opl, octopart_cpl)
    arduino_IN_opl = match_boms(seeed_opl, arduino_BOM)

    print ("================================================================")
    print ("================  OCTOPART CPL MATCHES  ========================")
    print ("================================================================")
    print ()

    print_results('ArmProMini in CPL', arm_IN_cpl)
    print_results('Arduino in CPL', arduino_IN_cpl)
    print_results('Seeed OPL in CPL', seeed_IN_cpl)

    print ("================================================================")
    print ("=================    SEEED OPL MATCHES    ======================")
    print ("================================================================")
    print ()

    print_results('ArmProMini in OPL', arm_IN_opl)
    print_results('Arduino in OPL', arduino_IN_opl)
    print_results('Octopart CPL in OPL', cpl_IN_opl)
 
