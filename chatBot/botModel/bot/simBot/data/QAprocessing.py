#插入QA数据以及其embedding
import pandas as pd
import sys
import pickle
import pymysql
sys.path.append('..')
from text2vec import SentenceModel, cos_sim, semantic_search

# 连接Mysql
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password="root",
    database='argi',
    port=3512,
    charset='utf8'
)
cursor = conn.cursor()

file_names=['苹果','黄瓜','大豆','小麦','玉米','柑橘','桃','梨','棉花','油菜','猕猴桃','甘蔗','番茄','芝麻','花生','荞麦','菜豆','葡萄','西瓜','谷子','辣椒','高粱','马铃薯','甘薯','木薯']
#将问题embedding，并转化为二进制便于储存
embedder = SentenceModel()
for file_name in file_names:
    data = pd.read_csv('D:\\学习\\实习实训\\最终项目\\数据集\\问题数据集\\' + file_name + '.csv', encoding='utf-8').astype(str)
    corpus = data['问题内容'].tolist()
    corpus_embeddings = embedder.encode(corpus)
    bin_embeddings = []
    for item in corpus_embeddings:
        bin_embeddings.append(pickle.dumps(item))
    # with open('data.pickle', 'wb') as f:
    #     pickle.dump(bin_embeddings, f)
    #
    # with open('data.pickle', 'rb') as f:
    #     bin_embeddings = pickle.load(f)
    # 插入数据库
    for index, item in data.iterrows():
        ques = item['问题内容']
        ans = item['问题解答']
        embedding = bin_embeddings[index]
        # 执行 SQL语句
        res = cursor.execute("INSERT INTO QA (crop,ques,ans,embedding) VALUES (%s,%s,%s,%s)",
                             (file_name, ques, ans, embedding))
        # 必须提交了才生效...
        conn.commit()

cursor.close()
conn.close()

# file_name = '水稻问题_去重版embedding版'
# data = pd.read_csv('D:\\学习\\实习实训\\最终项目\\数据集\\QA\\' + file_name + '.csv', encoding='utf-8').astype(str)
# embeddings = data['embeddings'].tolist()[0:5]
# corpus = []
# for item in embeddings:
#     corpus.append(bytes(pickle.loads(item)))
# print(corpus)