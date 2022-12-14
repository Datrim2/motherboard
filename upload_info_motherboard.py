import requests
from pathlib import Path
import json
from datetime import datetime
from models import MotherBoard
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

jpath = Path('.') / 'motherboard.json'

with open(jpath, mode='r', encoding='utf-8') as src:
    data = json.load(src)

engine = create_engine('sqlite:///motherboard.sqlite3') 
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

for el in data['result']['getProductList']:
    response_picture = requests.get(el["picture"])
    session.add(MotherBoard(id_web=el['id'],
                            title=el['title'],
                            subname=el['subname'],
                            link=el['link'],
                            description=el['desc'],
                            ean=el['ean'],
                            release=datetime.strptime(el['release'], "%Y-%m-%d %H:%M:%S"),
                            product=el['product_line'],
                            picture=response_picture.content,
                            color=','.join(el['color']),
                            label=el['label']))
    session.commit()
    
# out = open("img.jpg", "wb")
# out.write(p.content)
# out.close()