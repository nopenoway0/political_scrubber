# use an sio object to extract information
from url_creator import ScraperInfoObject
from bs4 import BeautifulSoup
import re
import requests

class Extractor:
	patterns = {"arg": r"(\s*)", "function": r"\s*("}
	def __init__(self):
		pass
	def extract_information(self, sio, soup):
		if sio is None or sio.steps is None:
			return soup
		for step in sio.steps:
			if step.find('{url}') is not -1:
				url = re.search(r'\{url\}(.*)', step).group(1)
				soup = BeautifulSoup(requests.get(url).text, 'html.parser')
			elif step.find('{iter}') is not -1:
				for x in range(0, len(soup)):
					pass
			elif step.find('{trim}') is not -1:
				pass
			elif step.find('(') is not -1:
				function, args = re.search(r'^\s*(\w+)\s*\((.*)\)', step).group(1), re.search(r'.*?\((.*)\)', step).group(1)
				soup = eval('soup.' + function + "(" + args + ")")
			elif step.find('[') is not -1:
				index = re.search(r'\[\'(.+)\'\]', step).group(1)
				soup = soup[index]
			else:
				soup = getattr(soup, step)
		if sio.scraper is not None:
			soup = self.extract_information(sio.scraper, soup)
		return soup
class ScrapedInfo:
	pass
