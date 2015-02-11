import cPickle as pickle

data = {}

data['abc'] = '123'
data['def'] = '456'
data['jhi'] = '789'


with open ('json_dict_01.json', 'wb') as fp:
	pickle.dump(data, fp)


print data['abc']
print data['def']
print data['jhi']

with open ('json_dict_01.json', 'rb') as fp:
	data_02 = pickle.load(fp)

print data_02['abc']
print data_02['def']
print data_02['jhi']