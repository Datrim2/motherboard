import requests
from bs4 import BeautifulSoup

from sqlalchemy import create_engine
from models import Memory,Specifications,Features,Timing
from sqlalchemy.orm import sessionmaker
from classPDFParse import PDFFileToDb

engine = create_engine('sqlite:///motherboard.sqlite3') 

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

result = session.query(Memory.model,Memory.specifications_id).join(Specifications).filter(Memory.vendor.like("Kingston"),Memory.specifications_id != None,Specifications.picture == None).distinct().all()
parse = PDFFileToDb()
for element in result:
    url_par=element[0].replace('/','_').replace('(Profile2)','').replace('-SP','').replace(' ','')
    print(element[0])
    response = requests.get(f"https://www.kingston.com/datasheets/{url_par}.pdf")
    print(response.ok)
    print(response.url)
    # response_img = requests.get(f"https://www.kingston.com/ru/memory/search?partid={element[0].replace('-SP','').replace('(Profile2)','').replace(' ','')}")
    # soup = BeautifulSoup(response_img.text, 'html.parser')
    if response.ok:
        parse.search(response.content,element[0].replace('(Profile2)','').replace('-SP','').replace(' ',''))
        # try:
        # img = soup.find('a',attrs={"class":"c-productCard4__image"}).find("img").get("src")
        if not parse.img:
            raise Exception("no image")
        add_picture = session.query(Specifications).filter(Specifications.id == element[1]).first()
        add_picture.picture = parse.img
        img = ''
        add_dname = session.query(Timing).filter(Timing.id == add_picture.timing_id).first()
        if add_dname:
            if not add_dname.dname:
                if parse.timing['dname']:
                    add_dname.dname = parse.timing['dname']

        session.commit()
        # except:
        #     session.rollback()
        #     raise