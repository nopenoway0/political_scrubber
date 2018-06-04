import requests
from bs4 import BeautifulSoup
import info_extracter
import url_creator
import re
from os import remove
import pdf_converter
# TODO: not writing GOVERNOR job in candidates1.pdf
# check for recent elections
# check candidates in recent elections
# gather information on current standing for the said candidate
# present it to user based on their location, they can also type in their zip code


jobs = {"STATE ASSEMBLY MEMBER": False, 
'STATE SENATOR DISTRICT' : False,  'GOVERNOR' : False, 'LIEUTENANT GOVERNOR' : False,
'SECRETARY OF STATE' : False, 'ATTORNEY GENERAL' : False, 'INSURANCE COMMISSIONER': False, 'SUPERINTENDENT OF PUBLIC': False,
'BOARD OF EQUALIZATION' : False, 'MEMBER DISTRICT ' : False, 'UNITED STATES SENATOR' : False, 'UNITED STATES REPRESENTATIVE' : False,
'U.S. R' : False, 
} # Need to provide working code for when malformed jobs appear as well as figuring out USAF M and S fixes



# get html page for state to extract information
cr = url_creator.URLCreator()
url = cr.create_election_url("california")
html = requests.get(url)
soup = BeautifulSoup(html.text, "html.parser")

# set up rules for extraction
ext = info_extracter.Extractor()
sio = cr.create_sio('california', req_type = 'election')
sio_candidate = cr.create_sio('california', req_type = 'candidate')

# extract links for page using designated sio object and html from homepage
results, links = ext.extract_information(sio, soup), []
#print (results)

# TEST _-------------------------
'''
with open('contents.txt', 'r') as file:
	results = file.read()
	soup = BeautifulSoup(results, 'html.parser')
	results = ext.extract_information(sio, soup)
	for heading in results.find_all('h3'):
		# check for links for elections
		print(heading.next_element.next_element.next_element)
'''
#print(results.next_sibling)

# END TEST ----------------------

for result in results:
	links.append(cr.create_homepage_url('california') + result['href'])

# parse through to get the candidate links for each election using dedicates sio candidate object
candidate_links = []
for link in links:
	print ("link: " + link)
	html = requests.get(link)
	soup = BeautifulSoup(html.text, "html.parser")
	candidate_links.append(ext.extract_information(sio_candidate, soup))
del links, html, soup, results, sio, sio_candidate, ext

# get pdf or html from each candidate link
counter, filenames = 1, []
for link in candidate_links:
	print ('downloading candidate information from: ',  link)
	contents = requests.get(link)
	with open('candidate' + str(counter) + '.pdf', 'wb') as file:
		file.write(contents.content)
	filenames.append('candidate' + str(counter) + '.pdf')
	counter += 1
with open('candidates.txt', 'w') as f:
# get names from file
	for name in filenames:
		print ('converting ', name, ' to text')
		text = pdf_converter.convert_pdf_to_txt(name)
		print('\textracting candidates')
		candidates = re.findall(r'\n*([A-Z\.][A-Z\.\"]+[ ]+[ \.\"]*[A-Z\"\-\(\)\']+[ \.]*[A-Z\"\-]*)+[\n\*]*?', text)
		print('\textracting election name')
		election = re.search(r'[\f]+(.*?)[\r\n]+', text).group(1)
		# write name and election to file
		f.write('-' * 10 + election + '-' * 10 + '\n')
		for candidate in candidates:
			if jobs.get(candidate, True):
				f.write(candidate + '\n')
			else:
				f.write(' ' * 10 + candidate + ' ' * 10 + '\n')

# cleanup
for name in filenames:
	print('deleting ', name)
	remove(name)
