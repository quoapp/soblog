from bs4 import BeautifulSoup
import requests
import time
import sys
from soblog.models import Blog

#获取分类与多页内部的博客列表的链接
def get_blog_links(category, page):
    links = []
    base_url = 'http://www.cnblogs.com/cate/{}/#p{}'.format(category, page)
    wb_data = requests.get(base_url)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    for link in soup.select('a.titlelnk'):
        links.append(link.get('href'))
    return links

def get_more_links(category, start, end):
    for i in range(start, end):
        return get_blog_links(category, str(i))
        time.sleep(1)

def get_views_count(url):
    id = url.split('/')[-1].strip('.html')
    apik = 'http://www.cnblogs.com/mvc/blog/ViewCountCommentCout.aspx?postId={}'.format(id)
    js = requests.get(apik)
    views = js.text
    return views

def get_item_info(category, start, end):
    urls = get_more_links(category, start, end)
    for url in urls:

        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text,'lxml')
        data = {
            'title': soup.select('.postTitle')[0].text if soup.find_all('h1','postTitle') else None,
            'content': soup.select('.postBody')[0].text if soup.find_all('div','postBody') else None,
            'create_time': soup.select('#post-date')[0].text,
            # 'author': soup.select('.postDesc a')[0].text if soup.find_all('div','.postDesc a') else None, #外键
            'view_times': get_views_count(url),
            # 'catagory': 'python', #数据库表为外键，不能这样加入，
            'blog_url': url
        }
        time.sleep(1)
        # return data
        # print(data)
        try:    #整理存入数据库。mysql编码格式需调整。
            y = Blog(**data)
            y.save()
            print('ok')
        except:
            print("fail to insert into db!")

# get_item_info('python', 1, 2)
