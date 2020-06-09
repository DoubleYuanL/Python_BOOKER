# 导入需要用到的模块
import webbrowser
import time
import requests
import os
import random
import re
import requests
from bs4 import BeautifulSoup 
import requests
import os

def get_proxies(uri_IP):
	#注意复制粘贴的HEADERS里不能有奇异的符号
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
	r = requests.get(url=uri_IP,headers=headers)#requests库get方法获取HTML网页
	soup = BeautifulSoup(r.text,"html.parser")
	#bs中的select方法通过类名查找，组合查找。   (".odd > td:nth-of-type(n)")是指class为odd的标签里的第n个类型为td的子标签
	server_address = soup.select(".odd > td:nth-of-type(4)")
	ip_list = soup.select(".odd > td:nth-of-type(2)")               #select对象返回的是列表
	ports_list = soup.select(".odd > td:nth-of-type(3)")
	proxies = []
	num_of_proxies = 0
	for ip,port in zip(ip_list,ports_list):            #zip函数接受任意多个可迭代对象作为参数,将对象中对应的元素打包成一个tuple，后以列表形式输出。
		ip = str(ip).replace('<td>','')
		ip = str(ip).replace('</td>','')
		port = str(port).replace('<td>','')
		port = str(port).replace('</td>','')
		proxies.append("http://"+ip+":"+port)
		num_of_proxies += 1
	return proxies, num_of_proxies

def function(url, proxies):
	# 注：免费的代理IP可以在这个网站上获取：http://www.xicidaili.com/nn/
	r = requests.get(url, proxies=proxies)
	data = r.text
	 
	# 利用正则查找所有连接
	link_list =re.findall(r"(?<=href=\"https://blog.csdn.net/qq_34792438/article/details).+?(?=\")" ,data)
	url_all = []

	num_of_url = 0
	for url in {}.fromkeys(link_list).keys():
		if url == "/99676743":
			continue
		else:
			url_all.append("https://blog.csdn.net/qq_34792438/article/details"+url)
			num_of_url += 1

	url = url_all[random.randint(0, num_of_url-1)]

	r = requests.get(url, timeout=5)
	result = r.status_code

	# 3.如果网页地址有效则打开网页
	if (result == 200):
	    # 4.打开浏览器
	    webbrowser.open(url)
	    # 5.关闭浏览器
	    # os.system('taskkill /F /IM Iexplore.exe')
	    os.system('taskkill /F /IM Chrome.exe')

if __name__=='__main__':
	uri_IP = "http://www.xicidaili.com/nn/"
	proxies_list, num_of_proxies = get_proxies(uri_IP)
	url = 'https://blog.csdn.net/qq_34792438/article/'
	while 1:
		proxies={'http':proxies_list[random.randint(0, num_of_proxies-1)]}
		function(url, proxies)
