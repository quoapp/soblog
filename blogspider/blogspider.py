from bs4 import BeautifulSoup
import requests
import time
import sys
from soblog.models import Blog

#获取分类与多页内部的博客列表的链接
def get_blog_links(category, start, end):
    links = []
    count = 0

    try:
        for page in range(start, end):
            base_url = 'http://www.cnblogs.com/cate/{}/{}'.format(category, str(page)) #曾经栽在这里#p，让我错误的怀疑for循环问题。
            print('loading..',base_url)
            wb_data = requests.get(base_url)
            soup = BeautifulSoup(wb_data.text, 'lxml')
            time.sleep(2)

            try:
                for link in soup.select('a.titlelnk'):
                    links.append(link.get('href'))
                    count += 1
                print('%d append in links list!'%count)
            except Exception as e:
                print('ERROR!!',e)
    except Exception as e:
        print('scrap fail:',e)

    urls = set(links)
    # print(urls)
    return urls


def get_views_count(url):
    id = url.split('/')[-1].strip('.html')
    if id.isdigit():
        apik = 'http://www.cnblogs.com/mvc/blog/ViewCountCommentCout.aspx?postId={}'.format(id)
        js = requests.get(apik)
        views = js.text
        return views
    else:
        return 9


def get_comment_count(url):
        id = url.split('/')[-1].strip('.html')
        if id.isdigit():
            apik = 'http://www.cnblogs.com/mvc/blog/GetComments.aspx?postId={}&' \
                   'blogApp=giserliu&pageIndex=0&anchorCommentId=0&_=1488121987015'.format(id)
            js = requests.get(apik)
            comments = js.text.split(':')[1].split(',')[0]
            return comments
        else:
            return 0


def get_item_info(category, start, end):
    urls = get_blog_links(category, start, end)
    count=0
    for slink in urls:
        wb_data = requests.get(slink)
        soup = BeautifulSoup(wb_data.text,'lxml')
        data = {
            'title': soup.select('.postTitle a')[0].text if soup.find_all(attrs={'class':'postTitle'}) else None,
            'content': soup.select('#cnblogs_post_body')[0].text if soup.find_all(attrs={'id':'cnblogs_post_body'}) else None,
            'create_time': soup.select('#post-date')[0].text if soup.find_all(attrs={'id':'post-date'}) else None,
            # 'author': soup.select('.postDesc a')[0].text if soup.find_all('div','.postDesc a') else None, #外键
            'view_times': get_views_count(slink),
            # 'catagory': 'python', #数据库表为外键，不能这样加入，
            'blog_url': slink,
            'comment_times':get_comment_count(slink),
        }
        time.sleep(3)
        try:    #整理存入数据库。注意mysql编码格式需调整。
            y = Blog(**data)
            y.save()
            count += 1
            print('%d insert to db success!'%count)
        except Exception as e:
            print(e,'can not insert to db!!')

# get_item_info('python', 1, 5)
