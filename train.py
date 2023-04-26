# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.decomposition import LatentDirichletAllocation
#
# # list of Chinese documents
# documents = [
#     "这是第一个文档。",
#     "这是第二个文档。",
#     "这是第三个文档。",
#     "这是第一个文档吗？",
# ]
#
# # convert the documents into a bag-of-words representation
# vectorizer = CountVectorizer(min_df=1)
# X = vectorizer.fit_transform(documents)
#
# lda = LatentDirichletAllocation(n_components=2)
# lda.fit(X)
# stop_dic = open('stop_words.txt', 'rb')
# stop_content = stop_dic.read()
# stop_ls = stop_content.splitlines()
# for i in range (len(stop_ls)):
#     stop_ls[i] = stop_ls[i].strip('b')
# stop_dic.close()
# # print(stop_ls)
# stopword_list = [k.strip() for k in open('stop_words.txt', encoding='utf8').readlines() if k.strip() != '']
# print(stopword_list)
# import os
#
#
# path = './cleaned_danmu'
# file_list = os.listdir(path)
# print(file_list)

import os
import pandas as pd
from sklearn.datasets import data
import jieba
import sklearn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import jieba.posseg as psg
import os
import re

stop_ls = [k.strip() for k in open('stop_words.txt', encoding='utf8').readlines() if k.strip() != '']

path = './cleaned_danmu'
file_list = os.listdir(path)
ls = []

for filename in file_list:
    df = pd.read_csv('./cleaned_danmu/' + filename, encoding='utf-8')
    ls += list(df.iloc[:, 0])

# new_ls = []
# for i in range(len(ls)):
#     str = ''
#     words = jieba.lcut(ls[i], cut_all=False)
#     for word in words:
#         str += word
#         str += ' '
#     new_ls.append(str)
# print(len(new_ls))
# filename = 'write_data.txt'
# with open(filename,'w',encoding='utf-8') as f: # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
#     for i in range(len(new_ls)):
#         f.write(new_ls[i]+'\n')

f = open('write_danmu.txt', 'w', encoding='utf-8')
for t in ls:
    t = re.sub('\n', '', t)
    t_seg = psg.cut(t)
    t_seg_f = []
    # flag_list = ['n','nz','vn','v']
    for word_flag in t_seg:
        if len(word_flag.word) > 1 and word_flag.word not in stop_ls:
            t_seg_f.append(word_flag.word)
    if len(t_seg_f) > 0:
        t_seg_f = ' '.join(t_seg_f)
        f.write(t_seg_f + '\n')
f.close()
