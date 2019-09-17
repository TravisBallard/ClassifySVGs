import os, fnmatch, re
from os import path, fdopen, remove
from tempfile import mkstemp
from shutil import move

rootDir = './svgs'

# elements to classify
elements = ['g', 'path', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon']

# add element classes to a single line svg. for example a <circle /> element would output <circle class="circle0" />
def classifySingleLineSVG(elementName, line):
	parts = line.split('<' + elementName)
	for index, part in enumerate(parts, start=0):
		if index == 0 :
			output = parts[index]
		else :
			output += '<' + elementName + ' class="'+elementName+str(index-1)+'"' + parts[index]
	return output

# get the number of lines in a file
def numLinesInFile(file):
	with open(file) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

# main
for dirName, subDirList, fileList in os.walk(rootDir, topdown=False):
	if len(fileList) > 0:
		print('Processing: %s' % dirName)
		for fileName in fileList:
			if (fnmatch.fnmatch(fileName, '*.svg')):

				filePath = path.join(dirName, fileName)
				lines = []
				numLines = numLinesInFile(filePath)
				fh, tmpfile = mkstemp()

				with fdopen(fh,'w') as outFile:

					# multiline svg files
					# this only works if elements are not defined on the same line because it only increments by 1 if it finds something and not the number of found items. 
					# would need to iterate instances of found items with splitting similar to classifySingleLineSVG
					if (numLines > 1):
						for element in elements:
							count = 0
							with open(filePath) as inFile:
								for index, line in enumerate(inFile, start=0):
									if (len(lines) < numLines):
										lines.append(line)
									
									newline = lines[index]
									if (newline.find('<' + element) != -1):
										lines[index] = newline.replace('<' + element, '<' + element + ' class="'+ element + str(count) + '"')
										count += 1

					# single line svg files
					elif (numLines == 1):
						with open(filePath) as inFile:
							for line in inFile:
								newline = line
								for element in elements:
									newline = classifySingleLineSVG(element, newline)
								lines.append(newline)

					outFile.write(''.join(lines))
				remove(filePath)
				move(tmpfile, filePath)
				print('Added classes to %s' % os.path.basename(filePath))
