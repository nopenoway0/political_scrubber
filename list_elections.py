import requests
import get_api_key
base_url = 'https://www.googleapis.com/civicinfo/v2/'
# use locations to find relevant and local elections
key = get_api_key.get_api_key('g_civic')

# get current election information in the form of JSON objects
url = base_url + 'elections?key=' + key

# get a list of current elections
result = requests.get(url)
print(result.text)
