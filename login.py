import requests                       #用来请求网页
def login():
		cookies = {}
		with open("C:/Users/lenovo/OneDrive/projects/Scraping/doubancookies.txt") as file:
		    raw_cookies = file.read();
		    for line in raw_cookies.split(';'):
		        key,value = line.split('=',1)
		        cookies[key] = value
		url = 'https://www.douban.com/tag/%E8%AF%BB%E4%B9%A6/?source=search'
		s = requests.get(url, cookies=cookies)
		return s  