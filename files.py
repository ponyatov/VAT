#!/usr/bin/env python

import os,sys,re

CWD = re.findall(r'/([a-zA-Z_0-9]+)$',os.getcwd())[0]

# lossless
VIDEO = '-vcodec libx264 -preset veryslow -qp 0 -crf 0 -bf 2 -flags +cgop -pix_fmt yuv420p '
#AUDIO = '-c:a aac -strict -2 -b:a 384 -r:a 48000 '

for i in sorted(filter(lambda x:re.match(r'\d+_\d+\.png',x),os.listdir('.'))):
	dd = re.findall(r'\d+_\d+',i)[0]
	print 'ffmpeg -i %s.png -r .2 %s -y %s.mp4'%(dd,VIDEO,dd)

files = open('files','w')
for i in sorted(filter(lambda x:re.match(r'\d+_\d+\.mp4',x),os.listdir('.'))):
	dd = re.findall(r'\d+_\d+',i)[0]
	if dd+'.en.wav' in os.listdir('.'):
		mix = open('%s.mix'%dd,'w')
		print >>mix,"file '%s.en.wav'"%dd
		print >>mix,"file '%s.ru.wav'"%dd
		mix.close()
		print 'ffmpeg -f concat -i %s.mix -c copy -y %s.wav'%(dd,dd)
		print 'ffmpeg -i %s.mp4 -i %s.wav -c:v copy -y %s.mix.mp4'%(dd,dd,dd)
		print >>files,"file '%s.mix.mp4'"%dd
	else:
		print >>files,"file '%s.mp4'"%dd
files.close()
print 'ffmpeg -f concat -i files -codec copy -y %s.mp4 ' % CWD
