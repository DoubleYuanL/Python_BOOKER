# 导入需要用到的模块
import webbrowser
import time
import requests
import os
import random
import re
from bs4 import BeautifulSoup 
import urllib.request

week = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

print(time.time())
print(time.localtime(time.time()))
print(time.asctime(time.localtime(time.time())))

class proxies():
	"""get proxies from https://"""
	def __init__(self, url_IP=""):
		super(proxies, self).__init__()
		self.url_IP = url_IP
		
	def get_proxies(self):
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
		r = requests.get(url=self.url_IP, headers=headers)#requests库get方法获取HTML网页
		print(self.url_IP)
		soup = BeautifulSoup(r.text, "html.parser")
		ip_list = soup.select("tr > td:nth-of-type(1)")               
		ports_list = soup.select("tr > td:nth-of-type(2)")

		proxies = []
		for ip,port in zip(ip_list,ports_list):            #zip函数接受任意多个可迭代对象作为参数,将对象中对应的元素打包成一个tuple，后以列表形式输出。
			ip = str(ip).replace('\t','')
			ip = str(ip).replace('\n','')
			ip = str(ip).replace('<td>','')
			ip = str(ip).replace('</td>','')

			port = str(port).replace('\t','')
			port = str(port).replace('\n','')
			port = str(port).replace('<td>','')
			port = str(port).replace('</td>','') #这部分写的不好 还需要继续改进 当时为了图简单 就这样写了
			proxies.append("http://"+ip+":"+port)
		return proxies

class CSDN():
	"""docstring for CSDN"""
	def __init__(self, csdn_url,proxies_list):
		self.csdn_url = csdn_url
		self.proxies_list = proxies_list
		self.proxies = {'http':random.choice(self.proxies_list)}

	def get_booker_url_all(self):
		proxy_support = urllib.request.ProxyHandler(self.proxies)

		opener = urllib.request.build_opener(proxy_support)
		opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36')]

		urllib.request.install_opener(opener)

		response = urllib.request.urlopen(self.csdn_url)
		html = response.read().decode('utf-8')

		link_list =re.findall(r"(?<=href=\"https://blog.csdn.net/qq_34792438/article/details).+?(?=\")", html)
		# print(link_list)
		url_all = []
		for url in {}.fromkeys(link_list).keys():
			if url == "/99676743":#这篇booker不需要访问
				continue
			else:
				url_all.append("https://blog.csdn.net/qq_34792438/article/details"+url)
		return url_all

	def check_booker_num(self):
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
		r = requests.get(url=self.csdn_url, headers=headers, proxies=self.proxies)
		booker_Views = re.findall(r"(?<=class=\"text-center\" style=\"min-width:58px\" title=\").+?(?=\")", r.text)

		return booker_Views

	def open_booker(self):
		self.proxies = {'http':random.choice(self.proxies_list)}
		print("self.proxies",self.proxies)
		print("self.csdn_url",self.csdn_url)
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
		r = requests.get(url=self.csdn_url, headers=headers, proxies=self.proxies)

		# result = r.status_code
		# # 3.如果网页地址有效则打开网页
		# if (result == 200):
		#     # 4.打开浏览器
		#     webbrowser.open(self.csdn_url)
		#     # 5.关闭浏览器
		#     # os.system('taskkill /F /IM Chrome.exe')

if __name__=='__main__':
	proxies_list = []
	proxies = proxies()
	if os.path.exists('proxies.txt'):
		with open('proxies.txt') as f:
			line = f.readline()
			while line:
				line = f.readline()
				proxies_list.append(line)
	else:
		filename = open('proxies.txt', 'w')
		for x in range(10):
			proxies.url_IP = "http://www.ip3366.net/?stype=1&page={:d}".format(x+1)
			proxies_url = proxies.get_proxies()
			print("proxies_url", proxies_url)
			proxies_list.append(proxies_url)
			for data in proxies_url:
				filename.write(str(data)+'\n')
		filename.close()

	csdn_url = 'https://blog.csdn.net/qq_34792438/article/'
	csdn = CSDN(csdn_url, proxies_list)

	booker_url_list = csdn.get_booker_url_all()

	booker_Views = csdn.check_booker_num()
	print("博客访问量：",format(int(booker_Views[0])))

	time = 0
	all_time = random.randint(100,5000)
	print(all_time)
	while time < all_time:
		csdn.csdn_url = random.choice(booker_url_list)
		csdn.open_booker()
		time += 1
		if time % 5 == 0:
			print(csdn.check_booker_num())