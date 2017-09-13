#coding:utf-8
import urllib
import urllib2
import re
import codecs

baseURL = "http://tieba.baidu.com/p/3138733512"

class Tool():
	#去除img标签和7位长空格
	removeImg = re.compile('<img.*?>| {7}|')
	#删除超链接标签
	removeAddr = re.compile('<a.*?>|</a>')
	#把换行的标签换为\n
	replaceLine = re.compile('<tr>|<div>|</div>|</p>')
	#将表格制表<td>替换为\t
	replaceTD= re.compile('<td>')
	#把段落开头换为\n加空两格
	replacePara = re.compile('<p.*?>')
	#将换行符或双换行符替换为\n
	replaceBR = re.compile('<br><br>|<br>')
	#将其余标签剔除
	removeExtraTag = re.compile('<.*?>')
	def replace(self,x):
		x = re.sub(self.removeImg,"",x)
		x = re.sub(self.removeAddr,"",x)
		x = re.sub(self.replaceLine,"\r\n",x)
		x = re.sub(self.replaceTD,"\t",x)
		x = re.sub(self.replacePara,"\r\n    ",x)
		x = re.sub(self.replaceBR,"\r\n",x)
		x = re.sub(self.removeExtraTag,"",x)
		#strip()将前后多余内容删除
		return x.strip()

class BDTB():
	"""docstring for BDTB"""
	def __init__(self, baseURL, seeLz):
		self.baseURL = baseURL
		self.seeLz = '?see_lz=' + str(seeLz)
		self.tool = Tool()

	def getPage(self, pageNum):
	 	try:
	 		url = self.baseURL + self.seeLz + '&pn=' + str(pageNum)
	 		request = urllib2.Request(url)
	 		response = urllib2.urlopen(request)
	 		#print response.read()
	 		return response.read().decode('utf-8')
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

	def getTitle(self, page):
	 	pattern = re.compile('<h3.*?title=.*?>(.*?)</h3>', re.S)
	 	result = re.search(pattern, page)
	 	return self.getResultGroup(result)

	def getPageNum(self, page):
	 	pattern = re.compile('<li class="l_reply_num".*?<span.*?>.*?<span.*?>(.*?)</span>', re.S)
	 	result = re.search(pattern, page)
	 	return self.getResultGroup(result)

	def getContent(self, page):
		pattern = re.compile('<div.*?j_d_post_content ">(.*?)</div>', re.S)
		contents = []
		items = re.findall(pattern, page)
		for item in items:
			content = "\n" + self.tool.replace(item) + "\n"
			contents.append(content)
		return contents

	def WriteInFile(self, pageFloors, page, title, pages, lzCount):
		f = codecs.open('NBA.txt','a','utf-8')
		#f=open('NBA.txt', 'a')
		f.write(u'【本帖标题：%s, 共%s页】' % (title, pages))
		f.write('\r\n')
		f.write('\r\n')
		f.write(u'========================================第%s页==============================================' % page)
		f.write('\r\n')
		for floor in pageFloors:
			f.write('\r\n')
			f.write(u'------------------------------------楼主发言楼层-%s------------------------------------' % lzCount)
			f.write('\r\n')           
			f.write('\r\n')
			f.write(floor)
			lzCount += 1
			f.write('\r\n')
		f.write('\r\n')
		f.write('\r\n')
		f.write(u'->第%s页帖子到此结束<-' % page)
		f.write('\r\n')
		f.write('\r\n')
		f.close()
		return lzCount

	def start(self):
		firstPage = self.getPage(1)
		title = self.getTitle(firstPage)
		pageNum = int(self.getPageNum(firstPage))
		print u'本帖标题为' + title
		print u'在只看楼主模式下，本贴一共有', pageNum, u'页'
		lzCount = 1
		for page in range(pageNum):
			print u'现将第%s页写入文档NBA.txt' % (page+1)
			print u'正在获取第%s页所有楼主发言楼层' % (page+1)
			pageCode = self.getPage(page+1)
			pageItems = self.getContent(pageCode)
			lzCount = self.WriteInFile(pageItems, page+1, title, pageNum, lzCount)
			print u'第%s页写入完毕' % (page+1)

bdtb = BDTB(baseURL, 1)
bdtb.start()
		