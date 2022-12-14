import requests
from bs4 import BeautifulSoup

from sqlalchemy import create_engine
from models import Memory,Specifications_corsair,Images,CorsairAll
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///motherboard.sqlite3') 

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

response = requests.get("https://www.xpg.com/ru/xpg/category/computer-memory",verify=False)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find_all("ul",attrs={"class":"product-list-content"}) 
