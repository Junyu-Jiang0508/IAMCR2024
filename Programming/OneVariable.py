import multiprocessing
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel
from gensim import corpora
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import warnings

# 忽略警告
warnings.filterwarnings('ignore')

def prepare_data(path):
    try:
        data_set = []
        with open(path, encoding='utf-8', errors='ignore') as file:
            for line in file:
                seg_list = line.split()
                data_set.append(seg_list)
        return data_set
    except Exception as e:
        print(f"Error reading data: {e}")
        return None

def create_dictionary(data_set):
    if data_set is None:
        return None
    dictionary = corpora.Dictionary(data_set)
    return dictionary

def create_corpus(dictionary, data_set):
    if dictionary is None:
        return None
    corpus = [dictionary.doc2bow(text) for text in data_set]
    return corpus

def calculate_perplexity(num_topics, corpus, dictionary):
    try:
        ldamodel = LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary, passes=30)
        perplexity = ldamodel.log_perplexity(corpus)
        print(f"Num topics: {num_topics}, Perplexity: {perplexity}")
        return perplexity
    except Exception as e:
        print(f"Error calculating perplexity: {e}")
        return None

def calculate_coherence(num_topics, corpus, dictionary, data_set):
    try:
        ldamodel = LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary, passes=30, random_state=1)
        coherence_model = CoherenceModel(model=ldamodel, texts=data_set, dictionary=dictionary, coherence='c_v')
        coherence = coherence_model.get_coherence()
        print(f"Num topics: {num_topics}, Coherence: {coherence}")
        return coherence
    except Exception as e:
        print(f"Error calculating coherence: {e}")
        return None

def plot_perplexity(perplexity_scores):
    if perplexity_scores:
        plt.plot(perplexity_scores)
        plt.xlabel('主题数目')
        plt.ylabel('困惑度大小')
        plt.title('主题-困惑度变化情况')
        plt.show()

def plot_coherence(coherence_scores):
    if coherence_scores:
        plt.plot(coherence_scores)
        plt.xlabel('主题数目')
        plt.ylabel('一致性大小')
        plt.title('主题-一致性变化情况')
        plt.show()

def grid_search_optimal_topics(data_set, dictionary, corpus, start_k=1, end_k=15, step=1):
    max_coherence = 0
    optimal_num_topics = start_k
    coherence_scores = []

    for num_topics in range(start_k, end_k + 1, step):
        coherence = calculate_coherence(num_topics, corpus, dictionary, data_set)
        if coherence is not None:
            coherence_scores.append(coherence)
            if coherence > max_coherence:
                max_coherence = coherence
                optimal_num_topics = num_topics

    return optimal_num_topics, coherence_scores

if __name__ == '__main__':
    # 路径需要根据实际情况修改
    PATH = "C:/Users/jain farstrider/Desktop/describe.csv"
    
    # 准备数据
    data_set = prepare_data(PATH)
    if data_set is None:
        exit(1)
    
    dictionary = create_dictionary(data_set)
    if dictionary is None:
        exit(1)
    
    corpus = create_corpus(dictionary, data_set)
    if corpus is None:
        exit(1)
    
    num_topics_range = range(1, 16)  # 根据需要调整主题数范围
    coherence_scores = []

    # 遍历主题数范围，计算每个主题数的一致性
    for num_topics in num_topics_range:
        coherence = calculate_coherence(num_topics, corpus, dictionary, data_set)
        if coherence is not None:
            coherence_scores.append(coherence)

    # 网格搜索最优主题数
    optimal_num_topics, _ = grid_search_optimal_topics(data_set, dictionary, corpus)

    # 绘制一致性折线图
    plot_coherence(coherence_scores)

    # 输出最优主题数
    print(f"最优主题数为: {optimal_num_topics}，在一致性最高的点")