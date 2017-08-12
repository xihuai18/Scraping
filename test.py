# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 13:29:17 2017

@author: lenovo
"""
import requests                       #用来请求网页
from bs4 import BeautifulSoup         #解析网页
import time          #设置延时时间，防止爬取过于频繁被封IP号
import re            #正则表达式库
import pymysql       #由于爬取的数据太多，我们要把他存入MySQL数据库中，这个库用于连接数据库
import random        #这个库里用到了产生随机数的randint函数，和上面的time搭配，使爬取间隔时间随机
from PIL import Image
from urllib.request import urlretrieve


#==============================================================================
# cookies = {}
# with open("C:/Users/lenovo/OneDrive/projects/Scraping/doubancookies.txt") as file:
#     raw_cookies = file.read();
#     for line in raw_cookies.split(';'):
#         key,value = line.split('=',1)
#         cookies[key] = value
#     headers = {'User-agent' : 'Mozilla/5.0'}
#     web_data = requests.get(url, cookies=cookies, headers=headers)
#==============================================================================
#for url in channel:


def get_brief(line_tags):
    brief = line_tags[0].contents
    for tag in line_tags[1:]:
        brief += tag.contents
    brief = '\n'.join(brief)
    return brief
    
    
def get_author(raw_author):
    parts = raw_author.split('\n')
    return ''.join(map(str.strip,parts))
    
with open('C:/Users/lenovo/OneDrive/projects/Scraping/testhtml.html', encoding='utf-8') as file:
    html = file.read()

soup = BeautifulSoup(html,'lxml')

#for book in books:
bookSoup = BeautifulSoup(html,'lxml')
info = bookSoup.select('#info')
infos = list(info[0].strings)
try:
    title = bookSoup.select('#wrapper > h1 > span')[0].contents[0]
    publish = infos[infos.index('出版社:') + 1]
    translator = bookSoup.select("#info > span > a")[0].contents[0]
    author = get_author(bookSoup.select("#info > a")[0].contents[0])
    ISBN = infos[infos.index('ISBN:') + 1]
    Ptime = infos[infos.index('出版年:') + 1]
    price = infos[infos.index('定价:') + 1]
    person = bookSoup.select("#interest_sectl > div > div.rating_self.clearfix > div > div.rating_sum > span > a > span")[0].contents[0]
    scor = bookSoup.select("#interest_sectl > div > div.rating_self.clearfix > strong")[0].contents[0]
    coverUrl = bookSoup.select("#mainpic > a > img")[0].attrs['src'];
    brief = get_brief(bookSoup.select('#link-report > div > div > p'))
    print(title, publish, translator, author, Ptime, price, person, scor, ISBN)
    print(brief)
    

except IndexError:
    try:
        title = bookSoup.select('#wrapper > h1 > span')[0].contents[0]
        publish = infos[infos.index('出版社:') + 1]
        translator = ""
        author = get_author(bookSoup.select("#info > a")[0].contents[0])
        ISBN = infos[infos.index('ISBN:') + 1]
        Ptime = infos[infos.index('出版年:') + 1]
        price = infos[infos.index('定价:') + 1]
        person = bookSoup.select("#interest_sectl > div > div.rating_self.clearfix > div > div.rating_sum > span > a > span")[0].contents[0]
        scor = bookSoup.select("#interest_sectl > div > div.rating_self.clearfix > strong")[0].contents[0]
        coverUrl = bookSoup.select("#mainpic > a > img")[0].attrs['src'];
        brief = get_brief(bookSoup.select('#link-report > div > div > p'))
        print(title, publish, translator, author, Ptime, price, person, scor,WISBN)
        print(brief)
    except:
        pass
data = []
path = "C:/Users/lenovo/OneDrive/projects/Scraping/covers/"+title+".png"
urlretrieve(coverUrl,path);
data.append([title,scor,author,price,Ptime,publish,person,translator,'小说',brief,ISBN])