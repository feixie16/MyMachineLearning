# encoding=utf-8

import pandas as pd


df = pd.read_csv('/Users/xiefei/Desktop/mobi_data_2018-06-12.csv', sep='\t')
df_1 = pd.read_csv("/Users/xiefei/Desktop/strategy_no", sep='\t')


def get_strategy_dict():
    df_1["strategy_dict"] = df_1.apply(lambda x: (x["json_name"], x["strategy_no"]), axis=1)
    strategy_tuple = tuple(df_1["strategy_dict"].tolist())
    strategy_dict = dict(strategy_tuple)
    print(strategy_dict)
    return strategy_dict


def rename_columns():
    strategy_dict = get_strategy_dict()
    df.rename(mapper={"ascore": "score"}, axis="columns", inplace=True)
    df.rename(mapper=strategy_dict, axis='columns', inplace=True)
    print df.head()


if __name__ == '__main__':
    rename_columns()