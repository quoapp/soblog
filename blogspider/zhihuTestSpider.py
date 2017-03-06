from bs4 import BeautifulSoup
import requests
import re

def get_xsrf_token(text):
    xsrf = re.search('(?<=name="_xsrf" value=")[^"]*(?="/)', text)
    if xsrf is None:
        return ''
    else:
        return xsrf.group(0)

def crawl_url(req, cookie, target_url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/40.0.2214.111 Chrome/40.0.2214.111 Safari/537.36',
        # 'Referer': 'http://www.zhihu.com/',
    }

    ret = req.get(target_url, headers=headers, cookies=cookie)
    print('crawl status:', ret.status_code)
    print(ret.text)


def get_captcha(req):
    captcha = req.get('http://www.zhihu.com/captcha.gif', stream=True)
    print ('captcha status: ')
    print (captcha)
    f = open('captcha.gif', 'wb')
    for line in captcha.iter_content(10):
        f.write(line)
    f.close()

    print ('Input the captcha')
    captcha_str = input()
    return captcha_str

def get_login_cookies():
    url = 'https://www.zhihu.com'
    login_url = url + '/login/email'
    login_data = {
        '_xsrf': '',
        'password': 'your_name',
        'remember_me': 'true',
        'email': 'your_email'
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Referer': 'https://www.zhihu.com/',
    }

    req = requests.session()
    reqx = req.get(url, headers=headers)
    xsrf = get_xsrf_token(reqx.text)

    login_data['_xsrf']=xsrf.encode('utf-8')
    captcha = get_captcha(req)
    login_data['captcha'] = captcha

    res = req.post(login_url, headers=headers, data=login_data)
    print('login status:', res.status_code)

    cookie = res.cookies
    return req, cookie



if __name__ == '__main__':

    # 获取登录 sesion 和 cookies，用来爬数据
    req, local_cookies = get_login_cookies()

    text = crawl_url(req, local_cookies, 'https://www.zhihu.com/people/tim-wells-55')


    # print(reqx)
#
# response = BeautifulSoup(reqx.text, 'lxml')
#
# print(response)