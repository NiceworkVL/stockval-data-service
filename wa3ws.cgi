#!/usr/bin/python
#!/data/data/com.termux/files/usr/bin/python

import sys
#print sys.version

#print("Content-Type: text/plain\n")
print "Content-Type: text/plain\n" 

import cgi

form = cgi.FieldStorage()
symbol = form.getfirst('symbol')
if symbol is not None:
    sys.argv.append(symbol)
goodwill = form.getfirst('goodwill')
if goodwill is not None:
    sys.argv.append(goodwill)
valmode = form.getfirst('valmode')
if valmode is not None:
    sys.argv.append(valmode)

#sys.path.insert(0,'/data/data/com.termux/files/home/project/webapp3')
sys.path.insert(0,'/home/neotruss/public_html/wa3')
import p3ws
