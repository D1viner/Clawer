import os
import pandas as pd
from sklearn.datasets import data
import jieba
import sklearn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


def print_top_words(model, feature_names, n_top_words):
    tword = []
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        topic_w = " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        tword.append(topic_w)
        print(topic_w)
    return tword

#
#读取停用词
stop_ls = [k.strip() for k in open('stop_words.txt', encoding='utf8').readlines() if k.strip() != '']

# #分词
# path = './danmu'
# file_list = os.listdir(path)
# ls = []
#
# for filename in file_list:
#     df = pd.read_csv('./danmu/' + filename, encoding='utf-8')
#     ls += list(df.iloc[:, 0])
df = pd.read_csv('./cleaned_danmu/danmu_11-24-8.csv',encoding='utf-8')
ls = []
ls += list(df.iloc[:,0])
print(len(ls))
new_ls = []
for i in range(len(ls)):
    str = ''
    words = jieba.lcut(ls[i], cut_all=False)
    for word in words:
        str += word
        str += ' '
    new_ls.append(str)
print(new_ls)

#向量化
cntVector = CountVectorizer(stop_words=stop_ls)
cntTf = cntVector.fit_transform(new_ls)
print(cntTf)

#LDA构建
lda = LatentDirichletAllocation(n_components=5,max_iter=50,learning_method='batch',learning_offset=50., random_state=0)
lda.fit(cntTf)

#输出topic
n_top_words = 20
tf_feature_names = cntVector.get_feature_names_out()
topic_word =print_top_words(lda, tf_feature_names, n_top_words)

# for topic_idx, topic in enumerate(lda.components_):
#     print("Topic %d:" % (topic_idx + 1))
#     print(" ".join([cntVector.get_feature_names_out()[i]
#                     for i in topic.argsort()[:-10 - 1:-1]]))


plexs = []
n_max_topics = 16
for i in range(1,n_max_topics):
    print(i)
    lda = LatentDirichletAllocation(n_components=i, max_iter=50,
                                    learning_method='batch',
                                    learning_offset=50,random_state=0)
    lda.fit(cntTf)
    plexs.append(lda.perplexity(cntTf))
n_t = 15

x = list(range(1, n_t))
plt.plot(x, plexs[1:n_t])
plt.xlabel("number of topics")
plt.ylabel("perplexity")
plt.show()
#
# print(x)
