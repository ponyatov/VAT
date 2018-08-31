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

# default target
print >>mk,'.PHONY: all\nall: $(CWD).mp4\n'

MP4=[]

clean=['files']

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

for i in sorted(F):
	if i+'.mp4' in F[i]:
		video = i+'.mp4'
		MP4 += [video]
	if i+'.png'	in F[i]:
		video = i+'.png.mp4'
		print >>mk,'%s: %s.png'%(video,i)
		MP4 += [video]
#		clean += [video]
	if i+'.en' in F[i] or i+'.ru' in F[i]:
		print >>mk,'%s.mix.mp4: %s %s.wav'%(i,video,i)
		if i+'.en' in F[i]:
			en = '%s.en.wav'%i
		else: en=''
		if i+'.ru' in F[i]:
			ru = '%s.ru.wav'%i
		else: ru=''
		print >>mk,'%s.wav: %s.mix'%(i,i)
#		clean += ['%s.mix'%i,
		clean += ['%s.wav'%i]
		print >>mk,'%s.mix: %s %s\n\t../mixfiles.py $@ $^'%(i,en,ru)
		if en:
			print >>mk,'%s.en.wav: %s.en'%(i,i)
#			clean += ['%s.en.wav'%i]
		if ru:
			print >>mk,'%s.ru.wav: %s.ru'%(i,i)
#			clean += ['%s.ru.wav'%i]
		MP4 = MP4[:-1] + [i+'.mix.mp4']

print >>mk,'''
FILE=180829_140652

go:
#	festival --tts $(FILE).en
	festival --tts --language russian $(FILE).ru 
'''

print >>mk, '''
$(CWD).mp4: %s
\t../mixfiles.py files $^
\tffmpeg -f concat -i files -c:v copy -an -y $@
#\tmplayer $@
'''% reduce(lambda a,b:a+' '+b,MP4)

#files = open('files','w')
#for i in MP4:
#	print >> files , "file '%s'" % i
#files.close()

print >> mk , '''

# ffmpeg options

VIDEO = -vcodec libx264 -preset veryslow -qp 0 -crf 0 -bf 2 -flags +cgop -pix_fmt yuv420p
AUDIO = -acodec mp3
#aac -strict 1 -ab 384k -ar 48000

# converting patterns

%.png.mp4: %.png
\tffmpeg -i $< -r .3 $(VIDEO) -y $@

%.en.wav: %.en
\ttext2wave -eval "(voice_kal_diphone)" $< -o $@

%.ru.wav: %.ru
\ttext2wave -eval "(voice_msu_ru_nsh_clunits)" $< -o $@

%.wav: %.mix
\tffmpeg -f concat -i $< $(AUDIO) -y $@

%.mix.mp4: %.png.mp4 %.wav
\tffmpeg -i $(word 1,$^) -i $(word 2,$^) -c:v copy -y $@

'''

print >>mk,'''.PHONY: clean
clean:
	rm -f $(CWD).mp4 *.png.mp4 *.en.wav *.ru.wav *.mix.mp4 *.mix \\
	%s
	ls -la --color
''' % reduce(lambda a,b:a+' '+b,clean)

mk.close()
os.system('make')

