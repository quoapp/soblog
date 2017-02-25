from bs4 import BeautifulSoup
import requests
import time
# from soblog.models import Blog


def get_blog_links(category, page):
    links = []
    base_url = 'http://www.cnblogs.com/cate/{}/#p{}'.format(category, page)
    wb_data = requests.get(base_url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # print (soup)

    for link in soup.select('a.titlelnk'):
        links.append(link.get('href'))
        # y = Blog('blog_url':links)
        # if y.is_valid():
        #     y.save()
        # else:
        #     pass
    # print(links)
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
            'author': soup.select('.postDesc a')[0].text if soup.find_all('div','.postDesc a') else None,
            'read_times': get_views_count(url),
            'catagory': 'python'
        }
        time.sleep(1)
        return data
        # print(data)

# get_item_info('python', 1, 2)

# blog_info('http://www.cnblogs.com/Mr-wanwan/p/6439116.html')#test_url