import multiprocessing
from gensim.models.ldamodel import LdaModel
from gensim import corpora
import matplotlib.pyplot as plt
import numpy as np
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

def calculate_model_scores(num_topics, learning_decay, corpus, dictionary):
    try:
        ldamodel = LdaModel(
            corpus=corpus,
            num_topics=num_topics,
            id2word=dictionary,
            passes=30,
            alpha='symmetric',
            eta='symmetric',
            decay=learning_decay,
            offset=1.0,
            random_state=1
        )
        log_likelihood = ldamodel.log_perplexity(corpus)
        perplexity = np.exp2(-log_likelihood)
        print(f"Num topics: {num_topics}, Learning Decay: {learning_decay}, Log likelihood: {log_likelihood}, Perplexity: {perplexity}")
        return num_topics, learning_decay, log_likelihood, perplexity
    except Exception as e:
        print(f"Error calculating model scores: {e}")
        return None

def grid_search_optimal_model(data_set, dictionary, corpus, num_topics_range, learning_decay_values):
    results = []
    for num_topics in num_topics_range:
        for learning_decay in learning_decay_values:
            score = calculate_model_scores(num_topics, learning_decay, corpus, dictionary)
            if score:
                results.append(score)
    return results

def plot_model_scores(results):
    if not results:
        print("No results to plot.")
        return

    learning_decay_scores = {}
    for num_topics, learning_decay, log_likelihood, perplexity in results:
        if learning_decay not in learning_decay_scores:
            learning_decay_scores[learning_decay] = ([], [], [])

        learning_decay_scores[learning_decay][0].append(num_topics)
        learning_decay_scores[learning_decay][1].append(log_likelihood)
        learning_decay_scores[learning_decay][2].append(perplexity)

    plt.figure(figsize=(12, 6))
    for learning_decay, (num_topics_list, log_likelihood_list, perplexity_list) in learning_decay_scores.items():
        plt.plot(num_topics_list, log_likelihood_list, marker='o', label=f'Learning Decay {learning_decay}')

    plt.xlabel('Number of Topics')
    plt.ylabel('Log Likelihood Score')
    plt.title('Choosing Optimal LDA Model')
    plt.legend()
    plt.grid(True)
    plt.show()

def find_optimal_model(results):
    if not results:
        print("No results to find optimal model.")
        return None

    best_model = min(results, key=lambda x: (x[2], x[3]))  # 根据 log likelihood 和 perplexity 找最优模型
    return best_model

if __name__ == '__main__':
    # 路径需要根据实际情况修改
    PATH = "original/公关回应-分词.csv"
    
    # 准备数据
    data_set = prepare_data(PATH)
    if data_set is None or len(data_set) == 0:
        print("Data preparation failed or no data found.")
        exit(1)
    
    dictionary = create_dictionary(data_set)
    if dictionary is None:
        print("Dictionary creation failed.")
        exit(1)
    
    corpus = create_corpus(dictionary, data_set)
    if corpus is None or len(corpus) == 0:
        print("Corpus creation failed.")
        exit(1)
    
    # 定义主题数量范围和学习衰减参数
    num_topics_range = range(2, 11)  # 从2到10个主题
    learning_decay_values = [ 0.8, 0.7,0.9]

    # 网格搜索最优模型
    results = grid_search_optimal_model(data_set, dictionary, corpus, num_topics_range, learning_decay_values)
    
    if not results:
        print("No results from grid search.")
        exit(1)
    
    # 找到最优模型
    best_model = find_optimal_model(results)
    if best_model:
        num_topics, learning_decay, log_likelihood, perplexity = best_model
        print(f"Best model: Num topics: {num_topics}, Learning Decay: {learning_decay}, Log likelihood: {log_likelihood}, Perplexity: {perplexity}")
    
    # 绘制模型评分
    plot_model_scores(results)
