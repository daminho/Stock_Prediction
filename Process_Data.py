import pandas as pd
import matplotlib.pyplot as plt
import cv2
prices = pd.read_csv("MBB_stock_price.csv")

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

average = []
length = len(prices.index)
for i in range(1,length):
    row = list(prices.iloc[i].values)
    average.append(round((row[5]+row[7])/2,2))
class Price:
    open, close, highest, lowest = float, float, float, float
    volume = int

class Stock:
    date,name = str,str


