import sys
sys.path.append('..')
import pymysql
import pickle
import torch
from text2vec import SentenceModel, cos_sim, semantic_search

class SimBot:
    def __init__(self) -> None:
        # 连接Mysql
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password="Sg1#iIj?4.iP",
            database='qa',
            port=3306,
            charset='utf8'
        )
        self.cursor = conn.cursor()
        self.embedder = SentenceModel()


    def query(self, sentence, entity_dict):
        entities = list(entity_dict.keys())
        sentence_embedding = self.embedder.encode(sentence)
        #找出指定crop的问题embeddings与id
        select_sql = f"SELECT embedding, id FROM QA WHERE crop = '{entities[0]}' "
        self.cursor.execute(select_sql)
        res = self.cursor.fetchall()
        #如果实体没有相关问题，就交给GPT
        if len(res)==0:
            return {"entities":entity_dict, "agent": 1, "content": 'fallback_gpt'}
        corpus_embeddings = []
        ids = []
        for item in res:
            #将pickle格式的bytes字串转换为python类型（ndarray），再转成torch的tensor
            corpus_embeddings.append(torch.from_numpy(pickle.loads(item[0])))
            ids.append(item[1])
        #相似度匹配
        hits = semantic_search(sentence_embedding, corpus_embeddings, top_k=3)
        #查看相似问题 debug用
        ans = ""
        for item in hits[0]:
            select_sql = f"SELECT ques FROM QA WHERE id = {ids[item['corpus_id']]} "
            self.cursor.execute(select_sql)
            res = self.cursor.fetchone()
            sco = str(item['score'])
            ques = res[0]
            ans += str('score:' + sco + ' ' + ques + '\n')


        hit = hits[0][0]
        #如果相似度小于阈值，就交给GPT
        if hit['score'] < 0.88:
            return {"entities":entity_dict, "agent": 1, "content": 'fallback_gpt'}
        select_sql = f"SELECT ans FROM QA WHERE id = {ids[hit['corpus_id']]} "
        self.cursor.execute(select_sql)
        res = self.cursor.fetchone()
        ans += str(res[0])
        return {"entities":entity_dict, "agent": 1, "content": ans}
        # return {"agent":1,"content":'fallback_gpt'}