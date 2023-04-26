import os
import pandas as pd
import numpy as np
import re
import jieba


def clean_reduplicated_data(sen):
    count = {}
    for word in sen:
        count.setdefault(word, 0)
        count[word] = count[word] + 1
    idx = len(sen)
    for key, value in count.items():
        if value == idx:
            sen = ''
    return sen


def jieba_clean(sen):
    ls = []
    new_ls = []
    words = jieba.cut(sen, cut_all=False)
    for word in words:
        ls.append(word)
    for i in ls:
        if i not in new_ls:
            new_ls.append(i)
    sen = ''.join(new_ls)
    return sen


# idx = 0
path = './danmu'
file_list = os.listdir(path)
for filename in file_list:
    df = pd.read_csv('./danmu/' + filename, encoding='utf-8')  # len = 268174

    for i in range(len(df)):
        df.iloc[:, 0][i] = clean_reduplicated_data(df.iloc[:, 0][i])  # 去除叠句

        # 去数字符号
        df.iloc[:, 0][i] = re.sub(r"[^\u4e00-\u9fa5\u0030-\u0039]", '', df.iloc[:, 0][i])  # 保留中文数字
        df.iloc[:, 0][i] = re.sub(r"\d{4,}", '', df.iloc[:, 0][i])  # 去除数字数量>4
        if df.iloc[:, 0][i] == '':
            df.iloc[:, 0][i] = np.nan  # 将空字符串变成NaN一起清洗

    df = df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)  # 去除NaN

    new_df = pd.DataFrame(list(df.iloc[:, 0]))  # 253254

    for j in range(len(new_df)):
        new_df.iloc[:, 0][j] = jieba_clean(new_df.iloc[:, 0][j])
        # print(new_df.iloc[:, 0][j])

    new_df.to_csv('./cleaned_danmu/' + filename, header=0, index=None, encoding="utf_8_sig")
