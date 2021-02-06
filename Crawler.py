import csv
import requests
import pandas
from bs4 import BeautifulSoup


def str2num(x):
    res,cnt = 0,0
    for i in x:
        if(cnt==0 and not (i==',' or i=='.')):
            res = res*10+ord(i)-ord('0')
            continue
        elif(i=='.'):
            cnt=1
            continue
        elif(i!=','):
            res = res+(ord(i)-ord('0'))*(1/(10**cnt))
            cnt+=1
    return round(res,2)

def process_text(x):
    res = ""
    for i in x:
        if(i != "\n" and i != "\r" and i != " "):
            res+=i
    return res

def get_data():
    with open("MBB_stock_price.csv", "w", encoding="utf-8") as infile:
        writer = csv.writer(infile)
        fst = "https://www.cophieu68.vn/historyprice.php?currentPage="
        snd = "&id=mbb"
        for i in range(1,48):
            link = fst + str(i) + snd
            print(link)
            r = requests.get(link, verify = False)
            soup = BeautifulSoup(r.content,'html.parser')
            table = list(soup.find('div',{'id' : 'content'}).find('table'))
            #print(table)
            if(i==1):
                title = table[1]
                tits = []
                for th in title.find_all('td'):
                    need = process_text(th.text)
                    tits.append(need)
                writer.writerow(tits)
            for i in range(2,len(table)):
                if(table[i]=='\n'):
                    continue
                data = []
                for td in table[i].find_all('td'):
                    data.append(process_text(td.text))
                for i in range(2,len(data)):
                    data[i] = str2num(data[i])
                writer.writerow(data)
            # ok = 0


get_data()