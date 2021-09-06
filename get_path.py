"""
引数で渡される，first_pathより下にある指定ファイルのpathリストを返す．
"""

import glob

def get_list(first_path, kind="csv", N=10):

    if first_path[-1] == "/":
        first_path = first_path[:-1]

    path_list = []
    conma = "/*"
    for i in range(N):
        l = glob.glob("{}{}/*.{}".format(first_path, conma*i, kind), recursive=True)
        i += 1
        if l != []:
            path_list += l
        
    return path_list



if __name__ == "__main__":
    first_path = "."
    l = get_list(first_path)
    for l_ in l:
        print(l_)