"""
ansys
"""

import sys
import time

from ansys.mapdl.core import launch_mapdl

import settings
from get_path import GetPath


class AutoAnalysis:

    OS = settings.OS
    if OS == "mac":
        SLASH = "/"
    elif OS == "windows":
        SLASH = "\ ".replace(" ", "")
    mapdl = None
    N = 3

    def __init__(self):
        self.cwd_path = r"C:\Users\matlab\ansys_kajimoto\ ".replace(" ", "")
        self.project = "test"

        self.first_path = "2/"
        self.input_path = ""
        self.output_path = ""


    def _setup(self):
        self.mapdl = launch_mapdl(self.cwd_path+self.project)
        time.sleep(1)
        self.mapdl.cwd()
        filname = self.input_path.split(self.SLASH)[-1].split(".")[0]
        self.mapdl.filname(filname, key=1)

    
    def _analysis(self):
        # 解析条件ファイルを実行
        # path = r"C:\Users\matlab\Documents\ansys-management\etc\sample_test\test1.ansys"
        self.mapdl.input(self.input_path)
        time.sleep(5)
        self.mapdl.solve()
        self.mapdl.finish()
        print("finish：{}".format(self.input_path))


    def _output(self):
        self.mapdl.post26()
        self.mapdl.rforce(2, "NNUM", "F", "X", "FX")
        text = self.mapdl.prvar(2)
        with open(self.output_path, 'w') as f:
            f.write(text)
    

    def single_main(self):
        self._setup()
        self._analysis()
        self._output()
        self.mapdl.exit()
        time.sleep(5)


    def main(self):
        a = GetPath(first_path=self.first_path, slash=self.SLASH)
        path_list = a.get_list_multiple(kind_list=["csv", "ansys"])
        path_list = a.get_pair_list(path_list)
        for pair_path in path_list:
            if ".ansys" in pair_path[0].split(self.SLASH)[-1]:
                self.input_path = pair_path[0]
                self.output_path = pair_path[1]
            else:
                self.input_path = pair_path[1]
                self.output_path = pair_path[0]
            self._setup()
            self._analysis()
            self._output()
            self.mapdl.exit()
            time.sleep(5)


if __name__ == "__main__":
    a = AutoAnalysis()
    a.main()