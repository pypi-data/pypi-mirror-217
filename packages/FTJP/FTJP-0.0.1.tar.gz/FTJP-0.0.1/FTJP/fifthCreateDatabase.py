import sqlite3
# 连接到SQLite数据库
# 数据库文件是zqy.db，如果文件不存在，会自动在当前目录创建
conn = sqlite3.connect('./ResultData.db')
# 创建一个Cursor
cursor = conn.cursor()
# 执行一条SQL语句，创建HousePrice表
cursor.execute('create  table  UserInfo (id int(10)  primary key, Recency float(100),Frequency float(100),Monetary float(100),ClusterCategory int(10) )')
# 关闭游标
cursor.close()
# 关闭Connection
conn.close()