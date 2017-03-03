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
    data_list = []
    sql = "SElECT title,view_times,blog_url,create_time," \
          "comment_times FROM soblog_blog ORDER BY -comment_times LIMIT 30"
    cursor.execute(sql)
    data = cursor.fetchall()
    for data in data:
        data_list.append(data['view_times'])
    # print(data_list)
    return data_list


data_list = get_data_from()

print("max:",np.max(data_list))
print("min:",np.min(data_list))
print("sum:",np.sum(data_list))
print("mean:",np.mean(data_list))
print("median:",np.median(data_list))
# print("mode:",mode(data_list))
print("min:",np.min(data_list))
print("range:",np.max(data_list)-np.min(data_list))
print("SD:",np.std(data_list))
print("variance:",np.var(data_list))

a,b = np.histogram(data_list,bins=10)
print(a)
print(b)
plt.hist(data_list,bins=[18, 119, 220, 321.9, 423, 524.5,
                         625, 727, 828, 929, 1031 ])
plt.show()