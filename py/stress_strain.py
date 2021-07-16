"""
./.csv/に格納されたansysで解析実行後の出力ファイルを整理する．
TIMEとFXの列から歪みと応力を算出し，エクセルファイルで書き出す．
"""


import pandas as pd
import sys
import openpyxl as px


SPEED = 0.001 #試験速度[m/s]
LENGTH = 0.12 #試験片長さ[m]
CROSS_SECTIONAL_AREA = 48.60 #[mm2]
FILE_NAME = input("csvファイル名を入力：")
FILE_NAME = FILE_NAME.replace(".csv","")
try:
    df = pd.read_csv("../csv/{}.csv".format(FILE_NAME))
except:
    print("そのファイルは存在しません．")
    sys.exit()
DETAIL = input("ファイルの詳細：")


# dataframeの整理
df = df.iloc[:,0].apply(lambda x: pd.Series(x.split()))
df = df.iloc[2:,:2]
df.columns = ["TIME", "FX"]

# 数値の文字型を小数型に変換し，文字をnanに変換し削除する．
def clean(x): # map用の関数を定義
    try:
        return float(x)
    except:
        return None
df.loc[:,"TIME"] = df.loc[:,"TIME"].map(clean)
df.loc[:,"FX"] = df.loc[:,"FX"].map(clean)
df = df.dropna(how="any")

df["strain"] = df.loc[:,"TIME"] * SPEED / LENGTH # 歪みの追加
df["FX"] = df.loc[:,"FX"] * (-1) # 荷重の変換
df["stress"] = df.loc[:,"FX"] / CROSS_SECTIONAL_AREA # 応力の追加
MAX_ROW = len(df)

# 最大応力の算出
max_stress = max(df["stress"])

#EXCELファイルへ書き出し
df.to_excel("../stress_strain_excel/stress_strain_{}.xlsx".format(FILE_NAME), index=False)


# エクセルファイルへ詳細を記載する．
book = px.load_workbook("../stress_strain_excel/stress_strain_{}.xlsx".format(FILE_NAME))
sheet = book['Sheet1']
# セルへ書き込む
sheet['F1'] = '詳細'
sheet['G1'] = DETAIL
sheet['F2'] = '最大応力'
sheet['G2'] = max_stress


# 散布図の追加
# 散布図をグラフ変数:chartとして定義
chart=px.chart.ScatterChart()

# y,xデータの範囲を選択
x = px.chart.Reference(book["Sheet1"] ,min_col=3 ,max_col=3 ,min_row=2 ,max_row=MAX_ROW+1)
y = px.chart.Reference(book["Sheet1"] ,min_col=4 ,max_col=4 ,min_row=2 ,max_row=MAX_ROW+1)

#系列変数seriesをy,xを指定して定義する
series = px.chart.Series(y, x)
#散布図として定義したchartへデータを指定したseries変数を渡す
chart.series.append(series)
#A6セルにグラフを表示
book["Sheet1"].add_chart(chart,"F5")

# 保存する
book.save("../stress_strain_excel/stress_strain_{}.xlsx".format(FILE_NAME))



# 記録ファイルへの記載
path = "../stress_strain_excel/file_details.txt"
with open(path, mode="a") as f:
    f.write("\nstress_strain_{}.xlsx    {}".format(FILE_NAME, DETAIL))

