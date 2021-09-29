"""
Ansys Mapdl
"""

import os
import sys
import time

from ansys.mapdl.core import launch_mapdl

import settings
from get_path import GetPath



class AutoAnalysis:

    SLASH = os.path.normcase("a/")[-1]
    PY_DIR_PATH = settings.PY_DIR_PATH # パスの初め
    CWD_PATH = settings.CWD_PATH
    mapdl = None
    N = 3


    def __init__(self, first_path):
        self.dir_name = "test"

        self.first_path = first_path
        self.input_path = self.PY_DIR_PATH
        self.output_path = self.PY_DIR_PATH


    def _setup(self):
        # ansysの立ち上げとデータの保存先とプロジェクト名の決定
        
        self.mapdl = launch_mapdl()
        time.sleep(1)
        # print("データ保存パス：{}".format(self.cwd_path+self.dir_name))
        self.mapdl.cwd(self.CWD_PATH+self.dir_name)
        filname = "".join(self.input_path.split(self.SLASH)[-1].split(".")[:-1])
        # print("プロジェクト名：{}".format(filname))
        self.mapdl.filname(filname, key=1)

    
    def _analysis(self):
        # 解析条件ファイルを実行
        # path = r"C:\Users\matlab\Documents\ansys-management\etc\sample_test\test1.ansys"
        t1 = time.time()
        self.mapdl.input(self.input_path)
        time.sleep(5)
        try:
            self.mapdl.solve()
        except:
            print("Warning")
            pass
        self.mapdl.finish()
        t2 = time.time()
        elapsed_time = t2-t1
        print(f"解析時間：{elapsed_time}s")
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
        time.sleep(5)


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
            self._csv_output()
            self.mapdl.exit()
            time.sleep(10)