import pandas as pd
import matplotlib.pyplot as plt
import cv2
from bs4 import BeautifulSoup
import requests
import warnings
warnings.filterwarnings('ignore')
day_info = pd.read_csv("MBB_stock_price.csv")

def str2num(x):
    res,cnt = 0,0
    s = 0
    if(x[0]=='-'):
        s+=1
    for i in range(s,len(x)):
        if(cnt==0 and not (x[i]==',' or x[i]=='.')):
            res = res*10+ord(x[i])-ord('0')
            continue
        elif(x[i]=='.'):
            cnt=1
            continue
        elif(x[i]!=','):
            res = res+(ord(x[i])-ord('0'))*(1/(10**cnt))
            cnt+=1
    if(s==1):
        s=-1
    else:
        s=1
    return s*round(res,2)

def process_text(x):
    res = ""
    for i in x:
        if(i != "\n" and i != "\r" and i != " "):
            res+=i
    return res

class Price:
    reference, open, close, highest, lowest = float,float, float, float, float
    def __init__(self,reference, open,close,highest,lowest):
        self.reference,self.open,self.close,self.highest,self.lowest = reference,open,close,highest,lowest

class Volume:
    volume = int
    prices = []
    def __init__(self,volume,prices):
        self.volume = volume
        self.prices = prices

class Day_Data:
    date = str
    data = Volume
    def __init__(self,date, data):
        self.date = date
        self.data = data

class Stock:
    name = str
    day_data = []
    def __init__(self,name):
        self.name = name
    def new_data(self):
        link = "https://www.cophieu68.vn/historyprice.php?currentPage=1&id=mbb"
        r = requests.get(link, verify=False)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = list(soup.find('div', {'id': 'content'}).find('table'))
        need = table[3]
        row = []
        for i in table[3].find_all('td'):
            row.append(process_text(i.text))
        for i in row:
            i = str2num(i)
        date = row[1]
        reference,close,volume,open,highest,lowest = row[2],row[5],row[6],row[7],row[8],row[9]
        price = Price(reference,open,close,highest,lowest)
        vol = Volume(volume,price)
        day_data = Day_Data(date,vol)
        self.day_data.append(day_data)
    def add(self,day_data):
        self.day_data.append(day_data)
    def SMA(self,x = int):
        sum = 0


def init_MBB():
    length = len(day_info.index)
    for i in range(1, length):
        row = list(day_info.iloc[i].values)
        date = row[1]
        reference, close, volume, open, highest, lowest = row[2], row[5], row[6], row[7], row[8], row[9]
        price = Price(reference, open, close, highest, lowest)
        vol = Volume(volume, price)
        day_data = Day_Data(date, vol)
        MBB.add(day_data)
    MBB.day_data.reverse()

MBB = Stock("MBB")
init_MBB()





