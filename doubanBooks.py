# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 13:29:17 2017

@author: Throne
"""
#每一本书的 1cover 2author 3yizhe(not must) 4time 5publish 6price 7scor 8person 9title 10brief 11tag 12ISBN

import requests                       #用来请求网页
from bs4 import BeautifulSoup         #解析网页
import time          #设置延时时间，防止爬取过于频繁被封IP号
import pymysql       #由于爬取的数据太多，我们要把他存入MySQL数据库中，这个库用于连接数据库
import random        #这个库里用到了产生随机数的randint函数，和上面的time搭配，使爬取间隔时间随机
from urllib.request import urlretrieve     #下载图片
import re             #处理诡异的书名


connection = pymysql.connect(host='localhost',user='root',password='',charset='utf8')
with connection.cursor() as cursor:
    sql = "USE DOUBAN_DB;"
    cursor.execute(sql)
connection.commit()



def deal_title(raw_title):
    r = re.compile('[/\*?"<>|:]')
    return r.sub('~',raw_title)

def get_brief(line_tags):
    brief = line_tags[0].contents
    for tag in line_tags[1:]:
        brief += tag.contents
    brief = '\n'.join(brief)
    return brief
    
    
def get_author(raw_author):
    parts = raw_author.split('\n')
    return ''.join(map(str.strip,parts))

def login(url):
        cookies = {}
        with open("C:/Users/lenovo/OneDrive/projects/Scraping/doubancookies.txt") as file:
            raw_cookies = file.read();
            for line in raw_cookies.split(';'):
                key,value = line.split('=',1)
                cookies[key] = value
        headers = {'User-Agent':'''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'''}
        s = requests.get(url, cookies=cookies, headers=headers)
        return s   

def crawl():
    # 获取链接
    channel = []
    with open('C:/Users/lenovo/OneDrive/projects/Scraping/channel.txt') as file:
        channel = file.readlines()
    for url in channel:
        data = [] #存放每一本书的数据
        web_data = login(url.strip())
        soup = BeautifulSoup(web_data.text.encode('utf-8'),'lxml')
        tag = url.split("?")[0].split("/")[-1]
        books = soup.select(
                '''#subject_list > ul > li > div.info > h2 > a''')
        for book in books:
            bookurl = book.attrs['href']
            book_data = login(bookurl)
            bookSoup = BeautifulSoup(book_data.text.encode('utf-8'),'lxml')
            info = bookSoup.select('#info')
            infos = list(info[0].strings)
            try:
                title = bookSoup.select('#wrapper > h1 > span')[0].contents[0]
                title = deal_title(title)
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
                
            except :
                try:
                    title = bookSoup.select('#wrapper > h1 > span')[0].contents[0]
                    title = deal_title(title)
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
                except:
                    continue
            finally:
                path = "C:/Users/lenovo/OneDrive/projects/Scraping/covers/"+title+".png"
                urlretrieve(coverUrl,path);
                data.append([title,scor,author,price,Ptime,publish,person,translator,tag,brief,ISBN])            
        with connection.cursor() as cursor:
            sql = '''INSERT INTO allbooks (
title, scor, author, price, time, publish, person, yizhe, tag, brief, ISBN)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            cursor.executemany(sql, data)
        connection.commit()
        del data
        time.sleep(random.randint(0,9))
            
            
            
            
            
            
            
            


start = time.clock()
crawl()
end = time.clock()
with connection.cursor() as cursor:
    print("Time Usage:", end -start)
    count = cursor.execute('SELECT * FROM allbooks')
    print("Total of books:", count)
    
if connection.open:
    connection.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    