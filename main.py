#-*- coding:utf-8 -*-
import os
import xml.dom.minidom as minidom
from interface import *

printHeader()

def getText(nodelist):
	rs = ""
	for node in nodelist:
		for child in node.childNodes:
			rs += child.nodeValue 
	return rs

def checkPwd(pwd):
	while True:
		if len(pwd) < 8:
			print "The password must longer than 8 characters."
			pwd = raw_input("Password  : ")
		else:
			return pwd

def writeToXml(ssid, pwd):
	out_file    = open("data.xml", 'w')
	indata_ssid = "<info>\n<ssid>" + ssid + "</ssid>\n"
	indata_key  = "<key>" + pwd + "</key>\n</info>"
	out_file.write(indata_ssid + indata_key)
	out_file.close()	

def echoHandle(cmd):
	str = os.popen(cmd).read()
	return str.decode('cp936').encode('utf-8')

def getTextByTagName(dom,str):
	node = dom.getElementsByTagName(str)
	return getText(node)

if (os.path.exists("data.xml")):
	dom      = minidom.parse("data.xml")
	ssid     = getTextByTagName(dom,"ssid")
	pwd      = getTextByTagName(dom,"key")
	pwd      = checkPwd(pwd)
else:
	printSplit()
	ssid = raw_input("WiFi Name : ")
	pwd  = raw_input("Password  : ")
	pwd  = checkPwd(pwd)
	printSplit()
	print "\n"
	
writeToXml(ssid, pwd)

cmd1 = "netsh wlan set hostednetwork mode=allow ssid=" + ssid + " key=" + pwd
cmd2 = "netsh wlan start hostednetwork"
cmd3 = "netsh wlan stop hostednetwork"
aaa  = "承载网络模式已设置为允许。\n已成功更改承载网络的 SSID。\n已成功更改托管网络的用户密钥密码。\n\n"
bbb  = "已启动承载网络。\n\n"
ccc  = "已停止承载网络。\n\n"

if echoHandle(cmd1) == aaa:
	printSplit()
	print "= SSID     : %s" % ssid
	print "= Password : %s" % pwd
	printSplit()
else:
	print "Please ensure running cmd in admin mode!"
	os._exit(0)

print "=\n=Now please set the status to 'Allow Share'"
raw_input("=If finished, press <ENTER> to continue.\n=")
printSplit()
print "\n"

if echoHandle(cmd2) == bbb:
	printSplit()
	print "=\n=Complete!The hotspot is started."
else:
	print "Sorry, something error. Please contact the author."
	os._exit(0)

raw_input("=If you want to stop, press <ENTER> to close.\n=")
printSplit()
print "\n"

if echoHandle(cmd3) == ccc:
	printSplit()
	print "Complete!"
else:
	print "Sorry, something error. Please contact the author."
	os._exit(0)
