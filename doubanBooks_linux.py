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


def get_brief(line_tags):
    brief = line_tags[0].contents
    for tag in line_tags[1:]:
        brief += tag.contents
    brief = '\n'.join(brief)
    return brief
    
    
def get_author(raw_author):
    parts = raw_author.split('\n')
    return ''.join(map(str.strip,parts))



def crawl():
    # 获取链接
    channel = []
    with open('C:/Users/lenovo/OneDrive/projects/Scraping/channel.txt') as file:
        channel = file.readlines()
    data = [] #存放每一本书的数据
    for url in channel:
        web_data = requests.get(url)
        soup = BeautifulSoup(web_data.text.encode('utf-8'),'lxml')
        tag = url.split("?")[0].split("/")[-1]
        books = soup.select(
                '''#subject_list > ul > li > div.info > h2 > a''')
        for book in books:
            bookurl = book.attrs['href']
            book_data = requests.get(bookurl)
            bookSoup = BeautifulSoup(book_data.text.encode('utf-8'),'lxml')
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
                except:
                    continue
            finally:
                path = "C:/Users/lenovo/OneDrive/projects/Scraping/covers/"+title+".png"
                urlretrieve(coverUrl,path);
                data.append([title,scor,author,price,Ptime,publish,person,translator,tag,brief,ISBN])            
        time.sleep(random.randint(0,9))
    return data
            
            
            
            
            
            
            
            
connection = pymysql.connect(host='localhost',user='root',password='midnGl8a3nd')
with connection.cursor() as cursor:
    sql = "USE DOUBAN_DB;"
    cursor.execute(sql)
    start = time.clock()
    data = crawl()
    sql = '''INSERT INTO allbooks (
    title, scor, author, price, time, publish, person, yizhe, tag, brief, ISBN)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    cursor.executemany(sql, data)
    end = time.clock()
    
    print("Time Usage:", end -start)
    count = cursor.execute('SELECT * FROM allbooks')
    print("Total of books:", count)
    
connection.commit()
connection.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    