#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import re

#zhuchi





#yige url
def add_new_url(url):
	global new_urls

	global old_urls
	if url is None:
		return
	if url not in new_urls and url not in old_urls:
		new_urls.add(url)

#duoge url
def add_new_urls(urls):
	if urls is None or len(urls)==0:
		return
	for url in urls:
		add_new_url(url)

#you daipaqu de url?
def has_new_url():
	global new_urls
	return len(new_urls)!=0

#new_urls tanchu yige url
def get_new_url():
	global new_urls
	global old_urls
	new_url = new_urls.pop()
	old_urls.add(new_url)
	return new_url

def download(url):
	if url is None:
		return None
	response = urlopen(url)
	if response.getcode()!=200:
		return None
	return response.read()

def parse_url(page_url,html_cont):
	if page_url is None or html_cont is None:
		return
	soup = BeautifulSoup(html_cont,'lxml')
	newUrls=get_page_url(page_url,soup)
	newData=get_page_data(page_url,soup)
	return newUrls,newData

def get_page_url(page_url,soup):
	newUrls=set()
	links=soup.find_all("a",href=re.compile(r"/view/\d+\.htm"))
	for link in links:
		new_url=link['href']
		new_full_url=urljoin(page_url,new_url)
		newUrls.add(new_full_url)
	return newUrls

def get_page_data(page_url,soup):
	res_data={}
	#url
	res_data['url']=page_url
	#<dd class="lemmaWgt-lemmaTitle-title"> <h1>Python<h1>
	title_node=soup.find("dd",{"class":"lemmaWgt-lemmaTitle-title"}).find ("h1")
	res_data['title']=title_node.get_text()
	


	#<div class="lemma-summary">
	summary_node =soup.find("div",{"class":"lemma-summary"})
	#type(summary_node.get_text()) is 'str'

	res_data['summary']=summary_node.get_text()
	


	return res_data

def collect_data(new_data):
	global datas
	if new_data is None:
		return
	datas.append(new_data)

def output_html(dataList):
	fout = open('output.html','w')
	fout.write("<html>")
	fout.write("<body>")
	fout.write("<table>")
	for data in dataList:
		fout.write("<tr>")
		fout.write("<td>%s</td>"%data['url'])
		fout.write("<td>%s</td>"%data['title'].encode('utf-8'))
		fout.write("<td>%s</td>"%data['summary'].encode('utf-8'))
		fout.write("</tr>")
	fout.write("</table>")
	fout.write("</body>")
	fout.write("</html>")

	fout.close()



if __name__ == '__main__':
	

	rootUrl="http://baike.baidu.com/view/21087.htm"
	count=1
	#daipaqu
	new_urls=set()
	#yipaqu
	old_urls=set()
	#yemian shuju
	datas=[]
	add_new_url(rootUrl)
	while has_new_url:
		try:
			new_url=get_new_url()
			print('craw%d: %s'%(count,new_url))
			html_cont=download(new_url)
			new_page_urls,new_page_data=parse_url(new_url,html_cont)
			add_new_urls(new_page_urls)
			collect_data(new_page_data)
			if count==10:
				break
			count=count+1
		except:
			print('craw failed')
	output_html(datas)
