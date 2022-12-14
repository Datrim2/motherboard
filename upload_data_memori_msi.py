from sqlalchemy import create_engine
from pathlib import Path
import json
import requests

from models import Memory, MotherBoard
from sqlalchemy.orm import sessionmaker

jpath = Path('.') / 'panel.json'

with open(jpath, mode='r', encoding='utf-8') as src:
    data = json.load(src)

engine = create_engine('sqlite:///motherboard.sqlite3') 

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

result = session.query(MotherBoard).filter(MotherBoard.mb_id>188).all()#96,132
for element in result:
    response = requests.get(f'https://ru.msi.com/api/v1/product/support/panel?product={element.link}&type=mem&per_page=5000')
    data = response.json()
    for elem in data['result']['downloads']['type_title']:
        objects = []
        for el in data['result']['downloads'][elem]['list']:
            objects.append(Memory(type_memory=elem,
                                motherboard_id=element.mb_id,
                                vendor=el['Vendor'],
                                model=el['Model'],
                                ddr=el['DDR'],
                                spd=el['SPD Speed'],
                                support=el['Supported Speed'],
                                chipset=el['Chipset'],
                                voltage=el['Voltage'],
                                sided=el['Sided'],
                                size=el['Size'],
                                dimm=list(el.items())[len(el.items())-1][1]
                                ))
        session.bulk_save_objects(objects)
        session.commit()