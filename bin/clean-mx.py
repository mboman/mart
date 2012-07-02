#!/usr/bin/env python

from elementtree.ElementTree import ElementTree
from urllib import urlopen

import urllib
import os
import errno
import shutil
import re
import time
import calendar
import base64
import hashlib
import subprocess
from glob import glob
import pprint

MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24

delay = int(30 * MINUTE)
basePath = "/MART/"
malwarePath = basePath + "samples/"

def main():
	pp = pprint.PrettyPrinter(indent=4)

	try:
		lastMod = int(os.path.getmtime(basePath + "xmlviruses.xml"))
	except:
		lastMod = 0

	curTime = int(calendar.timegm(time.gmtime()))

	#print("Last modified: " + str(lastMod))
	#print("Current time:  " + str(curTime))
	#print("Age:           " + str(int((curTime - lastMod)/60)) + " minutes")

	if (lastMod + delay) < curTime:
		age = int((curTime - lastMod))

		age_d = age / DAY
		age   = age - (age_d * DAY)

		age_h = age / HOUR
		age   = age - (age_h * HOUR)

		age_m = age / MINUTE
		age   = age - (age_m * MINUTE)

		print("It has been " + str(age_d) + " days, " + str(age_h) + " hours, " + str(age_m) + " minutes and " + str(age) + " seconds since last update")

		#print("Been at least 30 minutes since last checked")
	
		urllib.urlretrieve("http://support.clean-mx.de/clean-mx/xmlviruses.php?response=alive", basePath + "xmlviruses.xml")


		#with open(basePath + "xmlviruses.xml", "r+") as f:
		#	newF = []
		#	for line in f.readline():
		#		line = re.sub('\]\]\>\<\/url\>\]\]\>\<\/url\>', '\]\]\>\<\/url\>', line)
		#		line = re.sub('\<\/url\>\/\]\]\>\<\/url\>', '\<\/url\>', line)
		#		newF.append(line)
		#	newLines = ''.join(newF)
		#	f.seek(0)
		#	f.write(newLines)	
		
	else:
		print("Not updating virus list as it is less then 30 minutes old")

	# sed -e s:']]></url>]]></url>':']]></url>': -e s:'</url>/]]></url>':'</url>': -i xmlviruses.xml 
	# s:'</url>]].*':'</url>':
	cmd = [ 'sed', '-i', 
		'-e', 's:\'</url>.*\':\'</url>\':g',
		basePath + "xmlviruses.xml" ]
	pp.pprint(cmd)
	print("Running command: " + ' '.join(cmd))
	subprocess.check_call(cmd)

	cmd = [ 'xmllint', '-noout', basePath + "xmlviruses.xml" ]
	pp.pprint(cmd)
	print("Running command: " + ' '.join(cmd))
	subprocess.check_call(cmd)

	tree = ElementTree(file=basePath + "xmlviruses.xml")
	entryList = tree.findall("entries/entry")

	for entry in entryList:
		#print url.text
		urlString = entry[9].text
		md5String = entry[4].text

		#print "urlString: " + urlString
		#print "md5String: " + md5String

		re.IGNORECASE
		#result = re.match("^.*\.[Ee][Xx][Ee]$", urlString)
		result = re.match(".*", urlString)

		if result:
			try:
				filename = malwarePath + md5String
				generated_filename = False
			except:
				print("Filename generation error")
				filename = malwarePath + base64.urlsafe_b64encode(os.urandom(30))
				generated_filename = True

			files = glob(filename + "*")
			#if len(files) == 0 and os.path.isfile(filename) == False:
			if len(files) == 0:
				print("Downloading " + urlString + " as " + filename)
				try:
					urllib.urlretrieve(urlString, filename)
					if generated_filename == True:
						md5String = hashlib.md5(open(filename, 'rb').read()).hexdigest()
						newFilename = malwarePath + md5String
						print("Renaming " + filename + " to " + newFilename)
						os.rename(filename, newFilename)
						filename = newFilename
				except Exception as e:
					print("Error while downloading " + urlString + " %s" % e)
			#else:
				#print ("Not downloading " + urlString + " - already exists")
		else:
			print ("Not downloading " + urlString + " - not a exe file")

	print ("Finished downloading all available samples")

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

if __name__ == "__main__":
    main()

