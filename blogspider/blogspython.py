from blogspider import get_more_links
from bs4 import BeautifulSoup
import requests


def blog_info(url, data=None):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')

    status = soup.select('div.postDesc')
    title = soup.select('#cb_post_title_url')
    content = soup.select('div.postBody')

    if data == None:
        for title,content,status in zip(title,content,status):
            data = {
                'title': title.text,
                'content': content.text,
                'pub_time': status.select('span')[0].text,
                'author': status.select('a')[0].text,
                'read_times': status.select('span')[1].text,
                'catagory': 'python'
            }

    print(data)

blog_info('http://www.cnblogs.com/bigberg/p/6430095.html')#test_url

# for single_url in list(get_more_links(1, 2)):
#     blog_info(single_url)