from gensim.models import LdaModel
from gensim.corpora import Dictionary
from gensim import corpora
import pyLDAvis.gensim
import pandas as pd

# 准备数据
PATH = "original/形象修复-分词.csv"

# 读取数据并进行分词
file_object2 = open(PATH, encoding='utf-8', errors='ignore').read().split('\n')
data_set = [line.split() for line in file_object2 if line.strip()]  # 使用列表推导式进行分词并移除空行

# 构建词典和语料库
dictionary = corpora.Dictionary(data_set)
corpus = [dictionary.doc2bow(text) for text in data_set]

# 训练LDA模型
lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=7, passes=30, random_state=1)

# 输出主题
topic_list = lda.print_topics()
print(topic_list)

# 解析文档的主题分布并输出主题编号
for doc_topics in lda.get_document_topics(corpus):
    # doc_topics是一个列表，每个元素是一个元组 (topic_id, topic_probability)
    # 我们将按照概率最高的主题来确定该文档的主题
    max_prob_topic = max(doc_topics, key=lambda x: x[1])
    print("Document belongs to topic:", max_prob_topic[0])

# 保存可视化结果到HTML文件
data = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
pyLDAvis.save_html(data, 'outcome/形象修复t7.html')

