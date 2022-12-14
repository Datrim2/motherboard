from PDFParser import convert_pdf_to_txt
import math
from PIL import Image
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from classParser.classAgreggator_new import PDFPageDetailedAggregator
from io import BytesIO, StringIO

class PDFFileToDb():
    
    to_db = {}
    features = []
    timing = {}
    slv_spec = {'CL(IDD)':'cl','Row Cycle Time (tRCmin)':'tRCmin','Refresh to Active/Refresh Command Time (tRFCmin)':'tRFCmin',
    'Row Active Time (tRASmin)':'tRASmin','Maximum Operating Power':'MaxOper','UL Rating':'ul',
    'Operating Temperature':'otemperature','Storage Temperature':'stemperature'}
    slv_timing = {'Default (JEDEC):':'default','JEDEC:':'default','Default (Plug N Play):':'default','XMP Profile #1:':'xmp1',
                  'XMP Profile #2:':'xmp2','XMP Profile #3:':'xmp3','EXPO Profile #0:':'expo1','EXPO Profile #1:':'expo2',}
    
    def search(self,response,model):
        self.to_db = {}
        self.features = []
        self.timing = {}
        self.model=model
        self.img = None
        # self.data=next(convert_pdf_to_txt(response))
        # self.result=[ el for el in self.data.split("\n") if el]
        parser = PDFParser(BytesIO(response))
        doc = PDFDocument(parser)

        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageDetailedAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            # receive the LTPage object for this page
            device.get_result()
        self.result = device.rows
        self.img = device.img
        self.result[self.result.index('Refresh to Active/Refresh')]='Refresh to Active/Refresh Command Time (tRFCmin)'
        self.result.remove('Command Time (tRFCmin)')
        # self.search_memory()
        # self.search_specifications()
        # self.search_features()
        # self.search_desc()
        self.search_timing()
        
    def search_memory(self):
        if 'Memory Module Specifications' not in self.result and self.result[0]!=self.model:
            mem = [self.result.index(el) for el in self.result if 'Memory Module' in el][0]
            self.to_db["model"] = " ".join(self.result[mem+1:self.result.index('DESCRIPTION')])
            # del self.result[mem:self.result.index('DESCRIPTION')]
        elif self.result[0]==self.model:
            if self.result.index('SPECIFICATIONS') > 4:
                num = self.result.index('DESCRIPTION')
            else:
                num = self.result.index('SPECIFICATIONS')
            self.to_db["model"] = " ".join(self.result[0:num])
            # del self.result[0:self.result.index('DESCRIPTION')]
        else:
            self.to_db["model"] = " ".join(self.result[self.result.index('Memory Module Specifications')+1:self.result.index('SPECIFICATIONS')])
            # del self.result[self.result.index('Memory Module Specifications'):self.result.index('SPECIFICATIONS')]
    
    def search_specifications(self):
        for el in self.result[self.result.index('SPECIFICATIONS')+1:]:
            if 'FEATURES' in el:
                num = self.result.index(el)
                break
            if 'DESCRIPTION' in el:
                num = self.result.index(el)
                break
            if 'TIMING PARAMETERS' in el:
                num = self.result.index(el)
                break
            if 'kingston.com' in el:
                num = self.result.index(el)
                break
            if 'hyperxgaming.com' in el:
                num = self.result.index(el)
                break
        specifications = self.result[self.result.index('SPECIFICATIONS')+1:num]
        if '*Power will vary depending on the SDRAM used.' in specifications:
            self.to_db["dop"]='Power will vary depending on the SDRAM used'
            specifications.remove('*Power will vary depending on the SDRAM used.')
            # self.result.remove('*Power will vary depending on the SDRAM used.')
        # print(specifications)
        for el in range(round(len(specifications)/2)):
            self.to_db[self.slv_spec[specifications[el]]] = specifications[el+round(len(specifications)/2)]
        # del self.result[self.result.index('SPECIFICATIONS'):self.result.index('DESCRIPTION')]
    
    def search_features(self):
        for el in self.result[self.result.index('FEATURES')+1:]:
            if 'SPECIFICATIONS' in el:
                num = self.result.index(el)
                break
            if 'DESCRIPTION' in el:
                num = self.result.index(el)
                break
            if 'TIMING PARAMETERS' in el:
                num = self.result.index(el)
                break
            if 'kingston.com' in el:
                num = self.result.index(el)
                break
            if 'hyperxgaming.com' in el:
                num = self.result.index(el)
                break
        features = self.result[self.result.index('FEATURES')+1:num]
        for el in features: 
            if '•' in el:
                self.features.append(el.replace('•','').strip())
            else:
                self.features[len(self.features)-1]=self.features[len(self.features)-1]+' '+el.strip()
    
    def search_desc(self):
        for el in self.result[self.result.index('DESCRIPTION')+1:]:
            if 'SPECIFICATIONS' in el:
                num = self.result.index(el)
                break
            if 'FEATURES' in el:
                num = self.result.index(el)
                break
            if 'TIMING PARAMETERS' in el:
                num = self.result.index(el)
                break
            if 'kingston.com' in el:
                num = self.result.index(el)
                break
            if 'hyperxgaming.com' in el:
                num = self.result.index(el)
                break
        # for el in self.result:
        #     if 'TIMING PARAMETERS' in el:
        #         num = self.result.index(el)
        # if not num:
        #     for el in self.result:
        #         if 'kingston.com' in el:
        #             num = self.result.index(el)
        # if not num:
        #     raise Exception('Ошибка при поиске описания')
        self.to_db['desc']=' '.join(self.result[self.result.index('DESCRIPTION')+1:num])
    
    def search_timing(self):
        num = -1
        for el in self.result:
            if 'TIMING PARAMETERS' in el:
                num = self.result.index(el)
        if num != -1:
            for el in self.result[num+1:]:
                if 'SPECIFICATIONS' in el:
                    last_num = self.result.index(el)
                    break
                if 'FEATURES' in el:
                    last_num = self.result.index(el)
                    break
                if 'DESCRIPTION' in el:
                    last_num = self.result.index(el)
                    break
                if 'kingston.com' in el:
                    last_num = self.result.index(el)
                    break
                if 'hyperxgaming.com' in el:
                    last_num = self.result.index(el)
                    break
            # for el in self.result:
            #     if 'kingston.com' in el:
            #         last_num = self.result.index(el)
            # print(self.result)
            # print(num)
            # print(self.result[num+1].replace('• ',''))
            if self.result[num+1].replace('• ','').strip() in self.slv_timing:
                timing = self.result[num+1:last_num]
                self.timing = { self.slv_timing[timing[el].replace('• ','')]:timing[el+math.trunc(len(timing)/2)] for el in range(math.trunc(len(timing)/2))} 
                self.timing['dname'] = timing[0].replace('• ','')
            else:
                i = 1
                print(self.result[num+1:last_num])
                for el in self.result[num+1:last_num]:
                    if '•' in el and ('JEDEC' in el or 'Default' in el):
                        self.timing['default'] = el.split(': ')[1].replace('•','').strip()
                        self.timing['dname'] = el.split(': ')[0].replace('•','').strip()
                    elif '•' in el:
                        self.timing[f"xmp{i}"] = el.split(': ')[1].replace('•','').strip() if len(el.split(': ')) >1 else ''
                        i = i+1
                    else:
                        if i==1:
                            self.timing["default"] = self.timing["default"]+','+el
                        else:
                            self.timing[f"xmp{i-1}"] = self.timing[f"xmp{i-1}"]+','+el
            
            
                   
    # def search_timing(self):
    #     if 'FACTORY TIMING PARAMETERS' in self.result:
    #         factory = 1
    #     elif 'JEDEC/XMP TIMING PARAMETERS' in self.result:
    #         factory = 2
    #     else:
    #         factory = 0
        
    #     if factory:
    #         description = self.result[self.result.index('DESCRIPTION')+1:self.result.index('FACTORY TIMING PARAMETERS')]
    #     else:
    #         description = self.result[self.result.index('DESCRIPTION')+1:self.result.index('kingston.com')]
        
    #     self.to_db['desc'] = ''
    #     for el in description:
    #         if '•' in el:
    #             self.features.append(el.replace('•',''))
    #         elif 'FEATURES' not in el:
    #             self.to_db['desc'] = self.to_db['desc'] + el
        
    #     if factory:
    #         if factory == 1:    
    #             timing = self.result[self.result.index('FACTORY TIMING PARAMETERS')+1:self.result.index('kingston.com')]
    #         else:
    #             timing = self.result[self.result.index('JEDEC/XMP TIMING PARAMETERS')+1:self.result.index('kingston.com')]
    #         if len(timing) % 2 == 0:
    #             self.timing = { self.slv_timing[timing[el].replace('• ','')]:timing[el+math.trunc(len(timing)/2)] for el in range(math.trunc(len(timing)/2))} 
    #         else:
    #             num=1
    #             for el in timing:
    #                 if '(Plug N Play):  ' in el:
    #                     self.timing['default'] = el.split(':  ')[1]
    #                 elif 'Profile' not in el:
    #                     self.timing[f'xmp{num}'] = el
    #                     num = num + 1