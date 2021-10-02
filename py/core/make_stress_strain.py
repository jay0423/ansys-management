"""
mac osバージョン
path.xlsxで指定されているpath以降にあるcsvファイルをまとめる．
TIMEとFXの列から歪みと応力を算出し，エクセルファイルで書き出す．

1. ./path.xlsxにpathなどの情報を追加する．
2. path_multiple_stress_strain.pyを実行し，誘導に従って入力する．
3. path先へ引張強さやヤング率，グラフなどが出力される．

"""


import pandas as pd
import numpy as np
import os
import sys
import openpyxl as px
import pprint

from .get_path import GetPath
from ..settings import settings





class MakeStressStrain:

    SLASH = os.path.normcase("a/")[-1]
    PATH_FILE_NAME = settings.PATH_FILE_NAME


    FILE_NAME_LIST = None
    EXCEL_FILE_NAME = None
    POSITIVE_NEGATIVE = None
    SPEED = None
    LENGTH = None
    CROSS_SECTIONAL_AREA = None



    def __init__(self, first_path=""):
        self.first_path = first_path # MakeStressStrainFromAnsysFileからデータを収集する用
    

    def _make_df(self):
        # path.xlsxから情報を取得
        try:
            path_df = pd.read_excel(self.PATH_FILE_NAME)
            path_df = path_df.fillna("")
            path_df = path_df[path_df["finished"] == ""]
            path_df.reset_index(inplace=True, drop=True)
            path_s = path_df.iloc[0,:] # バグ発生用
        except:
            print("{}で指定されていません．".format(self.PATH_FILE_NAME))
            sys.exit()
        if len(path_df) > 1: # 複数入力されている時
            while True:
                print("\n＜＜　pathの選択肢が複数あります．　＞＞")
                for i, p in enumerate(path_df["output_file_name"]):
                    print("{}： {}".format(i, p))
                try:
                    path_num = int(input("\n数字で選択してください："))
                    break
                except:
                    print("\n不明な入力\n")
                    continue
            try:
                path_df = path_df[path_df.index == path_num]
            except:
                print("初めからやり直してください．\n")
                sys.exit()
        return path_df


    def _make_path_s(self, path_df):
        path_s = path_df.iloc[0,:]
        return path_s


    def _get_inputs(self, path_s):
        # 入力値
        FIRST_PATH = path_s["path"]
        KEY_WORD_LIST = path_s["key_word"].replace(" ", "").split(",") # csvファイルのキーワード
        REMOVE_WORD_LIST = path_s["remove_word"].replace(" ", "").split(",") # 除外のキーワード
        if FIRST_PATH[-1] == self.SLASH:
            FIRST_PATH = FIRST_PATH[:-1]
        FILE_NAME_LIST = GetPath(first_path=FIRST_PATH, slash=self.SLASH).get_list(kind="csv") #CSVファイルリスト
        FILE_NAME_LIST = [FILE_NAME for FILE_NAME in FILE_NAME_LIST for KEY_WORD in KEY_WORD_LIST if KEY_WORD in FILE_NAME] # KEY_WORDが含まれるファイル名だけ抽出
        if REMOVE_WORD_LIST != ['']:
            FILE_NAME_LIST = [FILE_NAME for FILE_NAME in FILE_NAME_LIST for REMOVE_WORD in REMOVE_WORD_LIST if REMOVE_WORD not in FILE_NAME] # KEY_WORDが含まれるファイル名だけ抽出
        self.FILE_NAME_LIST = sorted(FILE_NAME_LIST) # 並び替え．まだ不完全
        EXCEL_FILE_NAME = path_s["output_file_name"] # 出力ファイル名
        EXCEL_FILE_NAME = EXCEL_FILE_NAME.replace(".xlsx","")
        self.EXCEL_FILE_NAME = "{}{}{}.xlsx".format(FIRST_PATH, self.SLASH, EXCEL_FILE_NAME) # 出力先のpathをくっつける
        POSITIVE_NEGATIVE = int(path_s["plus"]) # プラスマイナス
        if POSITIVE_NEGATIVE == 0:
            self.POSITIVE_NEGATIVE = 1
        else:
            self.POSITIVE_NEGATIVE = -1
        self.SPEED = float(path_s["speed[mm/s]"])/1000 # 引張速度
        self.LENGTH = float(path_s["length[mm]"]/1000) # 試験片長さ（歪み算出用）
        self.CROSS_SECTIONAL_AREA = path_s["cross_section_area[mm2]"] # 断面積（応力算出用）


    def _make_excel_file(self, path_df):
        # 出力エクセルファイルの作成
        path_df.to_excel(self.EXCEL_FILE_NAME, index=False)


    def _csv_to_df(self, file_name):
        # csvファイルの取得
        try:
            df = pd.read_csv(file_name, usecols=[0])
        except:
            return None

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
        return df


    def _get_data_from_ansys(self, file_name):
        return


    def write_excel(self):

        sheet_name_list = []
        tensile_strength_list = []
        young_modulus_list = []


        for FILE_NAME in self.FILE_NAME_LIST:

            self._get_data_from_ansys(FILE_NAME) # ansysファイルからデータを収集する．

            df = self._csv_to_df(FILE_NAME)
            if df is None:
                print("Failed: {}".format(FILE_NAME))
                continue
            df["strain"] = df.loc[:,"TIME"] * self.SPEED / self.LENGTH # 歪みの追加
            df["FX"] = df.loc[:,"FX"] * self.POSITIVE_NEGATIVE # 荷重の変換
            df["stress"] = df.loc[:,"FX"] / self.CROSS_SECTIONAL_AREA # 応力の追加

            MAX_ROW = len(df)
            
            # ヤング率の算出
            x_ = df["strain"][:int((MAX_ROW-1)*0.1)]
            y_ = df["stress"][:int((MAX_ROW-1)*0.1)]
            a, b = np.polyfit(x_,y_,1)
            young_modulus_list.append(a)

            # 最大応力の算出
            max_stress = max(df["stress"])
            tensile_strength_list.append(max_stress)


            sheet_name = FILE_NAME.split(self.SLASH)[-1].replace(".csv", "")
            sheet_name_list.append(sheet_name)
            # エクセルファイルへ詳細を記載する．
            with pd.ExcelWriter(self.EXCEL_FILE_NAME, engine="openpyxl", mode='a') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            book = px.load_workbook(self.EXCEL_FILE_NAME)
            sheet = book[sheet_name]
            # セルへ書き込む
            sheet['F1'] = '最大応力'
            sheet['G1'] = max_stress
            sheet['F2'] = 'ヤング率'
            sheet['G2'] = a


            # 散布図の追加
            # 散布図をグラフ変数:chartとして定義
            chart=px.chart.ScatterChart()

            # y,xデータの範囲を選択
            x = px.chart.Reference(book[sheet_name] ,min_col=3 ,max_col=3 ,min_row=2 ,max_row=MAX_ROW+1)
            y = px.chart.Reference(book[sheet_name] ,min_col=4 ,max_col=4 ,min_row=2 ,max_row=MAX_ROW+1)

            #系列変数seriesをy,xを指定して定義する
            series = px.chart.Series(y, x)
            #散布図として定義したchartへデータを指定したseries変数を渡す
            chart.series.append(series)
            chart.title = sheet_name
            chart.x_axis.title = 'Strain [-]'
            chart.y_axis.title = 'Stress [MPa]'
            #A6セルにグラフを表示
            book[sheet_name].add_chart(chart,"F5")


            # ヤング率用散布図の追加
            # 散布図をグラフ変数:chartとして定義
            chart2=px.chart.ScatterChart()

            # y,xデータの範囲を選択
            x = px.chart.Reference(book[sheet_name] ,min_col=3 ,max_col=3 ,min_row=2 ,max_row=int((MAX_ROW-1)*0.1))
            y = px.chart.Reference(book[sheet_name] ,min_col=4 ,max_col=4 ,min_row=2 ,max_row=int((MAX_ROW-1)*0.1))

            #系列変数seriesをy,xを指定して定義する
            series = px.chart.Series(y, x)
            #散布図として定義したchartへデータを指定したseries変数を渡す
            chart2.series.append(series)
            chart2.title = "10%"
            chart2.x_axis.title = 'Strain [-]'
            chart2.y_axis.title = 'Stress [MPa]'
            #A6セルにグラフを表示
            book[sheet_name].add_chart(chart2,"F23")

            print("Success: {}".format(FILE_NAME))
            # 保存する
            book.save(self.EXCEL_FILE_NAME)



        # まとめの追加 現状初回のみに対応している．
        df = pd.DataFrame()
        df["sheet_name"] = sheet_name_list
        df["tensile_strength"] = tensile_strength_list
        df["young's_modulus"] = young_modulus_list
        # エクセルファイルへ詳細を記載する．
        with pd.ExcelWriter(self.EXCEL_FILE_NAME, engine="openpyxl", mode='a') as writer:
            df.to_excel(writer, sheet_name="まとめ", index=False)



    def make_stress_strain(self):
        path_df = self._make_df()
        path_s = self._make_path_s(path_df)
        self._get_inputs(path_s)
        self._make_excel_file(path_df)
        self.write_excel()
    
    


