# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 21:27:05 2018

@author: HP
"""


import re  
import jieba  
import math 
import pandas as pd    
import pymysql


#np.set_printoptions(threshold = 1e6)#设置打印数量的阈值
pd.set_option('max_colwidth',2000)


def jieba_function(sent):
    sent1 = jieba.cut(sent)
    s = []
    for each in sent1:
        s.append(each)
    return ' '.join(str(i) for i in s)


def count_cos_similarity(vec_1, vec_2):
    if len(vec_1) != len(vec_2):
        return 0

    s = sum(vec_1[i] * vec_2[i] for i in range(len(vec_2)))
    den1 = math.sqrt(sum([pow(number, 2) for number in vec_1]))
    den2 = math.sqrt(sum([pow(number, 2) for number in vec_2]))
    return s / (den1 * den2)


#计算文本向量，传入文本,接受的是字符串
def tf(sent1, sent2):
    from sklearn.feature_extraction.text import CountVectorizer

    sent1 = jieba_function(sent1)
    sent2 = jieba_function(sent2)
    count_vec = CountVectorizer()

    sentences = [sent1, sent2]

    #转换成维度相同的
    vec_1 = count_vec.fit_transform(sentences).toarray()[0]
    vec_2 = count_vec.fit_transform(sentences).toarray()[1]



def tfidf(sent1, sent2):
    from sklearn.feature_extraction.text import TfidfVectorizer

    sent1 = jieba_function(sent1)
    sent2 = jieba_function(sent2)

    tfidf_vec = TfidfVectorizer()

    sentences = [sent1, sent2]
    vec_1 = tfidf_vec.fit_transform(sentences).toarray()[0]
    vec_2 = tfidf_vec.fit_transform(sentences).toarray()[1]
    return count_cos_similarity(vec_1, vec_2)



dbconn=pymysql.connect(
  # host="192.168.1.100",
  host="127.0.0.1",
  database="sub-health",
  user="root",
  # password="Zehuo@2019",
  password="123456",
  port=3306,
  charset='utf8'
 )




sqlcmd="select sy.id ID,'定义' dis_def, group_concat( cl.desc SEPARATOR ',' ) comp_lang, sy.symptom tcm_dis from core co left join comp_lang cl  on cl.core_id=co.id left join symptom sy on sy.id=co.symptom_id GROUP BY sy.id"

tex_dat=pd.read_sql(sqlcmd,dbconn)  #利用pandas 模块导入mysql数据


row_num=tex_dat.shape[0]
col_num=tex_dat.shape[1]
def simcal(sent1):
    NewComplain=sent1
    cos_vec=[]
    for i in range(row_num):
        adf=tex_dat.iloc[i,2].encode("utf-8")
        cal=tfidf(NewComplain, adf)
        cal_id=[cal,i]
        cos_vec.append(cal_id)
    
    cos_dat=pd.DataFrame(cos_vec)
    maxsim=cos_dat[(cos_dat[0]==max(cos_dat[0]))]    #计算的最大相似度
    sim_qst=tex_dat.iloc[maxsim[1],1]
    link_vrb=tex_dat.iloc[maxsim[1],2]
    recom_ans=tex_dat.iloc[maxsim[1],0]
    ful_ans=recom_ans #+sim_qst+link_vrb
    # print("答："+ful_ans.to_string(index=False))
    # print("注："+sim_qst.to_string(index=False))
    return ful_ans.to_string(index=False)

