# import sys
# sys.path.append('..')
# from text2vec import SentenceModel, cos_sim, semantic_search
#
# embedder = SentenceModel()
#
# # Corpus with example sentences
# corpus = [
#     '花呗更改绑定银行卡',
#     '我什么时候开通了花呗',
#     'A man is eating food.',
#     'A man is eating a piece of bread.',
#     'The girl is carrying a baby.',
#     'A man is riding a horse.',
#     'A woman is playing violin.',
#     'Two men pushed carts through the woods.',
#     'A man is riding a white horse on an enclosed ground.',
#     'A monkey is playing drums.',
#     'A cheetah is running behind its prey.'
# ]
# corpus_embeddings = embedder.encode(corpus)
#
# # Query sentences:
# queries = [
#     '如何更换花呗绑定银行卡',
#     'A man is eating pasta.',
#     'Someone in a gorilla costume is playing a set of drums.',
#     'A cheetah chases prey on across a field.']
#
# for query in queries:
#     query_embedding = embedder.encode(query)
#     hits = semantic_search(query_embedding, corpus_embeddings, top_k=5)
#     print("\n\n======================\n\n")
#     print("Query:", query)
#     print("\nTop 5 most similar sentences in corpus:")
#     hits = hits[0]  # Get the hits for the first query
#     for hit in hits:
#         print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))