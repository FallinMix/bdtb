#coding:utf-8
import urllib
import urllib2
import re

baseURL = "http://tieba.baidu.com/p/3138733512"

class BDTB():
	"""docstring for BDTB"""
	def __init__(self, baseURL, seeLz):
		self.baseURL = baseURL
		self.seeLz = '?see_lz=' + str(seeLz)

	def getPage(self, pageNum):
	 	try:
	 		url = self.baseURL + self.seeLz + '&pn=' + str(pageNum)
	 		request = urllib2.Request(url)
	 		response = urllib2.urlopen(request)
	 		print response.read()
	 		return response
	 	except urllib2.URLError as e:
	 		if hasattr(e, "reason"):
	 			print u"连接百度贴吧失败，错误原因：", e.reason
	 			return None

bdtb = BDTB(baseURL, 1)
bdtb.getPage(1)
		