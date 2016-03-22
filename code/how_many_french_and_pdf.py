import os

for directory, subdirs, files in os.walk('../data/echr-copy-1'):
	#print subdirs
	#print files
	if len(files)> 0:
		if 'html' not in '-'.join(files):
			print files, subdirs, directory
count =0

for directory, subdirs, files in os.walk('../data/echr-copy-1'):
	if len(directory.split('/')) == 4:
		if 'en' not in '-'.join([x for x in os.listdir(directory)]):
			print directory
			print os.listdir(directory)
			count +=1
print count