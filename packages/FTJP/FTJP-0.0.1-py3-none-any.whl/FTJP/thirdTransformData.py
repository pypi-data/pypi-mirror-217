import pandas as pd
#标准化处理
datafile = r'./googleplaystore.csv' #需要进行标准化的数据文件；
data = pd.read_csv(datafile)
data=data[['Installs','Rating','Reviews']]
data = (data - data.mean(axis = 0))/(data.std(axis = 0)) #简洁的语句实现了标准化变换，类似地可以实现任何想要的变换。
data.columns=['In','Ra','Re'] #表头重命名。

transformfile = r'./03transformdata.csv' #标准化后的数据存储路径文件；
print('数据转换——数据标准化\n**********************************')
print(data)
data.to_csv(transformfile, index = False) #数据写入
