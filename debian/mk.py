#!/usr/bin/env python

# Makefile generator for Smalltalk/VAT grabbing toolkit (Linux)
#
# https://github.com/ponyatov/VAT
# https://ponyatov.quora.com/Smalltalk-etudes-VAT-Video-Authoring-Toolkit
#

import os,sys,time,re

# current dir/project name
CWD = re.findall(r'/([a-zA-Z_0-9]+)$',os.getcwd())[0]

# target Makefile will be (re)created
mk = open('Makefile','w')

print >>mk,'CWD = $(notdir $(CURDIR))\n'

# ffmpeg options
print >>mk,'VIDEO = -vcodec libx264 -preset veryslow -qp 0 -crf 0 -bf 2 -flags +cgop -pix_fmt yuv420p\n'

# default target
print >>mk,'.PHONY: all\nall: $(CWD).mp4\n'

MP4=[]

# get all files with YYMMDD_HHMMSS pattern
files = sorted(filter(lambda x:re.match(r'\d+_\d+\.',x),os.listdir('.')))
#print files

# group by timestamp pattern

F = {}
for i in files:
	ts = re.findall(r'\d+_\d+',i)[0]
	try: F[ts] += [i]
	except KeyError: F[ts] = [i]

def dump():
	for i in F:
		print i
		for j in F[i]:
			print '\t',j

#dump()

for i in F:
	if i+'.png'	in F[i]:
		print >>mk,'\n%s.mp4: %s.png'%(i,i)
		print >>mk,'\tffmpeg -i $< -r .2 $(VIDEO) -y $@'
		MP4 += [i+'.mp4']
	if i+'.en' in F[i] or i+'.ru' in F[i]:
		print >>mk,'\n%s.mix.mp4: %s.mp4 %s.wav'%(i,i,i)
		print >>mk,'%s.wav: %s.en %s.ru'%(i,i,i)
		MP4 += [i+'.mix.mp4']

print >>mk,'''
FILE=180829_140652

go:
#	festival --tts $(FILE).en
	festival --tts --language russian $(FILE).ru 
'''

print >>mk, '$(CWD).mp4: files\nfiles: %s'% reduce(lambda a,b:a+' '+b,MP4)

files = open('files','w')
for i in MP4:
	print >> files , "file '%s'" % i
files.close()

