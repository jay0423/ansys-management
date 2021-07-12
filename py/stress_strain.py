"""
./.csv/に格納されたansysで解析実行後の出力ファイルを整理する．
TIMEとFXの列から歪みと応力を算出し，エクセルファイルで書き出す．
"""


import pandas as pd
import numpy as np
import sys
import openpyxl


SPEED = 0.001 #試験速度[m/s]
LENGTH = 0.12 #試験片長さ[m]
CROSS_SECTIONAL_AREA = 48.60 #[mm2]
FILE_NAME = input("csvファイル名を入力：")
FILE_NAME = FILE_NAME.replace(".csv","")
DETAIL = input("ファイルの詳細：")


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

df["strain"] = df.loc[:,"TIME"] * SPEED / LENGTH # 歪みの追加
df["FX"] = df.loc[:,"FX"] * (-1) # 荷重の変換
df["stress"] = df.loc[:,"FX"] / CROSS_SECTIONAL_AREA # 応力の追加

# 最大応力の算出
max_stress = max(df["stress"])

#EXCELファイルへ書き出し
df.to_excel("../stress_strain_excel/stress_strain_{}.xlsx".format(FILE_NAME), index=False)


# エクセルファイルへ詳細を記載する．
book = openpyxl.load_workbook("../stress_strain_excel/stress_strain_{}.xlsx".format(FILE_NAME))
sheet = book['Sheet1']
# セルへ書き込む
sheet['F1'] = '詳細'
sheet['G1'] = DETAIL
sheet['F2'] = '最大応力'
sheet['G2'] = max_stress
# 保存する
book.save("../stress_strain_excel/stress_strain_{}.xlsx".format(FILE_NAME))


# 記録ファイルへの記載
path = "../stress_strain_excel/file_details.txt"
with open(path, mode="a") as f:
    f.write("\nstress_strain_{}.xlsx    {}".format(FILE_NAME, DETAIL))

