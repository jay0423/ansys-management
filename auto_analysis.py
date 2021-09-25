import time
from ansys.mapdl.core import launch_mapdl


class AutoAnalysis:

    mapdl = None

    def __init__(self) -> None:
        pass


    def setup(self):
        self.mapdl = launch_mapdl()
        time.spleep(1)
        self.mapdl.cwd(r"C:\Users\matlab\ansys_kajimoto\test1")
        self.mapdl.filname("tset1", key=1)

    
    def analysis(self):
        path = r"C:\Users\matlab\Documents\ansys-management\etc\sample_test\test1.ansys"
        self.mapdl.input(path)
        time.sleep(5)
        print("解析スタート")
        self.mapdl.solve()
        self.mapdl.finish()
        print("finish")


    
    def output(self):
        self.mapdl.post26()
        self.mapdl.rforce(2, "NNUM", "F", "X", "FX")
        text = self.mapdl.prvar(2)
        output_path = "test.csv"
        with open(output_path, 'w') as f:
            f.write(text)
    

    def main(self):
        self.setup()
        self.analysis()
        self.output()
