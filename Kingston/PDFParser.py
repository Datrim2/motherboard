from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO, StringIO
#Pillow, pdfplumber, Wand
def convert_pdf_to_txt(response):
    fh = BytesIO(response)
    for page in PDFPage.get_pages(fh, 
                                    caching=True,
                                    check_extractable=True):
        resource_manager = PDFResourceManager()
        fake_file_handle = StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, codec='utf-8', laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()
        yield text

        # close open handles
        converter.close()
        fake_file_handle.close()
    # rsrcmgr = PDFResourceManager()
    # retstr = StringIO()
    # laparams = LAParams()
    # device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=laparams)
    # fp = open(path, 'rb')
    # interpreter = PDFPageInterpreter(rsrcmgr, device)
    # password = ""
    # maxpages = 0
    # caching = True
    # pagenos=set()

    # for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
    #     interpreter.process_page(page)

    # text = retstr.getvalue()

    # fp.close()
    # device.close()
    # retstr.close()
    # return text