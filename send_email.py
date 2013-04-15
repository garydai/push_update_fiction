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
		for line in file('lastest_chapter.txt'):
			lst = line.strip()
			old_chapter = lst.decode('utf-8')
			print 'old_chapter', old_chapter

		for temp in target:
			img = temp.find('img', {'alt':'置顶'})
			if img:
				#link = 'http://tieba.baidu.com' + temp.div.a['href']
				text =  temp.div.a.string
				text = text.strip()
				print 'parser_content', text
				pattern = ur'第.+卷.+第.+章'
				match = re.search(pattern, text)
				if match:
					print match.end()
					new_chapter = text[match.end():len(text)]
					new_chapter = new_chapter.strip()
					if new_chapter != old_chapter:
						send_mail(mailto_list,"fiction update",text)	
						print 'update!new_chapter', new_chapter
						file_handle = open ( 'lastest_chapter.txt', 'w')
						file_handle.write(new_chapter.encode('utf-8'))
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
	print 'gap_time', gap, 's'
	print time.strftime( ISOTIMEFORMAT, time.localtime() )
	t = threading.Timer(gap, timer)
	t.start() 

if __name__ == "__main__":
	timer()
