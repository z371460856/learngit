#-*- coding: utf-8 -*-
import os
import re
import codecs
from urllib.request import urlopen
import ssl
from bs4 import BeautifulSoup
class SpiderHTML(object):
	#open page
	def getUrl(self,url,coding='utf-8'):
		req=urlopen(url)
		return BeautifulSoup(req.read().decode(coding),'lxml')
	#save file
	def saveText(self,filename,content,mode='w'):
		self._checkPath(filename)
		with codecs.open(filename,encoding='utf-8',mode=mode) as f:
			f.write(content)
	#save img
	def saveImg(self,imgUrl,imgName):
		data=urlopen(imgUrl).read()
		self._checkPath(imgName)
		with open(imgName,'wb') as f:
			f.write(data)
	# make dir
	def _checkPath(self,path):
		dirname=os.path.dirname(path.strip())
		if not os.path.exists(dirname):
			os.makedirs(dirname)