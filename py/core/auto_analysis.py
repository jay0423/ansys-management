"""
Ansys Mapdl
"""

import os
import sys
import time

from ansys.mapdl.core import launch_mapdl

from ..settings import settings
from .get_path import GetPath



class AutoAnalysis:

    SLASH = os.path.normcase("a/")[-1]
    PY_DIR_PATH = settings.PY_DIR_PATH # パスの初め
    CWD_PATH = settings.CWD_PATH
    mapdl = None
    N = 3
    file_record_list = []


    def __init__(self, first_path, output_csv=True):
        self.dir_name = "test"

        self.first_path = first_path
        self.input_path = self.PY_DIR_PATH
        self.output_path = self.PY_DIR_PATH
        self.output_csv = output_csv


    def _setup(self):
        # ansysの立ち上げとデータの保存先とプロジェクト名の決定
        
        self.mapdl = launch_mapdl()
        time.sleep(1)
        # print("データ保存パス：{}".format(self.cwd_path+self.dir_name))
        self.mapdl.cwd(self.CWD_PATH+self.dir_name)
        filname = "".join(self.input_path.split(self.SLASH)[-1].split(".")[:-1])
        # 以下，これまでのansysのfilnameと名前がかぶっている場合，名前の語尾に番号を振って見分けられるように実装している．
        i = 0
        filname_sub = filname
        while True:
            i += 1
            if filname in self.file_record_list:
                filname = filname_sub + "_{}".format(i)
            else:
                break
        if filname == filname_sub:
            print("{} -> {}".format(self.input_path, filname)) # 被っていない場合，ここでエラーが生じる
        self.mapdl.filname(filname, key=1)
        self.file_record_list.append(filname)
        # print("プロジェクト名：{}".format(filname))


    
    def _analysis(self):
        # 解析条件ファイルを実行
        # path = r"C:\Users\matlab\Documents\ansys-management\etc\sample_test\test1.ansys"
        t1 = time.time()
        self.mapdl.input(self.input_path)
        time.sleep(1)
        try:
            self.mapdl.solve()
        except:
            print("Warning")
            pass
        self.mapdl.finish()
        t2 = time.time()
        elapsed_time = round(t2-t1, 1)
        print("finish：{}，Time：{}s".format(self.input_path, elapsed_time))


    def _csv_output(self):
        # csvファイルへの書き込み
        self.mapdl.post26()
        self.mapdl.rforce(2, "NNUM", "F", "X", "FX")
        text = self.mapdl.prvar(2)
        with open(self.output_path, 'w') as f:
            f.write(text)
    

    def single_auto_analysis(self, input_path, output_path):
        self.input_path = self.PY_DIR_PATH + input_path
        self.output_path = self.PY_DIR_PATH + output_path
        self._setup()
        self._analysis()
        self._csv_output()
        self.mapdl.exit()


    def multiple_auto_analysis(self, path_list):
        for pair_path in path_list:
            if ".ansys" in pair_path[0].split(self.SLASH)[-1]:
                self.input_path = self.PY_DIR_PATH + pair_path[0]
                self.output_path = self.PY_DIR_PATH + pair_path[1]
            else:
                self.input_path = self.PY_DIR_PATH + pair_path[1]
                self.output_path = self.PY_DIR_PATH + pair_path[0]
            self._setup()
            self._analysis()
            if self.output_csv:
                self._csv_output()
            self.mapdl.exit()
            time.sleep(3)