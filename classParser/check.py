from pprint import pprint
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from classParser.classAgreggator_new import PDFPageDetailedAggregator
from io import BytesIO, StringIO
import requests

response = requests.get(f"https://www.kingston.com/datasheets/HX424C15FB4K4_64.pdf")
fp = BytesIO(response.content)
parser = PDFParser(fp)
doc = PDFDocument(parser)

rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageDetailedAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

for page in PDFPage.create_pages(doc):
    interpreter.process_page(page)
    # receive the LTPage object for this page
    device.get_result()

for el in range(len(device.img)):
    f = open(f"{el}.jpeg",'wb')
    f.write(device.img[el])
    f.close()

for el in device.rows:
    print(el)
print(len(device.rows))
print(device.img)
