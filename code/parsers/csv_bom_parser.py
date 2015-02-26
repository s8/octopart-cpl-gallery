import io
import json
import csv


def save_json(filename, data):
    """ serialize dictionary into json and save it to disk """
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))


def load_json(filename):
    """ read json file from disk into a dictionary """
    with io.open(filename, encoding='utf-8') as f:
        return json.loads(f.read())


def csv2dict(input_csv_file):
    """ read csv file from disk and parse it into a dictionary"""

    with io.open(input_csv_file, 'r', encoding='utf-8') as f:
        dict_from_csv = []
        csv_reader = csv.DictReader(f)
        for line_item in csv_reader:
            entry = {}
            for item in line_item:
                key = str(item).strip()
                value = str(line_item[item]).strip()
                if len(value) > 0 and len(key) > 0:
                    if key == 'MPN' or key == 'Manufactuer Part number' or key == 'Part Number':
                        entry['mpn'] = value
                    if key == 'Manufacturer' or key == 'Manufactuer Name':
                        entry['brand'] = value
            if len(entry) > 0:
                dict_from_csv.append(entry)
        return dict_from_csv


if __name__ == ('__main__'):
    """ open csv file, parse it into a dict and save as a json """

    seeedOPL_CSV_file = '../../data/parts_lists/OPL list20141222.csv'
    seeedOPL_JSON_file = '../../data/formatted_jsons/seeedOPL.json'
    save_json(seeedOPL_JSON_file, csv2dict(seeedOPL_CSV_file))
    seeed_opl = load_json(seeedOPL_JSON_file)

    octopartCPL_CSV_file = '../../data/parts_lists/Common Parts Library BOM.csv'
    octopartCPL_JSON_file = '../../data/formatted_jsons/octopartCPL.json'
    save_json(octopartCPL_JSON_file, csv2dict(octopartCPL_CSV_file))
    octopart_cpl = load_json(octopartCPL_JSON_file)

    arm_pm_BOM_CSV_file = '../../data/boms/arm-pro-mini-bom.csv'
    arm_pm_BOM_JSON_file = '../../data/boms/arm-pro-mini-bom.json'
    save_json(arm_pm_BOM_JSON_file, csv2dict(arm_pm_BOM_CSV_file))
    arm_pm_BOM = load_json(arm_pm_BOM_JSON_file)

    arduino_BOM_CSV_file = '../../data/boms/arduino_bom.csv'
    arduino_BOM_JSON_file = '../../data/boms/arm-pro-mini-bom.json'
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
    print ('arm: ' + str(len(arm_pm_BOM)) + ' elements')
    print ("----------------------------------------------------------------")
    print (arm_pm_BOM)

    print ("================================================================")
    print ('arduino: ' + str(len(arduino_BOM)) + ' elements')
    print ("----------------------------------------------------------------")
    print (arduino_BOM)
