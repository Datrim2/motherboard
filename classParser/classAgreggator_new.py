from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTPage, LTChar, LTAnno, LAParams, LTTextBox, LTTextLine, LTImage, LTFigure
# from PIL import Image
from io import BytesIO

class PDFPageDetailedAggregator(PDFPageAggregator):
    def __init__(self, rsrcmgr, pageno=1, laparams=None):
        PDFPageAggregator.__init__(self, rsrcmgr, pageno=pageno, laparams=laparams)
        self.rows = []
        self.img = []
        self.page_number = 0
    def receive_layout(self, ltpage):   
        if self.page_number == 0:     
            def render(item, page_number):
                if isinstance(item, LTPage) or isinstance(item, LTTextBox):
                    for child in item:
                        render(child, page_number)
                elif isinstance(item, LTTextLine):
                    child_str = ''
                    for child in item:
                        if isinstance(child, (LTChar, LTAnno)):
                            child_str += child.get_text()
                    child_str = ' '.join(child_str.split()).strip()
                    if child_str:
                        if item.bbox[1]>82:
                            row = (page_number, item.bbox[0], item.bbox[1], child_str) #  item.bbox[2], item.bbox[3],bbox == (x1, y1, x2, y2)
                            self.rows.append(row)
                    for child in item:
                        render(child, page_number)
                elif isinstance(item, LTFigure):
                    for el in item:
                        if isinstance(el, LTImage):
                            try:
                                # if el.bbox[1]>300 and el.bbox[1]<500:
                                self.img.append(el.stream.get_data())
                #                 self.it = item
                            except:
                                continue
                #             # self.img.append([el.bbox[0],el.bbox[1],el.stream.get_data()])
                #             # if el.bbox[1]>300 and el.bbox[1]<500:
                #             #     self.img=el.stream.get_data()
                return
            render(ltpage, self.page_number)
            self.page_number += 1
            rows_left = [ el[3] for el in self.rows if el[1]<300]#sorted(self.rows, key = lambda x: (-x[2], x[1]))
            rows_right = [ el[3] for el in self.rows if el[1]>300]
            self.rows = rows_left+rows_right+['hyperxgaming.com']
            # self.rows_right = sorted(self.rows_right, key = lambda x: (-x[2], x[1]))
            self.result = ltpage