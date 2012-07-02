#!/usr/bin/env python

import magic
import re

def getExt(filename):
	m = magic.Magic()
	filetype = m.from_file(filename)

	extension=""

	# Executables
	if( re.match("PE32 executable for MS Windows", filetype)):
		extension=".exe"

	if( re.match("MS-DOS executable", filetype)):
		extension=".exe"

	if( re.match("PE for MS Windows", filetype)):
		extension=".exe"

	if( re.match("python script", filetype)):
		extension=".py"

	if( re.match("perl.*script", filetype)):
		extension=".pl"

	if( re.match("PHP script", filetype)):
		extension=".php"

	# MS Office Documents
	if( re.match("CDF.*Microsoft Word [0-9]", filetype)):
		extension=".doc"

	if( re.match("Microsoft Office Word", filetype)):
		extension="*.doc"

	if( re.match("CDF.*Microsoft Excel", filetype)):
		extension=".xls"

	# Images
	if( re.match("GIF image data", filetype)):
		extension=".gif"

	if( re.match("PC bitmap", filetype)):
		extension=".bmp"

	if( re.match("JPEG image data", filetype)):
		extension=".jpg"

	# Archives
	if( re.match("Zip archive data", filetype)):
		extension=".zip"

	if( re.match("7-zip archive data", filetype)):
		extension=".7z"

	if( re.match("RAR archive data", filetype)):
		extension=".rar"

	if( re.match("POSIX tar archive", filetype)):
		extension=".tar"

	# Unsorted
	if( re.match("Windows Registry text", filetype)):
		extension=".reg"

	if( re.match("Macromedia Flash data", filetype)):
		extension=".swf"

	if( re.match("PDF document", filetype)):
		extension=".pdf"

	if( re.match("HTML document", filetype)):
		extension=".html"

	if( re.match("BitTorrent file", filetype)):
		extension=".torrent"

	if( re.match("compiled Java class data", filetype)):
		extension=".class"

	return(extension)

