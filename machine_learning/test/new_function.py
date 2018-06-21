# encoding=utf-8

import pandas as pd

pd.set_option('display.max_rows', 2000)
from IPython.display import display, HTML

df = pd.read_csv('/Users/xiefei/Desktop/mobi_data_2018-06-20.csv', sep='\t')
df_1 = pd.read_csv("/Users/xiefei/Desktop/strategy_no", sep='\t')
df = df[(df['is_pass'] == 'pass') & (df['apply_tm'] >= '2018-05-18') & (df['deadline'] <= '2018-06-19')
        & (df['deadline'] >= '2018-06-14')]


# df = df[(df['is_pass'] == 'pass') & (df['apply_tm'] >= '2018-05-18') & (df['deadline'] <= '2018-06-13')]


def filter_origin_data():
    pass


def get_strategy_dict():
    df_1["strategy_dict"] = df_1.apply(lambda x: (x["json_name"], x["strategy_no"]), axis=1)
    strategy_tuple = tuple(df_1["strategy_dict"].tolist())
    strategy_dict = dict(strategy_tuple)
    return strategy_dict


def rename_columns():
    strategy_dict = get_strategy_dict()
    df.rename(mapper={"ascore": "score", "ascore_v2": "Z003"}, axis="columns", inplace=True)
    df.rename(mapper=strategy_dict, axis='columns', inplace=True)


def trans_type():
    col = df.columns
    global use_col
    use_col = []
    for i in col:
        if str(i)[0] == "D" or str(i)[0] == "Z" or str(i) == "random_value":
            use_col.append(i)
            df[i] = pd.to_numeric(df[i], errors='coerce')
    return use_col


def standardize_feature_value():
    def bin_value(val):
        if str(val)[0] != "0":
            return int(val / 10) * 10
        else:
            return int((val * 100) / 10) * 10

    def bin_value_d015(x):
        if x > 5 and x <= 200:
            return int(x / 5) * 5
        elif x > 200:
            return "200+"
        else:
            return x

    def bin_value_d036(x):
        if x > 300:
            return "300+"
        else:
            return int(x / 50) * 50

    def bin_value_d012(x):
        if x > 1000:
            return "1000+"
        else:
            return int(x / 100) * 1000

    for col in use_col:
        if col == "D015":
            df[col] = df[col].apply(lambda x: str(x) if str(x) == "nan" or len(str(x)) <= 0 else bin_value_d015(x))
        elif col in ("D012"):
            df[col] = df[col].apply(lambda x: str(x) if str(x) == "nan" or len(str(x)) <= 0 else bin_value_d012(x))
        elif col in ("D036"):
            df[col] = df[col].apply(lambda x: str(x) if str(x) == "nan" or len(str(x)) <= 0 else bin_value_d036(x))
        elif col in ("D035"):
            df[col] = df[col].apply(lambda x: str(x) if str(x) == "nan" or len(str(x)) <= 0 else int(x / 1) * 1)
        elif col in ("D036"):
            df[col] = df[col].apply(lambda x: str(x) if str(x) == "nan" or len(str(x)) <= 0 else bin_value_d036(x))
        elif len(df[col].unique()) > 10:
            df[col] = df[col].apply(lambda x: str(x) if str(x) == "nan" or len(str(x)) <= 0 else bin_value(x))
        else:
            df[col] = df[col].apply(lambda x: str(x) if str(x) == "nan" or len(str(x)) <= 0 else x)


def add_columns():
    df["is_overdue"] = df['overdue_days'].apply(lambda x: 1 if int(x) > 0 else 0)


def strategy_overdue_rate(col):
    df_tmp = df[df['is_loan_type'] == "首贷"]
    a = df_tmp.groupby([col])['is_overdue'].sum().reset_index()
    b = df_tmp.groupby([col])['is_overdue'].count().reset_index()
    b.rename(mapper={"is_overdue": "total"}, inplace=True, axis='columns')
    a['total'] = b['total']
    a["overdue_rate"] = a['is_overdue'] / a['total']
    display(a)


def run():
    filter_origin_data()
    get_strategy_dict()
    rename_columns()
    trans_type()
    standardize_feature_value()
    add_columns()
    for k in use_col:
        strategy_overdue_rate(k)


if __name__ == '__main__':
    run()