class MakeStressStrainFromAnsysFile(MakeStressStrain):
    # ansysファイルから情報を収集する

    def _make_df(self):
        return pd.DataFrame()


    def _make_path_s(self, path_df):
        return


    def _get_inputs(self, path_s):
        # 入力値
        FILE_NAME_LIST = GetPath(first_path=self.first_path, slash=self.SLASH).get_list(kind="csv") #CSVファイルリスト
        self.FILE_NAME_LIST = sorted(FILE_NAME_LIST) # 並び替え．まだ不完全
        self.EXCEL_FILE_NAME = self.first_path + "summary.xlsx" # 出力先のpathをくっつける


    def _get_data_from_ansys(self, file_name):
        # ansysファイルからデータを収集する．
        self.POSITIVE_NEGATIVE = 1
        file_name = os.path.splitext(file_name)[0] + "." + settings.WRITE_EXTENSION

        def find_data(word):
            with open(file_name, encoding="utf-8_sig") as f: # 読み取り
                data_lines = f.readlines()
            for line in data_lines:
                if word in line:
                    try:
                        data = line.replace(" ", "")
                        data = data.split("=")[-1]
                        data = float(data.split("!")[0])
                        break
                    except:
                        pass
            return data
        DISTANCE = find_data(settings.DISTANCE)
        TIME = find_data(settings.TIME)
        self.SPEED = float(DISTANCE / TIME)
        self.LENGTH = float(find_data(settings.LENGTH)) # 試験片長さ（歪み算出用）
        self.CROSS_SECTIONAL_AREA = float(settings.CROSS_SECTIONAL_AREA/1000) # 断面積（応力算出用）




class MakeStressStrain2(MakeStressStrain):
    # csvファイル形式の変更

    def _csv_to_df(self, file_name):
        return super()._csv_to_df(file_name)
