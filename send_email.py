# coding=utf-8
import HTMLParser
from bs4 import BeautifulSoup
import urllib
import socket 
import sys
import re
import time
dicts ={u'零':0, u'一':1, u'二':2, u'三':3, u'四':4, u'五':5, u'六':6,
	 u'七':7, u'八':8, u'九':9, u'十':10, u'百':100, u'千':1000, u'万':10000,
      }
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
index0 = 2
#章
index1 = 52
def parserhtml():
	try:
		html = urllib.urlopen('http://tieba.baidu.com/f?kw=%C9%C1%CB%B8%C8%AD%C3%A2')
		text = html.read(90000)
		soup = BeautifulSoup(text)
		target	= soup.findAll('div', {'class':'threadlist_lz clearfix'})
		for temp in target:
			img = temp.find('img', {'alt':'置顶'})
			if img:
				#link = 'http://tieba.baidu.com' + temp.div.a['href']
				text =  temp.div.a.string
				print text
				pattern = ur'第.+卷'
				match = re.search(pattern, text)
				num0 = 0
				num1 = 0
				if match:
					t = match.group()[1:len(match.group()) - 1]
					#第十章
					if dicts[t[0]] > 9:
						num0 = 1
					else:
						num0 = 0

					for char in t:
						if dicts[char] < 10:
							num0 = num0 + dicts[char]
						else:
							num0 = num0 * dicts[char]

				pattern = ur'第.+章'
				match = re.search(pattern, text[3:])
				if match:
					t = match.group()[1:len(match.group()) - 1]
					if dicts[t[0]] > 9:
						num1 = 1
					else:
						num1 = 0

					for char in t:
						if dicts[char] < 10:
							num1 = num1 + dicts[char]
						else:
							num1 = num1 * dicts[char]		
				if num0 > index0 or (num0 == index0 and num1 > index1):
					num0 = index0
					num1 = index1
					send_mail(mailto_list,"fiction update",text)
					print num0, num1	
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
	print gap
	print time.strftime( ISOTIMEFORMAT, time.localtime() )
	t = threading.Timer(gap, timer)
	t.start() 

if __name__ == "__main__":
	timer()
