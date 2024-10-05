import jieba
import re
import csv

# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('hit_stopwords.txt', encoding='UTF-8').readlines()]
    return stopwords

def processing(text):
    text = re.sub("\n", "", text)
    return text

# 对句子进行中文分词
def seg_depart(sentence):
    sentence_depart = jieba.cut(sentence.strip())
    print(sentence_depart)
    stopwords = stopwordslist()  # 创建一个停用词列表
    outstr = ''  # 输出结果为outstr
    for word in sentence_depart:  # 去停用词
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

# 给出文档路径
filename = "original/公关回应.csv" # 原文档路径
outputs = open("original/公关回应post.csv", 'w', encoding='UTF-8')  # 输出文档路径
with open(filename, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"', doublequote=False)
    for line in reader:
        print(line[0])  # 微博在文档的第一列
        line = processing(line[0])
        line_seg = seg_depart(line)
        outputs.write(line_seg + '\n')
outputs.close()
print("分词成功！！！")
