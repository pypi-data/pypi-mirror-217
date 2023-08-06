#-*- coding: utf-8 -*-
#对数据进行基本的探索
#返回缺失值个数以及最大最小值
import pandas as pd
datafile= r'.\googleplaystore.csv'  #原始数据,第一行为属性标签
data = pd.read_csv(datafile) #读取原始数据，指定UTF-8编码（需要用文本编辑器将数据装换为UTF-8编码）
data=data[['Installs','Rating','Reviews']]
# 将 'Installs', 'Rating', 'Reviews' 列的值转换为数值类型，无法转换的值将变为 NaN
data['Installs'] = pd.to_numeric(data['Installs'], errors='coerce')
data['Rating'] = pd.to_numeric(data['Rating'], errors='coerce')
data['Reviews'] = pd.to_numeric(data['Reviews'], errors='coerce')

# 剔除含有非数字值的行
data = data.dropna(subset=['Installs', 'Rating', 'Reviews'])

view = data.describe(percentiles = [], include = 'all').T #包括对数据的基本描述，percentiles参数是指定计算多少的分位数表（如1/4分位数、中位数等）；T是转置，转置后更方便查阅
view['null'] = len(data)-view['count'] #describe()函数自动计算非空值数，需要手动计算空值数
view['max'] = data.max(numeric_only=True)  # 计算每列的最大值
view['min'] = data.min(numeric_only=True)  # 计算每列的最小值

view = view[['null', 'max', 'min']]
view.columns = [u'空值数', u'最大值', u'最小值'] #表头重命名
'''这里只选取部分探索结果。
describe()函数自动计算的字段有count（非空值数）、unique（唯一值数）、top（频数最高者）、freq（最高频数）、mean（平均值）、std（方差）、min（最小值）、50%（中位数）、max（最大值）'''
resultfile = r'./01view.csv' #数据探索结果表
print(view) # 打印结果
view.to_csv(resultfile) #导出结果
