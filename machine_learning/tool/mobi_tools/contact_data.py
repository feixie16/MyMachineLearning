import numpy as np
import pandas as pd
import os
import time
import datetime
pd.set_option('display.max_rows', 2000)


def read_file():
    file_list = os.listdir("./")
    df_feature_all = pd.DataFrame()
    df_score_all = pd.DataFrame()
    for file_name in file_list:
        try:
            if int(file_name) >= 20180523:
                file_list_minute = os.listdir("./%s" % file_name)
                for minute_list in file_list_minute:
                    print("%s day %s file" % (file_name, minute_list))
                    try:
                        df_minute = pd.read_csv("./%s/%s/ascore_features_input" % (file_name, minute_list), sep='\t')
                        df_score = pd.read_csv("./%s/%s/ascore_result" % (file_name, minute_list), sep='\t')
                    except:
                        continue
                    df_feature_all = pd.concat([df_feature_all, df_minute], ignore_index=True)
                    df_score_all = pd.concat([df_score_all, df_score], ignore_index=True)

        except:
            print("there is no data in this time slot")
    df_feature_all.to_csv("input_feature_data", sep="\t", index=None)
    df_score_all.to_csv("ascore_data", sep="\t", index=None)
    print(df_feature_all.shape, df_score_all.shape)





def calculate(df, thr):
    x_shape = df[df["score_x"] >= thr].shape[0]
    y_shape = df[df["score_y"] >= thr].shape[0]
    x_trans = df[(df["score_x"] < thr) & (df["score_y"] >= thr)].shape[0]
    print x_trans
    y_trans = df[(~(df["score_x"] < thr)) & (~(df["score_y"] >= thr))].shape[0]
    row = df.shape[0]
    x_rate = np.float(x_shape) / row
    y_rate = np.float(y_shape) / row
    print(x_shape, '\n', y_shape, '\n', x_rate, '\n', y_rate, '\n', x_trans, '\n', y_trans)

def merge_score(score):
    score_1 = pd.read_csv("/mnt/risk_model/risk/lr_mobi/data/xiefei/ascore_data", sep='\t')
    score_2 = pd.read_csv("/mnt/risk_model/risk/lr_mobi/output/lr_predict_res_plus", sep='\t')
    score_2.rename(columns={"user_account_id": "account_id"}, inplace=True)
    score_merge = pd.merge(score_1, score_2, how="left", on=["account_id", "imei"])
    print score_merge.head()
    calculate(score_merge, score)


if __name__ == "__main__":
    for i in range(600, 620, 5):
        merge_score(i)