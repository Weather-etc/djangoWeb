from py2neo import Graph
from py2neo import Node,NodeMatcher,Relationship
import pandas as pd

#数据库建立连接
graph = Graph("http://localhost:7474",auth=("neo4j","12345678"), name='neo4j')

# 读取csv，获得省份与城市名
data = pd.read_csv('china_city_list.csv', encoding='utf-8')
provinces = data['Province'].drop_duplicates()
cities = data['City']

# 遍历DataFrame的每一行
for index, row in data.iterrows():
    # row是一个pandas的Series对象，表示csv文件的一行数据
    #print(row['City'])
    city = Node('city',name=row['City'])
    province = Node('province',name=row['Province'])
    graph.merge(city,'city','name')
    graph.merge(province,'province','name')
    belongTo = Relationship(city, '归属', province)
    graph.create(belongTo)

