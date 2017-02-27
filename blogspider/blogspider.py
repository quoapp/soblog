from bs4 import BeautifulSoup
import requests
import time
import sys
from soblog.models import Blog

#获取分类与多页内部的博客列表的链接
def get_blog_links(category, start, end):
    links = []
    for page in range(start, end):
        base_url = 'http://www.cnblogs.com/cate/{}/#p{}'.format(category, str(page))
        wb_data = requests.get(base_url)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        time.sleep(1)

        try:
            for link in soup.select('a.titlelnk'):
                links.append(link.get('href'))
                return links
                time.sleep(1)
        except Exception as e:
            print('ERROR!!',e)


def get_views_count(url):
    id = url.split('/')[-1].strip('.html')
    apik = 'http://www.cnblogs.com/mvc/blog/ViewCountCommentCout.aspx?postId={}'.format(id)
    js = requests.get(apik)
    views = js.text
    return views


def get_comment_count(url):
    id = url.split('/')[-1].strip('.html')
    apik = 'http://www.cnblogs.com/mvc/blog/GetComments.aspx?postId={}&' \
           'blogApp=giserliu&pageIndex=0&anchorCommentId=0&_=1488121987015'.format(id)
    js = requests.get(apik)
    comments = js.text.split(':')[1].split(',')[0]
    # print(comments)
    return comments


def get_item_info(category, start, end):
    urls = get_blog_links(category, start, end)

    for slink in urls:
        wb_data = requests.get(slink)
        soup = BeautifulSoup(wb_data.text,'lxml')
        data = {
            'title': soup.select('.postTitle')[0].text if soup.find_all('h1','postTitle') else None,
            'content': soup.select('.postBody')[0].text if soup.find_all('div','postBody') else None,
            'create_time': soup.select('#post-date')[0].text,
            # 'author': soup.select('.postDesc a')[0].text if soup.find_all('div','.postDesc a') else None, #外键
            'view_times': get_views_count(slink),
            # 'catagory': 'python', #数据库表为外键，不能这样加入，
            'blog_url': slink,
            'comment_times':get_comment_count(slink),
        }
        time.sleep(2)
        try:    #整理存入数据库。注意mysql编码格式需调整。
            y = Blog(**data)
            y.save()
            # print(data,'ok')
        except Exception as e:
            print(e,'can not insert to db!!')

# get_item_info('python', 2, 4)
