import csv


def load_csv_fab(filepath):
    return_list = []
    discarded_list = []
    with open(filepath, 'rb') as csvfile:
        try:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            # print 'dialect detected for ' + filepath
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
        except:
            # print 'dialect NOT detected for ' + filepath
            csvfile.seek(0)
            reader = csv.reader(csvfile)

        for row in reader:
            if row[1] != '':
                return_list.append(row)
            else:
                discarded_list.append(row)

    return return_list, discarded_list


def load_csv_seed(filepath):
    return_list = []
    discarded_list = []
    with open(filepath, 'rb') as csvfile:

        csvfile.seek(0)
        reader = csv.reader(csvfile)

        for row in reader:
            return_list.append(row)

    return return_list, discarded_list


fab_list, fab_trash_list = load_csv_fab('fablab_electronics.csv')

seed_list, seed_trash_list = load_csv_seed('seedStudio_list.csv')

print seed_list

seed_parts = {
    'resistor': [],
    'capacitor': [],
    'switch': [],
    'sensor': [],
    'relay': [],
    'module': [],
    'microphone': [],
    'inductor': [],
    'ic': [],
    'fuse': [],
    'display': [],
    'diode': [],
    'connector': [],
    'buzzer': [],
    'battery': [],
    'antenna': [],
    'transistor': [],
    'crystal': [],
    }

for i in seed_list:
    if 'Resistor' in i[3]:
        seed_parts['resistor'].append(i)
    if 'Capacitor' in i[3]:
        seed_parts['capacitor'].append(i)
    if 'Switch' in i[3]:
        seed_parts['switch'].append(i)
    if 'Sensor' in i[3]:
        seed_parts['sensor'].append(i)
    if 'Relay' in i[3]:
        seed_parts['relay'].append(i)
    if 'Module' in i[3]:
        seed_parts['module'].append(i)
    if 'Microphone' in i[3]:
        seed_parts['microphone'].append(i)
    if 'Inductor' in i[3]:
        seed_parts['inductor'].append(i)
    if 'IC' in i[3]:
        seed_parts['ic'].append(i)
    if 'Fuse' in i[3]:
        seed_parts['fuse'].append(i)
    if 'Display' in i[3]:
        seed_parts['display'].append(i)
    if 'Diode' in i[3]:
        seed_parts['diode'].append(i)
    if 'Connector' in i[3]:
        seed_parts['connector'].append(i)
    if 'Buzzer' in i[3]:
        seed_parts['buzzer'].append(i)
    if 'Battery' in i[3]:
        seed_parts['battery'].append(i)
    if 'Antenna' in i[3]:
        seed_parts['antenna'].append(i)
    if 'Transistor' in i[3]:
        seed_parts['transistor'].append(i)
    if 'Crystal' in i[3]:
        seed_parts['crystal'].append(i)

res_values = [i[2].strip().split() for i in seed_parts['resistor']]


for i in res_values:
    if 'Array' in i[2] or 'ARRAY' in i[2]:
        print i


# print '=================================='
# print [i for i in seed_parts['capacitors']]
# print '=================================='
