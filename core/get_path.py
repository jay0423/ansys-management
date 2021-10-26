"""
引数で渡される，first_pathより下にある指定ファイルのpathリストを返す．
"""

import os
import glob


class GetPath:

    def __init__(self, first_path, slash="/"):
        self.N = 10
        self.slash = slash
        if first_path[-1] == slash:
            self.first_path = first_path[:-1]
        else:
            self.first_path = first_path



    def get_list(self, kind="csv", omission_files=[]):
        path_list = []
        conma = self.slash + "*"
        for i in range(self.N):
            l = glob.glob("{}{}{}*.{}".format(self.first_path, conma*i, self.slash, kind), recursive=True)
            if l != []:
                path_list += l
        path_list = [path for path in path_list if path.split(self.slash)[-1] not in omission_files] 
            
        return path_list



    def get_list_multiple(self, kind_list=["csv", "ansys"]):

        path_list = []
        for kind in kind_list:
            path_list += self.get_list(kind=kind)
        return path_list





if __name__ == "__main__":
    a = input("1: get_list\n2: get_list_multiple\n3: get_pair_list\n4: search_files\n：")
    first_path = "1/"
    g = GetPath(first_path)
    if a == "1":
        l = sorted(g.get_list())
    elif a == "2":
        l = sorted(g.get_list_multiple())
    for l_ in l:
        print(l_)