# -*- coding: utf-8 -*-


import requests                       #用来请求网页
from bs4 import BeautifulSoup         #解析网页
import time          #设置延时时间，防止爬取过于频繁被封IP号
import re            #正则表达式库
import pymysql       #由于爬取的数据太多，我们要把他存入MySQL数据库中，这个库用于连接数据库
import random        #这个库里用到了产生随机数的randint函数，和上面的time搭配，使爬取间隔时间随机



#获取网页目录并放入数据库
url = "https://book.douban.com/tag/?view=type&icn=index-sorttags-all"
wb_data=requests.get(url)
soup = BeautifulSoup(wb_data.text,'lxml')
tags = soup.select('#content > div > div.article > div > div > table > tbody > tr > td > a')
connection = pymysql.connect(host='localhost',user='root',password='midnGl8a3nd')
with connection.cursor() as cursor:
    sql = "USE DOUBAN_DB;"
    cursor.execute(sql)
    channel = []
    for tag in tags:
        tag = tag.get_text()
        herf = "https://book.douban.com/tag/"
        url = herf + str(tag) + "\n"
        channel.append(url)

with open('channel.txt','w') as file:
    file.writelines(channel)
    
    
        
        

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    