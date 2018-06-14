import get_api_key
import requests
import logging

log = logging.getLogger('officals_log')
log.setLevel(logging.DEBUG)
fh = logging.FileHandler('officals_list.txt', 'w')
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
fh.setLevel(logging.DEBUG)
log.addHandler(fh)
log.addHandler(ch)

# convert spaces into %20 for get request
def escape_spaces(string):
	return string.replace(' ', '%20')

# set up request
key = get_api_key.get_api_key('g_civic')
url = 'https://www.googleapis.com/civicinfo/v2/representatives?'
address = escape_spaces('4255 23rd Ave S, Fargo, ND 58104')
url = url + 'address=' + address + "&key=" + key
log.info('sending request')
log.debug('request: ' + url)

# get results and store them as officials and offices
result = requests.get(url).json()
log.debug('request result: ' + str(result))
officials = result['officials']
offices = result['offices']

log.debug('deleting results')
del result

log.info('Name | Position | Phone(s) | Email')
# cycle through officials and offices matching only state offices
for official, office in zip(officials, offices):
	if official['address'][0]['state'] == 'CA':
		log.info(official['name'] + ' : ' + office['name'])

# retrieve current elections based on address
url = 'https://www.googleapis.com/civicinfo/v2/voterinfo?address='
url = url + address + '&key=' + key
response = requests.get(url)
if response.status_code is 200:
	response = response.json()
	for k, v in response.items():
		log.info(k + " : " + str(v))
else:
	log.info('no current elections for ' + address)
