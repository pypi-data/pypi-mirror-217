#-*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pandas import to_datetime
#引入sklearn框架，导入K均值聚类算法
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
#from sklearn.manifold import
# 在代码中添加如下语句 —— 设置字体为：SimHei（黑体）
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签（中文乱码问题）
##########################################################
def showTest():
  inputfile = r'./zqy_data/03transformdata.csv'  # 待聚类的数据文件
  # 读取数据并进行聚类分析
  data = pd.read_csv(inputfile)  # 读取数据
  # 利用K-Means聚类算法对客户数据进行客户分群，聚成4类
  k = 4  # 需要进行的聚类类别数
  iteration = 500
  kmodel = KMeans(n_clusters=k, max_iter=iteration)
  kmodel.fit(data)  # 训练模型
  r1 = pd.Series(kmodel.labels_).value_counts()
  r2 = pd.DataFrame(kmodel.cluster_centers_)
  r = pd.concat([r2, r1], axis=1)
  r.columns = list(data.columns) + [u'聚类数量']
  r3 = pd.Series(kmodel.labels_, index=data.index)
  r = pd.concat([data, r3], axis=1)
  r.columns = list(data.columns) + [u'聚类类别']
  outputfile = r'./zqy_data/04data_type.csv'  # 结果输出文件
  print(r)
  r.to_csv(outputfile)
  ################################
  ### 绘制图片显示
  kmodel.cluster_centers_
  kmodel.labels_
  plt.rcParams['font.sans-serif'] = ['SimHei']
  plt.rcParams['axes.unicode_minus'] = False
  for i in range(k):
    cls = data[r[u'聚类类别'] == i]
    cls.plot(kind='kde', linewidth=2, subplots=True, sharex=False)
    plt.suptitle('客户群=%d;聚类数量=%d' % (i, r1[i]))
  plt.legend()
  plt.show()

