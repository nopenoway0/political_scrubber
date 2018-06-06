#!/usr/bin/python
# process candidate information

import re

def contains(string, substring):
	return True if string.find(substring) is not -1 else False


def process_candidate_info(filepath = 'candidates.txt'):
	data = None
	with open(filepath, 'r') as file:
		data = file.read()
	elections = {}
	election_name = None
	cur_position =	'GOVERNOR'
	# for test purposes prematurely insert GOVERNOR
	elections['GOVERNOR'] = []
	for line in data.split('\n'):
		if contains(line, '---'):
			election_name = line 	# election
		elif contains(line, '\t'): 	# position
			print('found position')
			elections[line] = []
			cur_position = line
		else:				# candidate
			elections[cur_position].append(line)
	print (' ' * 5, 'ELECTION DATA', ' ' * 5)
	for position, candidates in elections.items():
		print(' ' * 10, '\'', position.strip(), '\'', ' ' * 10)
		for candidate in candidates:
			print (candidate.strip())

process_candidate_info()
