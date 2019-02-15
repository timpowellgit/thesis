import nltk.data
import re
import os
from bs4 import BeautifulSoup

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

for directory, subs, files in os.walk('../../data/echr-copy-1'):
    for fname in files:
        if fname.endswith((".html", ".htm")) and 'jud_en' in directory:
            with open(os.path.join(directory, fname)) as fp:

                read = fp.read()
                cleaned =  BeautifulSoup(read)
                print fname
                p = cleaned.find_all('p')
                with open(os.path.join(directory, 'one_line_per_sentence'), 'a') as fp2:
                    for para in p:
                        parajoined = ' '.join([x.string if x.string else ' ' for x in para.find_all('span')]) 
                        print >> fp2,re.sub(r'\W',' ',parajoined) 
                # x = tokenizer.tokenize(data2.decode('utf8'))
                # newname = '%s_sentence_per_line.txt' %(file.split('.')[0])
                # with open(os.path.join(dir,newname), 'wb') as fp2:

                #     fp2.write('\n'.join(x).encode('utf8'))