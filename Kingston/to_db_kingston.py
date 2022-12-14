import requests

from sqlalchemy import create_engine
from models import Memory,Specifications,Features,Timing
from sqlalchemy.orm import sessionmaker
from classPDFParse import PDFFileToDb

engine = create_engine('sqlite:///motherboard.sqlite3') 

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

result = session.query(Memory.model).filter(Memory.vendor.like("Kingston"),Memory.specifications_id == None).distinct().all()
parse = PDFFileToDb()
for element in result:
    url_par=element[0].replace('/','_').replace('(Profile2)','').replace('-SP','').replace(' ','')
    print(element[0])
    response = requests.get(f"https://www.kingston.com/datasheets/{url_par}.pdf")
    print(response.ok)
    print(response.url)
    if response.ok:
        parse.search(response.content,element[0].replace('(Profile2)','').replace(' ',''))
        try:
            if parse.timing:
                t = Timing(**parse.timing)
                session.add(t)
            if len(parse.features)<8:
                for el in range(8-len(parse.features)+1):
                    parse.features.append('0')
            f = Features(**{f'f{el}':parse.features[el] for el in range(1,len(parse.features))})
            session.add(f)
            session.commit()
            if parse.timing:
                s = Specifications(features_id=f.id,timing_id=t.id,**parse.to_db)
            else:
                s = Specifications(features_id=f.id,**parse.to_db)
            session.add(s)
            session.commit()
            add_id_ram = session.query(Memory).filter(Memory.model.like(f"{element[0]}")).all()
            for el in add_id_ram:
                el.specifications_id = s.id
            session.commit() 
        except:
            session.rollback()
            raise

result = session.query(Specifications).filter(Specifications.model.like('%DESCRIPTION%')).all()
        
for elem in result:
    res = []
    for el in elem.model[0:elem.model.index(' DESCRIPTION')].replace('288 Pi','288-Pin').replace('DDR4 ','DDR4-').replace('288-Pinn','288-Pin').split():
        if el not in res:
            res.append(el)
    elem.name = ' '.join(res)

session.commit()