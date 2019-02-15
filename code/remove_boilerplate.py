#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'timothypowell'


import re
import codecs
from preprocessing import *
import os
count =0
for directory, subs, files in os.walk('../data/echr-copy-1'):
    for file in files:
        if file.endswith('noboiler') and 'jud_en' in directory:
            with codecs.open(os.path.join(directory, file), encoding = 'utf8') as f:
                cleaned = f.read()
                
                
                if 'PROCEDURE' in cleaned: 
                    cleaned = cleaned[cleaned.index('PROCEDURE'):]
                elif 'P RO CEDURE' in cleaned:
                    cleaned = cleaned[cleaned.index('P RO CEDURE'):]
                elif 'PROCeDURE' in cleaned:
                    cleaned = cleaned[cleaned.index('PROCeDURE'):]
                else:
                    if 'THE FACTS' in cleaned:
                        cleaned = cleaned[:cleaned.index('THE FACTS')]
                    else:
                        cleaned = cleaned[:700]
                        
                found = re.findall(r'[A-Z]{3,}',cleaned)
                #print [f for f in found]
                if 'FOR THESE REAS' in cleaned:
                    cleaned = cleaned[:cleaned.index('FOR THESE REAS')]

                if 'UNANIMOUSLY' in cleaned:
                    cleaned = cleaned[:cleaned.index('UNANIMOUSLY')]
                if 'Default interest' in cleaned:
                    cleaned = cleaned[:cleaned.index('Default interest')]

                filename = file.split('.')[0]
                textfile = os.path.join(directory, '{}noboiler'.format(filename))
                myfile =  open(textfile, 'w+')
                myfile.write(cleaned.encode('utf8'))
                print '***'
                print '***'
                print '***'
                print '***'
                    #cleaned = cleaned[:cleaned.index('APPLICATION OF ARTICLE 41')]

                # re sub fulltext with '' filename = file.split('.')[0]
                # textfile = os.path.join(directory, '{}nodissenting_nocitations'.format(filename))
                # myfile =  open(textfile, 'w+')
                # myfile.write(cleaned.encode('utf8'))