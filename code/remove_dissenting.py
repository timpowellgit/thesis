__author__ = 'timothypowell'


import re
import codecs
from preprocessing import *
import os

casepattern = re.compile('\([^\(^\)]*\d{5}\/\d\d[^|)]*\)')
count = 0
for directory, subs, files in os.walk('/Users/timothypowell/thesis/data/echr-copy-1'):
    for file in files:
        if 'fulltext' in file and 'jud_en' in directory:
            with codecs.open(os.path.join(directory, file), encoding = 'utf8') as f:
                cleaned = f.read()


                if 'DISSENTING' in cleaned :
                    cleaned = cleaned[:cleaned.index('DISSENTING')]
                # re sub fulltext with '' filename = file.split('.')[0]
                textfile = os.path.join(directory, '{}nodissenting_nocitations'.format(filename))
                myfile =  open(textfile, 'w+')
                myfile.write(cleaned.encode('utf8'))