import requests
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve
import time
import random

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
cookies = {}
with open('C:/Users/lenovo/OneDrive/projects/Scraping/zhihucookies.txt') as file:
    for pair in file.read().split(';'):
        key,value = pair.split('=',1)
        cookies[key] = value;


limit = 20
offset = 20
while(True):
    try:
        url = 'https://zhuanlan.zhihu.com/api/columns/shuaiqiyyc/posts?limit=%d&offset=%d&topic=1307' % (limit, offset)
        r = requests.get(url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(r.text.encode('utf-8'), 'html.parser')
        r1=re.compile('"url": "/p/.*?"')
        datas = str(soup)
        prefix = 'https://zhuanlan.zhihu.com'
        count = 0
        for link in r1.findall(datas):
            link = prefix + str(link)[8:-1]
            print(link)
            story = requests.get(link, headers=headers, cookies=cookies)
            storySoup = BeautifulSoup(story.text.encode('utf-8'),'lxml')
            reForTitle = re.compile('(?<=睡前故事：).+?(?= )')
            try:
                title = reForTitle.findall(storySoup.find('title').contents[0])[0]
            except:
                continue
            img = str(storySoup.select('img'))
            reForImg = re.compile('''(?<=src=').+?(?=')''')
            imgUrl = reForImg.findall(img)[0][2:-2]
            path = r'C:\Users\lenovo\OneDrive\projects\Scraping\stories\\'+title+'.png'
            urlretrieve(imgUrl, path)
            time.sleep(random.randint(0,9))
    except:
        break
    finally:
        count += 1
        limit += 20
        offset += 20
print("Total: %d stories." % count)