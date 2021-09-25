import time
from ansys.mapdl.core import launch_mapdl


class AutoAnalysis:

    mapdl = None
    N = 3

    def __init__(self):
        self._num = 0


    def setup(self):
        self.mapdl = launch_mapdl()
        time.sleep(1)
        self.mapdl.cwd(r"C:\Users\matlab\ansys_kajimoto\test2")
        self.mapdl.filname("tset{}".format(self._num), key=1)

    
    def analysis(self):
        path = r"C:\Users\matlab\Documents\ansys-management\etc\sample_test\test1.ansys"
        self.mapdl.input(path)
        time.sleep(5)
        print("解析{} スタート".format(self._num))
        self.mapdl.solve()
        self.mapdl.finish()
        print("finish：解析{}".format(self._num))


    
    def output(self):
        self.mapdl.post26()
        self.mapdl.rforce(2, "NNUM", "F", "X", "FX")
        text = self.mapdl.prvar(2)
        output_path = "test{}.csv".format(self._num)
        with open(output_path, 'w') as f:
            f.write(text)
    

    def main(self):
        for _ in range(self.N):
            self._num += 1
            self.setup()
            self.analysis()
            self.output()
            self.mapdl.exit()
            time.sleep(5)
