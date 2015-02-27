import cPickle as pickle


def scrub_bom(input_bom):
    """ clean dictionary from empty entries """
    clean_bom = []
    for part in input_bom:
        if part['mpn'] is not '':
            clean_bom.append(part)
    return clean_bom


def match_boms(bom_01, bom_02):
    """ find matches between two boms """
    matches = []
    coverage = 0.0
    for part_01 in bom_01:
        for part_02 in bom_02:
            if part_01['mpn'] == part_02['mpn']:
                matches.append(part_01)
    coverage = float(len(matches)) / len(bom_02)
    return matches, coverage


#  do the matching
if __name__ == '__main__':

    #  load all the boms from .json files
    with open('../../data/formatted_jsons/cpl_bom.json', 'rb') as cpl_file:
        cpl_bom = pickle.load(cpl_file)

    with open('../../data/formatted_jsons/arm_pro_mini_bom.json', 'rb') as arm_file:
        arm_bom = pickle.load(arm_file)

    with open('../../data/formatted_jsons/seeedOPL_bom.json', 'rb') as seeed_file:
        seeed_bom = pickle.load(seeed_file)

    with open('../../data/formatted_jsons/arduino_bom.json', 'rb') as arduino_file:
        arduino_bom = pickle.load(arduino_file)

    # Clean all the boms from empty entries
    cpl_bom = scrub_bom(cpl_bom)
    arm_bom = scrub_bom(arm_bom)
    seeed_bom = scrub_bom(seeed_bom)
    arduino_bom = scrub_bom(arduino_bom)

    # Match three boms against CPL
    arm_matches, arm_coverage = match_boms(cpl_bom, arm_bom)
    seeed_matches, seeed_coverage = match_boms(cpl_bom, seeed_bom)
    arduino_matches, arduino_coverage = match_boms(cpl_bom, arduino_bom)

    print 'Arm Pro Mini: covered %.2f percent of parts' % (arm_coverage * 100)
    print arm_matches
    print '----------------------------------'
    print 'Seeed Studio OPL: covered %.2f percent of parts' % (seeed_coverage * 100)
    print seeed_matches
    print '----------------------------------'
    print 'Arduino: covered %.2f percent of parts' % (arduino_coverage * 100)
    print arduino_matches
    print '----------------------------------'


