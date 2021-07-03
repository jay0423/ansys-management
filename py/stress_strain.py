"""
./.csv/に格納されたansysで解析実行後の出力ファイルを整理する．
TIMEとFXの列から歪みと応力を算出し，エクセルファイルで書き出す．
"""


import pandas as pd
import numpy as np
import sys

SPEED = 0.001 #[m/s]
LENGTH = 0.12 #[m]
CROSS_SECTIONAL_AREA = 48.60 #[mm2]
FILE_NAME = input("csvファイル名を入力：")
FILE_NAME = FILE_NAME.replace(".csv","")

# dataframeの整理
try:
    df = pd.read_csv("../csv/{}.csv".format(FILE_NAME))
except:
    print("そのファイルは存在しません．")
    sys.exit()

df = df.iloc[:,0].apply(lambda x: pd.Series(x.split()))
df = df.iloc[2:,:2]
df.columns = ["TIME", "FX"]

# map用の関数を定義
def clean(x):
    try:
        return float(x)
    except:
        return None
# 数値の文字型を小数型に変換し，文字をnanに変換し削除する．
df.loc[:,"TIME"] = df.loc[:,"TIME"].map(clean)
df.loc[:,"FX"] = df.loc[:,"FX"].map(clean)
df = df.dropna(how="any")

# 歪みの追加
df["strain"] = df.loc[:,"TIME"] * SPEED / LENGTH
# 荷重の変換
df["FX"] = df.loc[:,"FX"] * (-1)
# 応力の追加
df["stress"] = df.loc[:,"FX"] / CROSS_SECTIONAL_AREA


#EXCELファイルへ書き出し
df.to_excel("../stress_strain_excel/stress_strain_{}.xlsx".format(FILE_NAME), index=False)

print(df)
