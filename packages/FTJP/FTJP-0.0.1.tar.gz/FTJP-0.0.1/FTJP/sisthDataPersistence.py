#-*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
# 在代码中添加如下语句 —— 设置字体为：SimHei（黑体）
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签（中文乱码问题）
##########################################################
# 连接到SQLite数据库
# 数据库文件是zqy.db，如果文件不存在，会自动在当前目录创建
conn = sqlite3.connect('./ResultData.db')
# 创建一个Cursor
cursor = conn.cursor()
#####################################################

df = pd.read_csv('./04data_type.csv') # 分析结果

for i in range(0,4945):
    m_id = i+1
    m_rency = df.loc[i][1]
    m_frency = df.loc[i][2]
    m_montery = df.loc[i][3]
    m_catory = df.loc[i][4]
    print(m_id,' ',m_rency,' ',m_frency,' ',m_montery,' ',m_catory)
    sql = 'insert into UserInfo values(?,?,?,?,?)'  # 插入到数据库中
    content = [m_id,m_rency,m_frency,m_montery,m_catory]
    cursor.execute(sql,content)
    conn.commit()
print(df)
#########################################################
# 关闭游标
cursor.close()
# 关闭Connection
conn.close()