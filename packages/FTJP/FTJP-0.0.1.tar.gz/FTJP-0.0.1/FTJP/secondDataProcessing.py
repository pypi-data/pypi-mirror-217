import pandas as pd
import numpy as np
aa = r'./googleplaystore.csv'
df = pd.DataFrame(pd.read_csv(aa))
# 数据规约
df1=df[['App','Installs','Rating','Reviews']]
df2=df1.groupby('App').agg({'Installs': 'sum','Rating':'sum','Reviews':'sum'})
print(df2)
resultfile=r'./02result_data.csv'
df2.to_csv(resultfile)#导出结果
