import requests
from bs4 import BeautifulSoup
import time
import random
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import jieba as jb
# import jieba.analyse


header = {
'Accept':'*/*',
'Accept-Encoding':'gzip, deflate, sdch, br',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Referer':'https://item.jd.com/11983227.html',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

cook = {
    "Cookie":"o2Control=lastvisit=2; o2-webp=true; unpl=V2_ZzNtbRJ"
             "WRBV1C0dSfxFZBWICRlVKVBZHJV1BVngZDAduUUddclRCFXMUR1ZnGF"
             "4UZAEZXEVcQxBFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3"
             "RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2UnsZVA1"
             "uChRZcmdEJUU4QlJ%2bHl4CVwIiXHIVF0l1DEFUcxERA2cDGlVLXk"
             "URRQl2Vw%3d%3d; __jdv=122270672|baidu-pinzhuan|t_2885"
             "51095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8a"
             "c7d_0_a0611207594140e992dcad6321a38cd1|1488554087242; "
             "ipLoc-djd=1-72-2799-0; ipLocation=%u5317%u4EAC; areaId=1"
             "; __jda=122270672.711998875.1479869402.1488590533.14885"
             "92865.18; __jdb=122270672.1.711998875|18.1488592865;"
             " __jdc=122270672; __jdu=711998875"

}

# page_num = random.sample(range(50), 50)

# for page in page_num:
#     a = ran_num[0]
#     if page == a:


json_for_comment = "https://sclub.jd.com/comment/productPageComments." \
                   "action?productId=11983227&score=0&sortType=3&page=0" \
                   "&pageSize=10&isShadowSku=0&callback=fetchJSON_comment98vv567".format(str(6))

response=requests.get(json_for_comment, headers=header, cookies=cook)

soup=BeautifulSoup(response.text, 'lxml')
print(soup)

# file = open("C:\\Users\\Administrator\\Desktop\\comment_python.txt", "w")
#
# file.write()
# file.close