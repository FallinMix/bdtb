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
	 		#print response.read()
	 		return response.read()
	 	except urllib2.URLError as e:
	 		if hasattr(e, "reason"):
	 			print u"连接百度贴吧失败，错误原因：", e.reason
	 			return None

	def getResultGroup(self, result):
	 	if result:
	 		print result.group(1)
	 		return result.group(1).strip()
	 	else:
	 		return None

	def getTitle(self):
	 	page = self.getPage(1)
	 	pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>', re.S)
	 	result = re.search(pattern, page)
	 	return self.getResultGroup(result)

	def getPageNum(self):
	 	page = self.getPage(1)
	 	pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
	 	result = re.search(pattern, page)
	 	return self.getResultGroup(result)

	def getContent(self, page):
		pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
		items = re.findall(pattern, page)
		for item in items:
			print item


bdtb = BDTB(baseURL, 1)
page = bdtb.getPage(1)
bdtb.getContent(page)
		