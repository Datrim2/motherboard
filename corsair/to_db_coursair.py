import requests
from bs4 import BeautifulSoup

from sqlalchemy import create_engine
from models import Memory,Specifications_corsair,Images,CorsairAll
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///motherboard.sqlite3') 

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
slv_spec = {'Fan Included':'fan','Memory Series':'memSeries','Memory Type':'memType','Memory Color':'memColor','SPD Latency':'spdLat',
 'SPD Speed':'spdSpeed','SPD Voltage':'spdVolt','Speed Rating':'spdRat','Compatibility':'compatibility','Memory Size':'memSize',
 'Tested Latency':'testLat','Tested Voltage':'testVolt','Tested Speed':'testSpeed','Heat Spreader':'heatSpread',
 'Package Memory Format':'packMemFormat','Performance Profile':'profile','Package Memory Pin':'packMemPin',
 'Memory Package contents':'memPackCont','Memory Compatibility':'memComp','LED Lighting':'ledLight','Single Zone / Multi-Zone Lighting':'singmultiZone',
 'PMIC Type':'pmicT'}
result = session.query(Memory.model).filter(Memory.vendor.like("CORSAIR"),Memory.specifications_id==None).distinct().all()
for elements in result:
    print(elements[0].replace('(Profile2)','').split()[0])
    url_par = elements[0].replace('(Profile2)','').split()[0]
    response = requests.get(f"https://www.corsair.com/ru/ru/p/json/{url_par}") 
    print(response.url)
    if response.ok:
        dataJSON = response.json()
        insDataSpec ={}
        for el in dataJSON["classifications"]:
            for elem in el["features"]:
                insDataSpec[slv_spec[elem["name"]]]= elem["featureValues"][0]["value"] if len(elem["featureValues"])<=1 else [ element["value"] for element in elem["featureValues"]]
        insDataSpec["code"] = dataJSON["code"]
        insDataSpec["name"] = dataJSON["name"]
        insDataSpec["description"] = dataJSON["summary"]

        insDataImg = []
        if dataJSON["images"]!=None:
            for el in dataJSON["images"]:
                _emp = {}
                if el["imageType"] == 'PRIMARY':
                    _emp["type"] = el["imageType"]
                    _emp["desc"] = el["altText"]
                    try:
                        print(el["url"])
                        _emp["image"] = requests.get("https://www.corsair.com"+el["url"]).content
                    except requests.exceptions.ConnectionError:
                        continue
                    insDataImg.append(_emp)
                else:
                    continue

        insDataCode = []
        for el in dataJSON["baseOptions"]:
            for elem in el["options"]:
                _emp = {}
                _emp["code"] = elem["code"]
                _emp["url"] = elem["url"]
                _emp["status"] = 0
                insDataCode.append(_emp)

        if dataJSON["variantMatrix"]!=None:
            insDataCode2 = []
            for el in dataJSON["variantMatrix"]:
                _emp = {}
                _emp["code"] = el["variantOption"]["code"]
                _emp["name"] = el["variantValueCategory"]["name"]
                _emp["url"] = el["variantOption"]["url"]
                _emp["status"] = 0
                insDataCode2.append(_emp)

        spec = Specifications_corsair(**insDataSpec)
        session.add(spec)
        session.commit()
        
        if dataJSON["images"]!=None:
            objects = []
            for el in insDataImg:
                objects.append(Images(spec_id=spec.id,**el))
            session.bulk_save_objects(objects)
            session.commit()
        
        objects = []
        for el in insDataCode:
            objects.append(CorsairAll(**el))
        session.bulk_save_objects(objects)
        session.commit()
        
        if dataJSON["variantMatrix"]!=None:
            objects = []
            for el in insDataCode2:
                objects.append(CorsairAll(**el))
            session.bulk_save_objects(objects)
        session.commit()
        add_id_ram = session.query(Memory).filter(Memory.model.like(f"{elements[0]}")).all()
        for el in add_id_ram:
            el.specifications_id = spec.id
        session.commit() 