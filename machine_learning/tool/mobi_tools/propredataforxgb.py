#encoding=utf-8

import pandas as pd
import numpy as np
import logging
import sys
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s][%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout
)

"""
    处理数据的类，后面继承这个类，减少重复搬砖
"""


class ProprecessData(object):

    def __init__(self):
        self.col_dtype = ["object"]
        self.path = "./feature_list"

    def read_date(self):
        fea_list = self.read_list(self.path)
        df = pd.read_csv("/Users/xiefei/Desktop/mobi_data.csv", sep='\t') #, usecols=fea_list)
        logging.info(df.info())
        df_type = df.dtypes
        for i in df_type.items():
            if i[1] in self.col_dtype:
                print(df[i[0]].head())

    def read_list(self, path):
        fea_list = []
        with open(path, 'r') as f:
            for i in f.readlines():
                i = str(i).strip('\n').strip('\r')
                if str(i)[0] not in ("#", "\n"):
                    fea_list.append(i)
            return fea_list

    def strToInt(self, df):
        df_set = set(df.tolist())
        dic = {}
        j = 0
        for i in df_set:
            dic[i] = j
            j+=1
        df.replace(to_replace=dic, inplace=True)

if __name__ == "__main__":
    a = ProprecessData()
    a.read_date()