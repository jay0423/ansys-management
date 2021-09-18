"""
Refresh：ファイル名をルールにのっとり改名する．
MakeFiles：settings.pyで設定されたディレクトリ構造で自動的に空ファイルを作成する．
WriteAnsysFile：base.ansysファイルを元に自動的に変数を埋め込み，ファイルを自動作成する．

Usage
ターミナルにて
ipython ansys_management.py
を入力し，選択肢から実行したい機能の数字を選択することで実行する．

Version
python 3.8.8
ipython 7.22.0
"""



import os
import sys
import pathlib
import itertools
import glob

import settings
import get_path




class Refresh:
    """
    ルールに乗っ取り，ファイル名を自動で修正する．
    setting.pyのABBREVIATIONでディレクトリ名の略称名称を定義し，それに従ってファイル名を決定する．

    ファイル名のルール
    ・フォルダ名の頭文字（settings.py）を繋げて作成する．
    exp.
    CFRP2本/thickness=2.0/gap=2.0/ のcsvファイルの場合 -> C2_l10_th2.0_g2.0.csv
    """

    ABBREVIATION = settings.ABBREVIATION
    OMISSION = settings.OMISSION
    FILE_EXTENSION = settings.FILE_EXTENSION


    def __init__(self, first_path):
        self.first_path = first_path
        self.kind = ""
        self.omission = True # ファイル無視をするかの選択
        self.only_word = ""


    def get_pre_path(self):
        # 変更前のパスを取得し，変更後のパスを作成する．
        pre_path_list = get_path.get_list(self.first_path, kind=self.kind) #ファイルリスト
        if self.omission:
            pre_path_list = [pre_path for pre_path in pre_path_list if pre_path.split("/")[-1] not in self.OMISSION] # 除外ファイルをなくす処理
        if self.only_word != "":
            pre_path_list = [pre_path for pre_path in pre_path_list if pre_path.split("/")[-1] == self.only_word] # 
        return pre_path_list


    def get_post_path(self, pre_path_list):
        # 変更前のパスを受け取り，変更後のパスを作成する．
        pre_path_list_list = [pre_path.split("/") for pre_path in pre_path_list]
        post_path_list = []
        for pre_path in pre_path_list_list:
            new_file_name = ""
            for path in pre_path[1:-1]: # 最初のパスとファイル名を省いたものをループで回している．
                try:
                    if "=" in path: # 名前に=が含まれていない場合
                        new_file_name += "_" + self.ABBREVIATION[path.split("=")[0]] + path.split("=")[-1] # 略称からファイル名を取得する．
                    else:
                        new_file_name += "_" + self.ABBREVIATION[path] # 略称からファイル名を取得する．
                except:
                    print("ディレクトリ名がまちがえています．やり直してください．")
                    print("/".join(pre_path))
                    sys.exit()
            new_file_name = "/".join(pre_path[:-1]) + "/" + new_file_name[1:] + ".{}".format(self.kind)
            post_path_list.append(new_file_name)
        return post_path_list


    def refresh(self):
        # ディレクトリ名の従ってファイル名を更新する．
        pre_path_list = []
        post_path_list = []
        for k in self.FILE_EXTENSION:
            self.kind = k
            pre_path_list_ = self.get_pre_path()
            post_path_list_ = self.get_post_path(pre_path_list_)
            pre_path_list += pre_path_list_
            post_path_list += post_path_list_

        if pre_path_list == post_path_list:
            print("変更なし")
            sys.exit()
        
        for pre_path, post_path in zip(pre_path_list, post_path_list):
            if pre_path != post_path:
                print("変更前：", pre_path)
                print("変更後：", post_path)
                print()
        a = input("実行:0，中断:1　：")
        if a != "0":
            print("初めからやり直してください．")
            sys.exit()

        for pre_path, post_path in zip(pre_path_list, post_path_list):
            if pre_path != post_path:
                os.rename(pre_path, post_path)
        print("\n完了．")
    

    def refresh_force(self, print_permissoin=False):
        # ディレクトリ名の従ってファイル名を更新する．
        pre_path_list = []
        post_path_list = []
        for k in self.FILE_EXTENSION:
            self.kind = k
            pre_path_list_ = self.get_pre_path()
            post_path_list_ = self.get_post_path(pre_path_list_)
            pre_path_list += pre_path_list_
            post_path_list += post_path_list_
        for pre_path, post_path in zip(pre_path_list, post_path_list):
            if pre_path != post_path:
                if print_permissoin:
                    print(post_path)
                os.rename(pre_path, post_path)






