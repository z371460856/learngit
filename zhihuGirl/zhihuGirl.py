#-*- coding: utf-8 -*-
from spider import SpiderHTML
import sys
from urllib.request import urlopen
import http
import os
import random
import re
import time


store_path='/home/shanks/py/zhihuGirl'
class zhihuCollectionSpider(SpiderHTML):
	def __init__(self,url):
		
		self._url=url


		self.downLimit=0
	def start(self):
		#page number in collection
		for page in range(3,10):
			url=self._url+str(page)
			content=self.getUrl(url)
			questionList=content.findAll("div",{"class":"zm-item"})
			#question in collection
			for question in questionList:
				Qtitle = question.find("h2",{"class":"zm-item-title"})
				if Qtitle is None:
					continue
				questionStr=Qtitle.a.string
				Qurl='https://www.zhihu.com'+Qtitle.a['href']
				#Qtitle=re.sub(r'[\\/:*?<>]','#',Qtitle.a.string) 
				print("----get the question: "+"Qtitle"+"----")
				Qcontent=self.getUrl(Qurl)
				answerList=Qcontent.findAll("div",{"class":"zm-item-answer zm-item-expanded"})
				self._processAnswer(answerList,Qtitle)
				time.sleep(5)

			  
	def _processAnswer(self,answerList,Qtitle):
		j=0
		for answer in answerList:
			j = j+1
			upvoted=int(answer.find("span",{"class":"count"}).string.replace('K','000'))
			if upvoted < 100:
				pass
			authorInfo=answer.find("div",{"class":"zm-item-answer-author-info"})
			author={'introduction':'','link':''}
			try:
				author['name']=authorInfo.find("a",{"class":"author-link"}).string
				author['introdution']=str(authorInfo.find("span",{"class":"bio"})['title'])
			except AttributeError:
				author['name']='anonymous name'+str(j)

			except TypeError:
				pass

			try:
				author['link']=authorInfo.find("a",{"class":"author-link"})['href']
			except TypeError:
				pass


			file_name=os.path.join(store_path,str(Qtitle),'info',author['name']+'_info.txt')
			#already scraping
			if os.path.exists(file_name):
				continue
			self.saveText(file_name,'{introduction}\r\n{link}'.format(**author))
			print("getting user'{name}' answer".format(**author))
			answerContent=answer.find("div",{"class":"zm-editable-content clearfix"})
			if answerContent is None:
				continue
			imgs=answerContent.findAll("img")
			if len(imgs) ==0:
				pass
			else:
				self._getImgFromAnswer(imgs,Qtitle,**author)

	def _getImgFromAnswer(self,imgs,Qtitle,**author):
		i=0
		for img in imgs:
			if 'inline-image' in img['class']:
				continue
			i = i + 1
			imgUrl = img['src']
			extension = os.path.splitext(imgUrl)[1]
			path_name=os.path.join(store_path,str(Qtitle),author['name']+'_'+str(i)+extension)
			print("Image_crawedUrl: "+imgUrl)
			print("Image_Save_Path: "+path_name)
			try:
				self.saveImg(imgUrl,path_name)
			except ValueError:
				pass
			except KeyError:
				pass
			except Exception as e:
				print(str(e))
				pass
if __name__=='__main__':
	'''
	page,limit,parasNum=1,0,len(sys.argv)
	if parasNum>=3:
		page,pageEnd=sys.argv[1],sys.argv[2]
	elif parasNum==2:
		page=sys.argv[1]
		pageEnd=page
	else:
		page,pageEnd=1,1
	'''

	url='https://www.zhihu.com/collection/69135664?page='

	spider=zhihuCollectionSpider(url)
	spider.start()

                
