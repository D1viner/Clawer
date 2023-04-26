# from bertopic import BERTopic
import bertopic
import os
import pandas as pd


#分词
path = './cleaned_danmu'
file_list = os.listdir(path)
ls = []

for filename in file_list:
    df = pd.read_csv('./cleaned_danmu/' + filename, encoding='utf-8')
    ls += list(df.iloc[:, 0])


topic_model = bertopic.BERTopic(language="multilingual")
topics, probs = topic_model.fit_transform(ls)
topic_model.get_topic_info()