class MakeFiles:
    """
    settings.pyのディレクトリ構造(DIR_STRUCTURE)を元に新たなファイルを作成する．
    """

    FILE_EXTENSION = settings.FILE_EXTENSION
    DIR_STRUCTURE = settings.DIR_STRUCTURE


    def __init__(self):
        self.kind = "ansys"
        self.first_path = "2/"
        self.all = True # パスを作成する際，全ての部分でパスを作成するのかを選択することができる．
        self.make_file_all_path = True # 全てのファイルを作成する．


    def make_path(self):
        # DIR_STRUCTUREをもとにパスを作成する．
        first_path = self.first_path
        dir_list_list = [dir_list[1] for dir_list in self.DIR_STRUCTURE[first_path]]
        dir_name_list = [dir_list[0] for dir_list in self.DIR_STRUCTURE[first_path]]
        product_list = list(itertools.product(*dir_list_list))
        path_list = []
        for product in product_list:
            path = first_path
            for dir_name, num in zip(dir_name_list, product):
                path += dir_name + "=" + str(num) + "/"
            path_list.append(path)
        return path_list


    def make_path_all(self):
        # 全てのパスを作成する
        first_path = self.first_path
        path_list_all = []
        for i in range(len(self.DIR_STRUCTURE[first_path])):
            dir_structure_list = self.DIR_STRUCTURE[first_path][:i+1]
            dir_list_list = [dir_list[1] for dir_list in dir_structure_list]
            dir_name_list = [dir_list[0] for dir_list in dir_structure_list]
            product_list = list(itertools.product(*dir_list_list))
            path_list = []
            for product in product_list:
                path = first_path
                for dir_name, num in zip(dir_name_list, product):
                    path += dir_name + "=" + str(num) + "/"
                path_list.append(path)
            path_list_all += path_list
        return path_list_all



    def make_dir(self):
        # ディレクトリを自動的に生成する．
        if self.all:
            path_list = self.make_path_all()
        else:
            path_list = self.make_path()
        for path in path_list:
            try:
                os.mkdir(path)
            except:
                continue


    def make_damy_files(self):
        # ダミーファイルを作成する．
        self.make_dir()
        if self.all:
            path_list = self.make_path_all()
        else:
            path_list = self.make_path()
        for path in path_list:
            try:
                make_permission = True
                for files in glob.glob(path + "*"):
                    if self.kind == os.path.splitext(files)[1][1:]:
                        make_permission = False # 既存ファイルがある場合にファイルを作成しなくなる．
                    if self.make_file_all_path:
                        if self.DIR_STRUCTURE[self.first_path][-1][0] != files.split("/")[-2].split("=")[0]:
                            make_permission = False
                if make_permission:
                    pathlib.Path(path + "damy_file.{}".format(self.kind)).touch()
                else:
                    continue
            except:
                continue


    def change_damy_files(self):
        # damy_fileを変換する．
        a = Refresh(self.first_path)
        a.only_word = "damy_file.{}".format(self.kind)
        a.refresh_force(print_permissoin=True)


    def make_files(self):
        for k in self.FILE_EXTENSION:
            self.kind = k
            self.make_damy_files()
            self.change_damy_files()






class WriteAnsysFile:

    def __init__(self) -> None:
        pass


    def write(self):
        # base.ansysの変数部分に値を入力したファイルを出力する．
        path = "2/CFRP2_lap=20/base.ansys"
        with open(path) as f:
            s = f.read()
            print(type(s))
            print(s)






"""
以下，実行用の関数
"""


def refresh_main():
    print("\n!!!　必ず事前にgitでコミットしておいてください　!!!")
    completion = input("完了: 0, 未完了: 1　：")
    if completion != "0":
        print("やり直してください．")
        sys.exit()

    # ファーストパスの選択
    first_path = input("ファーストパス　1, 2：")
    if first_path != "1" and first_path != "2":
        print("やり直してください．")
        sys.exit()
    else:
        first_path += "/"

    a = Refresh(first_path)
    a.refresh()



def make_files_main():
    a = MakeFiles()
    a.make_files()



def write_ansys_file_main():
    a = WriteAnsysFile()
    a.write()







if __name__ == '__main__':
    print("\n0： refresh（ファイル名をルール通りに更新する．）")
    print("1： make files（ファイルを自動的に作成する．）")
    print("2： write ansys\n")
    a = input("入力してください：")
    if a == "0":
        refresh_main()
    elif a == "1":
        make_files_main()
    elif a == "2":
        write_ansys_file_main()
    else:
        print("やり直してください．")
        sys.exit()
