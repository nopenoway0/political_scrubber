# warning Arizona is currently broken
# Stopped at colorado website
# TODO: create adaptable SIOs
class URLCreator:
	year = 2018
	state_mappings = {"california": "http://www.sos.ca.gov",
	 "alabama": "http://www.sos.alabama.gov/", 
	"alaska":"http://www.sos.alaska.gov/elections", "arizona": False,
	 "arkansas": "http://www.sos.arkansas.gov/elections", 
	"colorado": "http://www.sos.state.co.us/pubs/elections/main.html",
	}
	def create_election_url(self, state):
		return self.state_mappings[state] + '/elections'
	def create_homepage_url(self, state):
		return self.state_mappings[state]

	def create_sio(self, state, req_type = "election"):
		if state is 'california':
			if req_type is "election":
				return ScraperInfoObject(name = "Election Scrape", steps = ("h2", "parent", "td", "find_all('a')"))
			else:
				return ScraperInfoObject(name = "Candidate Scrape", steps = ("find(string=re.compile(r\'Certified\'))", 'parent', '[\'href\']'))
		elif state is 'alabama':
			if req_type is 'election':
				return ScraperInfoObject(name = 'Election Scrape', steps = None )
				#'{url}https://sos.alabama.gov/alabama-votes/voter/election-information/' + str(self.year),))# "find_all('h2')"))

class ScraperInfoObject:
	def __init__(self, steps = None, embed_scraper = None, name = "Scraper"):
		self.name = name
		self.steps =  steps
		self.scraper = embed_scraper
