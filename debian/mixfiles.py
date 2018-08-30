#!/usr/bin/env python
import os,sys,time,re

files = open(sys.argv[1],'w')
for i in sys.argv[2:]:
	print >>files, "file '%s'"% i

