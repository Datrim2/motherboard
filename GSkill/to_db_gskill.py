import requests
from bs4 import BeautifulSoup

from sqlalchemy import create_engine
from models import Specifications_Gskill,images_Gskill,GskillAll
# from models import Memory,Specifications_Gskill,images_Gskill
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///motherboard.sqlite3') 

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
# result = session.query(Memory.model).filter(Memory.vendor.like("G.SKILL"),Memory.specifications_id==None).distinct().all()
result = session.query(GskillAll).filter(GskillAll.status == 0).all()
slv_spec = {'Memory Type':'menType', 'Capacity':'capacity', 'Multi-Channel Kit':'multi', 'Tested Speed (XMP/EXPO)':'testSpeed',
 'Tested Latency (XMP/EXPO)':'testLatency','Tested Voltage (XMP/EXPO)':'testVolt', 'Registered/Unbuffered':'register',
 'Error Checking':'err','SPD Speed (Default)':'spdSpeed','SPD Voltage (Default)':'spdVolt','Fan Included':'fan',
 'Warranty':'warranty', 'Features':'features', 'Additional Notes':'addNote','Form Factor':'formFact',
 'Channel Config':'channelConf','SPD Latency (Default)':'spdLat','CAS Latency':'casLat','DRAM Voltage':'dramVolt'}
for elements in result:
    # print(elements[0].replace('(Profile2)',''))
    # response_url = requests.get(f"https://www.gskill.com/search?keywords={elements[0].replace('(Profile2)','')}",headers={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"})
    # print(response_url.url)
    # soup = BeautifulSoup(response_url.text, 'html.parser')
    # search_url = soup.find("div",attrs={"class":"list"})
    # if not search_url:
        # continue
    # search_url = search_url.find_all("a",attrs={"class":"item"}) 
    # if not len(search_url)<=1:
    #     raise Exception("Несколько url")
    # search_url = search_url[0].get("href").replace("product","specification") 
    # response = requests.get(f"https://www.gskill.com{search_url}",headers={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"})
    url_par = elements.url.replace("product","specification")
    response = requests.get(f"https://www.gskill.com{url_par}",headers={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"})
    print(response.url)
    # if response.ok:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('div',attrs={"class":"list-inner"})
    data = { slv_spec[el.find("div",attrs={"class":"list-tit"}).text] : el.find_all("div",attrs={"class":"list-block"})[1].text.replace("\n"," ") for el in table if el != "\n" }
    img = [ requests.get("https://www.gskill.com"+el.find("a").get("href")).content for el in soup.find("div",attrs={"class":"slider slider-for"}) if el != "\n" ]
    data["name"] = soup.find("div",attrs={"class":"font-25 sub-title"}).text.replace("\r\n"," ")
    data["code"] = soup.find("h1",attrs={"class":"font-40 title"}).text
    data["description"] = soup.find("p",attrs={"class":"info"}).text
    
    spec = Specifications_Gskill(**data)
    session.add(spec)
    session.commit()
    
    objects = []
    for el in img:
        objects.append(images_Gskill(spec_id=spec.id,img=el))
    session.bulk_save_objects(objects)
    elements.status = 1
    session.commit()
        
        # add_id_ram = session.query(Memory).filter(Memory.model.like(f"{elements[0]}")).all()
        # for el in add_id_ram:
        #     el.specifications_id = spec.id
        # session.commit() 