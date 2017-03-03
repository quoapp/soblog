# from soblog.models import *

import pymysql
import pandas as pd
import numpy as np
import matplotlib
from tkinter import *
import pymysql.cursors
import matplotlib.pyplot as plt

db = pymysql.connect('localhost','root',
                     '111111','soblog',charset='utf8',
                     cursorclass = pymysql.cursors.DictCursor)
cursor = db.cursor()

def get_data_from():
    sql = "SElECT title,view_times,blog_url,create_time," \
          "comment_times FROM soblog_blog ORDER BY -comment_times LIMIT 30"
    cursor.execute(sql)
    data_list = cursor.fetchall()
    # print(data_list)
    return data_list

def data_show():
    y = []
    for data in get_data_from():
        y.append(data['view_times'])
    return y

y = data_show()
x = range(2000, 2030)
plt.figure()
plt.plot(x, y, 'ro', color='green',)
plt.show()


cursor.close()
db.close()
#
# def hot_blog_analize():
#     list=Blog.objects.filter('title','view_times','blog_url','create_time',
#                              'comment_times').orderby('comment_times')
#     print(list)