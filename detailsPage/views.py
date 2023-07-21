import json
from django.shortcuts import render
import requests
from py2neo import Graph

# Create your views here.

user_name = 'neo4j'
user_pass = '12345678'
user_port = '7474'
graph = Graph("http://localhost:{}".format(user_port), auth=(user_name, user_pass), name='neo4j')


def show_detail(request):
    entity = request.GET['entity']

    # search the neo4j database
    answer = graph.run("MATCH (entity1) - [rel] - (entity2) WHERE entity1.品种名称 = \""
                       + str(entity) + "\" RETURN rel, entity2").data()
    if len(answer) == 0:
        answer = graph.run("MATCH (entity1) - [rel] - (entity2) WHERE entity1.name = \""
                           + str(entity) + "\" RETURN rel, entity2").data()

    for rel in answer:
        rel['rel'] = type(rel['rel']).__name__

    # search mysql database
    entity_des = graph.run(f"match (n) where n.name='{str(entity)}' return n.profile").data()
    if len(entity_des) == 0:
        entity_des = graph.run(f"match (n) where n.品种名称='{str(entity)}' return n.全国品审会审定意见").data()
    if len(entity_des) == 0:
        entity_des = "资料缺失"
    else:
        entity_des = list(entity_des[0].values())[0]

    return render(request, "detailPage.html", {'entityRelation': json.dumps(answer, ensure_ascii=False),
                                               'des00': json.dumps(entity_des, ensure_ascii=False),
                                               'name00': json.dumps(entity, ensure_ascii=False)})
