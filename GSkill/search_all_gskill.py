import requests
from bs4 import BeautifulSoup

from sqlalchemy import create_engine
from models import GskillAll
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///motherboard.sqlite3') 

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

for el in range(1,21):
    response = requests.post(f"https://www.gskill.com/ajax.php",headers={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"},data={'Func': 'firstGetProduct','Val': f'2%7C%7C%7C{el}'})#f'165%257C%257C%257C{el}'})
    r = response.json()
    soup = BeautifulSoup(r["html"], 'html.parser')
    soup.find_all("a",attrs={"class":"item"})
    #search = soup.find("div",attrs={"class":"product-list"})
    search = soup.find_all("div",attrs={"class":"list"})
    tovar = []
    for el in search:
        tovar.append({"code":el.find("h4",attrs={"class":"title"}).get("title"),"url":el.find("a",attrs={"class":"item"}).get("href"),"status":0})

    objects = []
    for el in tovar:
        objects.append(GskillAll(**el))
    session.bulk_save_objects(objects)
    session.commit()