"""
Ansys Mapdl
"""

import os
import sys
import time
from glob import glob
import shutil

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


    def __init__(self, output_csv=True):
        self.dir_name = "test"

        # self.first_path = first_path
        self.input_path = self.PY_DIR_PATH
        self.output_path = self.PY_DIR_PATH
        self.output_csv = output_csv

        self.dir_name = None


    def _setup(self):
        # ansysの立ち上げとデータの保存先とプロジェクト名の決定
        
        self.mapdl = launch_mapdl(nproc=settings.NPROC)
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
        if filname != filname_sub:
            print("{} -> {}".format(self.input_path, filname)) # 被っていない場合，ここでエラーが生じる
        self.mapdl.filname(filname, key=1)
        self.file_record_list.append(filname)
        # print("プロジェクト名：{}".format(filname))



    def _analysis(self):
        # 解析条件ファイルを実行
        t1 = time.time()
        self.mapdl.input(self.input_path)
        time.sleep(1)
        success = True
        try:
            self.mapdl.solve()
        except:
            print("Warning: SOLVE")
            pass
        try:
            self.mapdl.finish()
        except:
            print("Warning: FINISH")
            success = False
            pass
        t2 = time.time()
        elapsed_time = round(t2-t1, 1)
        if success:
            print("Successful analysis：{}，Time：{}s".format(self.input_path, elapsed_time))


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


    def get_pair_list(self, ansys_path_list):
        csv_path_list = []
        for base_path in ansys_path_list:
            path = os.path.split(base_path)
            csv_path_list.append(path[0] + self.SLASH + os.path.splitext(path[1])[0] + ".csv")
        path_list = [(ansys, csv) for ansys, csv in zip(ansys_path_list, csv_path_list)]
        return path_list


    def multiple_auto_analysis(self, ansys_path_list):
        path_list = self.get_pair_list(ansys_path_list)
        for i in path_list:
            print(i)
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
                try:
                    self._csv_output()
                except: # 解析（input時点で）失敗したときようのエラー
                    print("Error analysis：{}".format(self.input_path))
            self.mapdl.exit()
            time.sleep(1)

            # ファイルの削除
            if settings.DELETE_ANSYS_FILES:
                shutil.rmtree(self.dir_name)
                time.sleep(30)
                for dirname in glob("{}ansys_*".format(settings.TEMP_PATH)):
                    shutil.rmtree(dirname)
                time.sleep(15)
                os.mkdir(self.dir_name)
