import importlib
import yaml
import pandas as pd

# yaml_path = 'example_breeds.yaml'
# file_names=['主要作物','杂粮','果树','棉麻','油料作物','糖烟','茶桑','蔬菜','薯类']
# names=[]
# for file_name in file_names:
#     data = pd.read_csv('D:\\学习\\实习实训\\最终项目\\数据集\\' + file_name + '.csv', encoding='utf-8').astype(str)
#     for index, item in data.iterrows():
#         name = item['品种名称']
#         names.append(name)
#
# with open(yaml_path, encoding="utf-8", mode="w") as f:
#     yaml.dump(names,stream=f,allow_unicode=True)

# yaml_path = 'example_crops.yaml'
# file_names=['作物简介']
# names=[]
# for file_name in file_names:
#     data = pd.read_csv('D:\\学习\\实习实训\\最终项目\\数据集\\' + file_name + '.csv', encoding='utf-8').astype(str)
#     for index, item in data.iterrows():
#         name = item['作物名称']
#         names.append(name)
#
# with open(yaml_path, encoding="utf-8", mode="w") as f:
#     yaml.dump(names,stream=f,allow_unicode=True)

yaml_path = 'example_cities.yaml'
file_names=['china_city_list']
names=[]
for file_name in file_names:
    data = pd.read_csv('D:\\学习\\实习实训\\最终项目\\' + file_name + '.csv', encoding='utf-8').astype(str)
    for index, item in data.iterrows():
        name = item['City']
        names.append(name)

with open(yaml_path, encoding="utf-8", mode="w") as f:
    yaml.dump(names,stream=f,allow_unicode=True)