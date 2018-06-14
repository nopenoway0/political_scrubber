# use to retreive the API key
# keys.json file follows:
# 'keyname':
# {
#	"description": "description field",
#	"location" : "path"
# }

import json
# default keys location
KEYDB_LOCATION = '../keys.json'

class key_object:
	def __init__(self, description = 'none', key = None):
		self.description = description
		self.key = key
	def __str__(self):
		return 'description: ' + self.description
keys = {}
# import keys from json
with open(KEYDB_LOCATION, 'r') as db:
	contents  = db.read()
	contents = json.loads(contents)
	for k, v in contents.items():
		keys[k] = key_object(key = v['key'].strip(), description = v['description'].strip())

def get_api_key(api_name):
	if keys.get(api_name, False):
		return keys.get(api_name).key
	else:
		return None

def get_api_list():
	list = [];
	for val, obj in keys.items():
		list.append(val + ': ' + str(obj))
	return list
