# coding=utf-8
import HTMLParser
from bs4 import BeautifulSoup
import urllib
import socket 
import sys
import re
import time

import smtplib  
from email.mime.text import MIMEText  
import threading  
mailto_list=['172776024@qq.com'] 
mail_host="smtp.126.com"  #设置服务器
mail_user="fictionupdate"    #用户名
mail_pass="fictionupdate123"   #口令 
mail_postfix="126.com"  #发件箱的后缀

import logging
 
# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log\myapp.log',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-8s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

def send_mail(to_list,sub,content):  

    me="hello"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)
        return False  

#卷
#index0 = 2
#章
#index1 = 52
def parserhtml():
	try:

		html = urllib.urlopen('http://tieba.baidu.com/f?kw=%C9%C1%CB%B8%C8%AD%C3%A2')
		text = html.read(90000)
		soup = BeautifulSoup(text)
		target	= soup.findAll('div', {'class':'threadlist_lz clearfix'})
		old_chapter = u''
		lst = [ line.strip().replace('\n','').decode('utf-8') for line in file('lastest_chapter.txt')]
		#logging.info('old_chapter: %s', lst)
			#print 'old_chapter', old_chapter

		for temp in target:
			img = temp.find('img', {'alt':'置顶'})
			if img:
				#link = 'http://tieba.baidu.com' + temp.div.a['href']
				text =  temp.div.a.string
				text = text.strip()
				logging.info('parser_content: %s', text)
				#print 'parser_content', text

				pattern = ur'第.+卷.+第.+章'
				match = re.search(pattern, text)
				if match:
					#print match.end()
					new_chapter = text[match.end():len(text)]
					new_chapter = new_chapter.strip()
					if new_chapter not in lst:
						send_mail(mailto_list,"fiction update",text)
						logging.info('update!new_chapter: %s', new_chapter)	
						#print 'update!new_chapter', new_chapter
						file_handle = open ( 'lastest_chapter.txt', 'a+')
						file_handle.write('\n' + new_chapter.encode('utf-8'))
						file_handle.close()
			else:
				break
		#print target.div.a['href']
		#print target.div.img

		#output rocommend2.div.a

	except socket.error, msg:
		print 'error'


def timer():
	parserhtml()
	ISOTIMEFORMAT='%Y-%m-%d %X'
	#10分钟
	gap = 600
	if time.localtime(time.time()).tm_hour == 0:
		gap = 60 * 7
	if time.localtime(time.time()).tm_hour > 7:
		gap = 600

	logging.info('gap_time: %ss\n', gap)
	#print 'gap_time', gap, 's'
	print time.strftime( ISOTIMEFORMAT, time.localtime() )
	t = threading.Timer(gap, timer)
	t.start() 

if __name__ == "__main__":
	timer()
