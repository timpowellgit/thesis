__author__ = 'timothypowell'

import re
import codecs
from preprocessing import *
import os

pattern = re.compile('(\([^\(^\)]*(v\.|see).+?\))')
casepattern = re.compile('\([^\(^\)]*\d{5}\/\d\d[^|)]*\)')
count = 0
for directory, subs, files in os.walk('/Users/timothypowell/thesis/data/echr-copy-1'):
    for file in files:
        if file.endswith((".html", ".htm")) and 'jud_en' in directory:
            with codecs.open(os.path.join(directory, file), encoding = 'utf8') as f:
                read = f.read()
                cleaned =  html2text(read)
                if 'DISSENTING' in cleaned :
                    cleaned = cleaned[:cleaned.index('DISSENTING')]
                #print directory, file

                #print cleaned.encode('utf8')
                cleaned1 = re.sub(pattern, ' ', cleaned)
                cleaned2 = re.sub(casepattern, ' ', cleaned1)
                cleaned3 = re.sub('_', ' ', cleaned2)
                cleaned4 = re.sub('&#xa0', ' ', cleaned3)
                #print cleaned1.encode('utf8')
                #print cleaned2.encode('utf8')
                #print '************'
                filename = file.split('.')[0]
                textfile = os.path.join(directory, '{}nodissenting_nocitations'.format(filename))
                print textfile
                #print os.path.abspath(os.curdir)
                myfile =  open(textfile, 'w+')
                myfile.write(cleaned4.encode('utf8'))