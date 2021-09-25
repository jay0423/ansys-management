from ansys.mapdl.core import launch_mapdl


class AutoAnalysis:

    mapdl = launch_mapdl()

    def __init__(self) -> None:
        pass


    def setup(self):
        self.mapdl.cwd(r"C:\Users\matlab\ansys_kajimoto\test")
        self.mapdl.filname("tset1", key=1)

    
    def analysis(self):
        path = "C:\Users\matlab\Documents\ansys-management\2\CFRP2_lap=20\thickness=2.0\C2_l20_th2.0.ansys"
        self.mapdl.input(path)


    
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
