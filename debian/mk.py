#!/usr/bin/env python

# Makefile generator for Smalltalk/VAT grabbing toolkit (Linux)
#
# https://github.com/ponyatov/VAT
# https://ponyatov.quora.com/Smalltalk-etudes-VAT-Video-Authoring-Toolkit
#

import os,sys,time,re

# get all files with YYMMDD_HHMMSS pattern
files = sorted(filter(lambda x:re.match(r'\d+_\d+\.',x),os.listdir('.')))
#print files

# group by timestamp pattern

F = {}
for i in files:
	ts = re.findall(r'\d+_\d+',i)[0]
	try: F[ts] += [i]
	except KeyError: F[ts] = [i]
print F

