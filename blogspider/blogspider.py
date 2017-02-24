from bs4 import BeautifulSoup
import requests
import time

url = 'http://www.cnblogs.com/cate/python/#p'

def get_blog_links(url, data=None):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    links = soup.select('div.post_item_body > h3 > a')
    # time.sleep(2)

    if data == None:
        for link in links:
            data = {
                'link': link.get('href'),
            }
            return data
            # print(data)
def get_more_links(start,end):
    for i in range(start,end):
        get_blog_links(url + str(i))

get_more_links(1,2)

