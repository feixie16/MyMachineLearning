# encoding=utf-8
import pandas as pd
pd.set_option('display.width', 200)

# df = pd.read_csv("/Users/xiefei/Desktop/strategy_no", sep='\t')
df = pd.read_csv('/Users/xiefei/Desktop/dm_tmp_mzy_0605_05', sep='\t', dtype=str)


def get_strategy_dict():
    df["strategy_dict"] = df.apply(lambda x: [x["json_name"], x["strategy_no"]], axis=1)
    df["strategy_dict"] = df["strategy_dict"].apply(lambda x: tuple(x))
    strategy_tuple = tuple(df["strategy_dict"].tolist())
    strategy_dict = dict(strategy_tuple)
    print(strategy_dict)
    return strategy_dict



if __name__ == "__main__":
    strategy_dict = get_strategy_dict()

