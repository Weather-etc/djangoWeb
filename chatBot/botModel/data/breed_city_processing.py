#处理csv文件，找出品种适宜种植的城市
from py2neo import Graph
from py2neo import Node,NodeMatcher,Relationship
import pandas as pd
import jieba

def rep(profile):
    profile = profile.replace('西南','四川、云南、贵州')
    profile = profile.replace('长江流域', '四川、云南、重庆、湖北、湖南、江西、安徽、江苏、上海')
    profile = profile.replace('京、津、唐', '北京、天津、河北')
    profile = profile.replace('黄淮', '河南、山东、安徽、江苏')
    profile = profile.replace('东北', '辽宁、吉林、黑龙江')
    return profile


#数据库建立连接
graph = Graph("http://localhost:7474",auth=("neo4j","12345678"), name='neo4j')
file_names=['主要作物','杂粮','果树','棉麻','油料作物','糖烟','茶桑','蔬菜','薯类']
# 读取csv，获得省份与城市名
data = pd.read_csv('china_city_list.csv', encoding='utf-8')
provinces = data['Province'].drop_duplicates()
cities = data['City']

#西南、长江流域
for file_name in file_names:
    ########################
    #修改文件路径
    ########################
    data = pd.read_csv('D:\\学习\\实习实训\\最终项目\\数据集\\' + file_name + '.csv', encoding='utf-8').astype(str)
    for index, item in data.iterrows():
        name = item['品种名称']
        profile = item['全国品审会审定意见']
        #将地理简称替换为省份
        profile = rep(profile)
        # 查询该品种节点
        # node_matcher = NodeMatcher(graph)
        # node = Node(node_matcher.match("品种").where(品种名称=name).first())
        breedNode = graph.evaluate(f"MATCH (n:品种) WHERE n.品种名称 = '{name}' RETURN n")
        words = jieba.lcut(profile)
        #分词后匹配适宜省份
        for word in words:
            if word in provinces.array:
                provinceNode = graph.evaluate(f"MATCH (n:province) WHERE n.name = '{word}' RETURN n")
                suitable = Relationship(breedNode, '适宜', provinceNode)
                graph.create(suitable)



