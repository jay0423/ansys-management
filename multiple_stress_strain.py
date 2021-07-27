"""
../csv/に格納されたansysで解析実行後の出力csvファイルから，エクセルファイルにまとめる．
TIMEとFXの列から歪みと応力を算出し，エクセルファイルで書き出す．

1. ../excel/base.xlsxをその場でコピー＆ペースト
2. base copy.xlsx ファイルを任意のファイル名に変更する．（例：lap=10.xlsx）
3. ファイル（lap=10.xlsx）を開き，csvファイル名や試験速度，詳細などを入力し保存する．
4. multiple_stress_strain.pyを実行し，誘導に従って入力する．
5. 同ファイルへ引張強さやヤング率，グラフなどが出力される．
"""


import pandas as pd
import numpy as np
import sys
import openpyxl as px

# 入力値
EXCEL_FILE_NAME = input("指定excelファイル名を入力：")
EXCEL_FILE_NAME = EXCEL_FILE_NAME.replace(".xlsx","")
try:
    excel_df = pd.read_excel("{}.xlsx".format(EXCEL_FILE_NAME))
except:
    print("そのファイルは存在しません．")
    sys.exit()
EXCEL_DETAIL = input("ファイルの詳細：")

FILE_NAME_LIST = list(excel_df["file_name"]) #CSVファイル
N = len(FILE_NAME_LIST)
NEW_LIST = list(excel_df["new"].fillna(0)) # 新たに追加するか．0:新たに追加, 1:今回は追加しない
SPEED_LIST = list(excel_df["speed[mm/s]"].fillna(1)/1000) # 引張速度
LENGTH_LIST = list(excel_df["length[mm]"].fillna(120)/1000) # 試験片長さ（歪み算出用）
CROSS_SECTIONAL_AREA_LIST = list(excel_df["cross_section_area[mm2]"].fillna(50)) #面積（応力算出用）
DETAIL_LIST = list(excel_df["detail"].fillna(""))


tensile_strength_list = []
young_modulus_list = []


for (i, FILE_NAME, NEW, SPEED, LENGTH, CROSS_SECTIONAL_AREA, DETAIL) in zip(range(N), FILE_NAME_LIST, NEW_LIST, SPEED_LIST, LENGTH_LIST, CROSS_SECTIONAL_AREA_LIST, DETAIL_LIST):

    # 新たに追加するか判定
    if NEW == 1:
        print("Already added: {}.csv".format(FILE_NAME))
        continue


    # csvファイルの取得
    try:
        FILE_NAME = FILE_NAME.replace(".csv","")
        df = pd.read_csv("../csv/{}.csv".format(FILE_NAME))
    except:
        print("Failed: {}.csv".format(FILE_NAME))
        continue


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

    # ヤング率の算出
    x_ = df["strain"][:int((MAX_ROW-1)*0.1)]
    y_ = df["stress"][:int((MAX_ROW-1)*0.1)]
    a, b = np.polyfit(x_,y_,1)
    # print("ヤング率： {}".format(a))
    young_modulus_list.append(a)

    # 最大応力の算出
    max_stress = max(df["stress"])
    tensile_strength_list.append(max_stress)


    # エクセルファイルへ詳細を記載する．
    with pd.ExcelWriter("{}.xlsx".format(EXCEL_FILE_NAME), engine="openpyxl", mode='a') as writer:
        df.to_excel(writer, sheet_name=FILE_NAME, index=False)
    book = px.load_workbook("../excel/{}.xlsx".format(EXCEL_FILE_NAME))
    sheet = book[FILE_NAME]
    # セルへ書き込む
    sheet['F1'] = '詳細'
    sheet['G1'] = DETAIL
    sheet['F2'] = '最大応力'
    sheet['G2'] = max_stress
    sheet['F3'] = 'ヤング率'
    sheet['G3'] = a


    # 散布図の追加
    # 散布図をグラフ変数:chartとして定義
    chart=px.chart.ScatterChart()

    # y,xデータの範囲を選択
    x = px.chart.Reference(book[FILE_NAME] ,min_col=3 ,max_col=3 ,min_row=2 ,max_row=MAX_ROW+1)
    y = px.chart.Reference(book[FILE_NAME] ,min_col=4 ,max_col=4 ,min_row=2 ,max_row=MAX_ROW+1)

    #系列変数seriesをy,xを指定して定義する
    series = px.chart.Series(y, x)
    #散布図として定義したchartへデータを指定したseries変数を渡す
    chart.series.append(series)
    chart.title = FILE_NAME
    chart.x_axis.title = 'Strain [-]'
    chart.y_axis.title = 'Stress [MPa]'
    #A6セルにグラフを表示
    book[FILE_NAME].add_chart(chart,"F5")


    # ヤング率用散布図の追加
    # 散布図をグラフ変数:chartとして定義
    chart2=px.chart.ScatterChart()

    # y,xデータの範囲を選択
    x = px.chart.Reference(book[FILE_NAME] ,min_col=3 ,max_col=3 ,min_row=2 ,max_row=int((MAX_ROW-1)*0.1))
    y = px.chart.Reference(book[FILE_NAME] ,min_col=4 ,max_col=4 ,min_row=2 ,max_row=int((MAX_ROW-1)*0.1))

    #系列変数seriesをy,xを指定して定義する
    series = px.chart.Series(y, x)
    #散布図として定義したchartへデータを指定したseries変数を渡す
    chart2.series.append(series)
    chart2.title = "10%"
    chart2.x_axis.title = 'Strain [-]'
    chart2.y_axis.title = 'Stress [MPa]'
    #A6セルにグラフを表示
    book[FILE_NAME].add_chart(chart2,"F17")

    print("Success: {}.csv".format(FILE_NAME))
    # 保存する
    book.save("../excel/{}.xlsx".format(EXCEL_FILE_NAME))


# まとめの追加 現状初回のみに対応している．
df = pd.DataFrame()
df["tensile_strength"] = tensile_strength_list
df["young's_modulus"] = young_modulus_list
# エクセルファイルへ詳細を記載する．
with pd.ExcelWriter("{}.xlsx".format(EXCEL_FILE_NAME), engine="openpyxl", mode='a') as writer:
    df.to_excel(writer, sheet_name="まとめ", index=False)



# # 記録テキストファイルへの記載
# path = "../excel/file_details.txt"
# with open(path, mode="a") as f:
#     f.write("\nstress_strain_{}.xlsx    {}".format(EXCEL_FILE_NAME, EXCEL_DETAIL))

