import smtplib
from email.mime.text import MIMEText
import requests
# from lxml import etree
import os
import time
import sys

class mailhelper(object):
    def __init__(self):
        self.mail_host="smtp.sina.com"
        self.mail_user="wangzhitian1987"
        self.mail_pass="wzt1987"
        self.mail_postfix="sina.com"

    def send_mail(self, to_list, sub, content):
        me = "wangzhitian" + "<" + self.mail_user + "@" +self.mail_postfix +">"
        msg = MIMEText(content, _subtype='plain',_charset='utf_8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user, self.mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception as e:
            print(str(e))
            return False

class helper(object):
    def __init__(self):
        self.url = "http://weibo.cn/u/1890493665"
        self.url_login = "https://login.weibo.cn/login/"
        self.new_url = self.url_login

    def getSource(self):
        html = requests.get(self.url).content
        return html

    def getData(self, html):
        selector = etree.HTML(html)
        password = selector.xpath('//input[@type="password"]/@name')[0]
        vk = selector.xpath('//input[@name="vk"]/@value')[0]
        action = selector.xpath('//form[@method="post"]/@action')[0]
        self.new_url = self.url_login + action

        data = {
            'mobile': 'xiqikun@163.com',
            'password':'sdlakf',
            'remember':'on',
            'backURL':'http://weibo.cn/u/1999283293',
            'backTitle':'weibo',
            'tryCount':'',
            'vk': vk,
            'submit':'login'
        }
        return data

    def getContent(self, data):
        newhtml = requests.post(self.new_url, data=data).content
        new_selector = etree.HTML(newhtml)
        content = new_selector.xpath('//span[@class = "ctt"]')
        newcontent = unicode(content[2].xpath('string(.)')).replace('http://','')
        sendtime = new_selector.xpath('//span[@class="ct"]/text()')[0]
        sendtext = newcontent + sendtime
        return sendtext

    def tosave(self, text):
        f = open('weibo.txt', 'a')
        f.write(text + "\n")
        f.close()

    def tocheck(self, data):
        if not os.path.exists('weibo.txt'):
            return True
        else:
            f = open('weibo.txt', 'r')
            existweibo = f.readlines()
            if data + '\n' in existweibo:
                return False
            else:
                return True


if __name__ == '__main__':
    mailto_list = ['1807520300@qq.com']
    helper = helper()
    while True:
        source = helper.getSource()
        data = helper.getData(source)
        content = helper.getContent(data)
        if helper.tocheck(content):
            if mailhelper().send_mail(mailto_list,"更新了",content):
                print("send success!!")
            else:
                print("send failed!!")
            helper.tosave(content)
            print(content)
        else:
            print("pass")
        time.sleep(20)
