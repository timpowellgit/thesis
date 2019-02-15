
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

def pdfparser(data):

    fp = file(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()

    return data

# files = os.listdir('../data/guides/')
# for f in files:
# 	guide = '../data/guides/%s' %(f)
# 	text = pdfparser(guide)
# 	with open('../data/guides/%s.txt' %(f), 'w') as newfile:
# 		newfile.write(text)


guide = '../data/guides/righttoprop.pdf'
text = pdfparser(guide)
with open('../data/guides/righttoprop.pdf.txt', 'w') as newfile:
    newfile.write(text)