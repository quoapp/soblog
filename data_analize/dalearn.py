import pandas as pd
import matplotlib.pyplot as plt

data_url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"

df = pd.read_csv(data_url)

x = df["total_bill"]
y = df['tip']
plt.figure(num=1,)
plt.plot(x, y, 'ro',color='green')
plt.show()