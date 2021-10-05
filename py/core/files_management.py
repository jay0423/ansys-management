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

from ..settings import settings
from .get_path import GetPath




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
    SLASH = os.path.normcase("a/")[-1]


    def __init__(self, first_path):
        self.first_path = os.path.normcase(first_path)
        self.kind = ""
        self.omission = True # ファイル無視をするかの選択
        self.only_word = ""


    def _get_pre_path(self):
        # 変更前のパスを取得し，変更後のパスを作成する．
        pre_path_list = GetPath(first_path=self.first_path, slash=self.SLASH).get_list(kind=self.kind) #ファイルリスト
        if self.omission:
            pre_path_list = [pre_path for pre_path in pre_path_list if pre_path.split(self.SLASH)[-1] not in self.OMISSION] # 除外ファイルをなくす処理
        if self.only_word != "":
            pre_path_list = [pre_path for pre_path in pre_path_list if pre_path.split(self.SLASH)[-1] == self.only_word] # 
        return pre_path_list


    def _get_post_path(self, pre_path_list):
        # 変更前のパスを受け取り，変更後のパスを作成する．
        pre_path_list_list = []
        for pre_path in pre_path_list:
            path_list = []
            for dir in pre_path.split(self.SLASH):
                if dir not in self.first_path.split(self.SLASH):
                    path_list.append(dir)
            pre_path_list_list.append(path_list)

        post_path_list = []
        for pre_path in pre_path_list_list:
            new_file_name = ""
            for path in pre_path[:-1]: # ダミーファイル名を省いたものをループで回している．
                try:
                    if "=" in path: # 名前に=が含まれていない場合
                        new_file_name += "_" + self.ABBREVIATION[path.split("=")[0]] + path.split("=")[-1] # 略称からファイル名を取得する．
                    else:
                        new_file_name += "_" + self.ABBREVIATION[path] # 略称からファイル名を取得する．
                except:
                    pass
            new_file_name = self.SLASH.join(pre_path[:-1]) + self.SLASH + new_file_name[1:] + ".{}".format(self.kind)
            post_path_list.append(new_file_name)
        post_path_list = [self.first_path + post_path for post_path in post_path_list]
        return post_path_list


    def refresh(self):
        # ディレクトリ名の従ってファイル名を更新する．
        pre_path_list = []
        post_path_list = []
        for k in self.FILE_EXTENSION:
            self.kind = k
            pre_path_list_ = self._get_pre_path()
            post_path_list_ = self._get_post_path(pre_path_list_)
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
            pre_path_list_ = self._get_pre_path()
            post_path_list_ = self._get_post_path(pre_path_list_)
            pre_path_list += pre_path_list_
            post_path_list += post_path_list_
        for pre_path, post_path in zip(pre_path_list, post_path_list):
            if pre_path != post_path:
                if print_permissoin:
                    print("create: {}".format(post_path))
                os.rename(pre_path, post_path)






class MakeFiles:
    """
    settings.pyのディレクトリ構造(DIR_STRUCTURE)を元に新たなファイルを作成する．
    """

    FILE_EXTENSION = settings.FILE_EXTENSION
    DIR_STRUCTURE = settings.DIR_STRUCTURE
    SLASH = os.path.normcase("a/")[-1]
    BASE_PATH = settings.BASE_PATH


    def __init__(self, first_path):
        self.kind = ""
        self.first_path = first_path
        self.all = True # パスを作成する際，全ての部分でパスを作成するのかを選択することができる．
        self.make_file_all_path = True # 全てのファイルを作成する．


    def _make_path(self):
        # DIR_STRUCTUREをもとにパスを作成する．
        first_path = self.first_path
        dir_list_list = [dir_list[1] for dir_list in self.DIR_STRUCTURE[first_path]]
        dir_name_list = [dir_list[0] for dir_list in self.DIR_STRUCTURE[first_path]]
        product_list = list(itertools.product(*dir_list_list))
        path_list = []
        for product in product_list:
            path = first_path
            for dir_name, num in zip(dir_name_list, product):
                path += dir_name + "=" + str(num) + self.SLASH
            path_list.append(path)
        return path_list


    def _make_path_all(self):
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
                    path += dir_name + "=" + str(num) + self.SLASH
                path_list.append(path)
            path_list_all += path_list
        return path_list_all



    def _make_dir(self):
        # ディレクトリを自動的に生成する．
        if self.all:
            path_list = self._make_path_all()
        else:
            path_list = self._make_path()
        for path in path_list:
            try:
                os.mkdir(path)
            except:
                continue


    def _make_damy_files(self):
        # ダミーファイルを作成する．
        self._make_dir()
        if self.all:
            path_list = self._make_path_all()
        else:
            path_list = self._make_path()
        for path in path_list:
            try:
                make_permission = True
                for files in glob.glob(path + "*"):
                    if self.kind == os.path.splitext(files)[1][1:]:
                        make_permission = False # 既存ファイルがある場合にファイルを作成しなくなる．
                    if self.make_file_all_path:
                        if self.DIR_STRUCTURE[self.first_path][-1][0] != files.split(self.SLASH)[-2].split("=")[0]:
                            make_permission = False
                if make_permission:
                    pathlib.Path(path + "damy_file.{}".format(self.kind)).touch()
                else:
                    continue
            except:
                continue


    def _change_damy_files(self):
        # damy_fileを変換する．
        if self.BASE_PATH != "":
            path = os.path.split(self.BASE_PATH)[0] + self.SLASH
        else:
            path = self.first_path
        a = Refresh(path)
        a.only_word = "damy_file.{}".format(self.kind)
        a.refresh_force(print_permissoin=True)


    def make_files(self):
        for k in self.FILE_EXTENSION:
            self.kind = k
            self._make_damy_files()
            self._change_damy_files()






class WriteAnsysFile(MakeFiles):


    SEARCH_WORDS = list(settings.ABBREVIATION.keys())
    WRITE_EXTENSION = settings.WRITE_EXTENSION
    DEFAOLUT_REPLACE_WORD_DICT = settings.DEFAOLUT_REPLACE_WORD_DICT


    def _replace_word(self, data_lines, replace_word_dict):
        # 変換して返す
        for search_key_word in self.SEARCH_WORDS:
            search_word = "{% " + search_key_word + " %}"
            for line in data_lines:
                if search_word in line:
                    try:
                        new_line = line.replace(search_word, replace_word_dict[search_key_word])
                    except:
                        new_line = line.replace(search_word, self.DEFAOLUT_REPLACE_WORD_DICT[search_key_word])
                    data_lines[data_lines.index(line)] = new_line
        return data_lines


    def _get_replace_word_dict(self, path):
        # パスから変換キーワードと数値を抽出し，辞書型を作成する．
        replace_word_dict = dict([tuple(key_word.split("=")) for key_word in path.split(self.SLASH)[:-1] if len(key_word.split("="))==2])
        return replace_word_dict


    def write(self, output_path):
        # base.ansysの変数部分に値を入力したファイルを出力する．
        def _get_new_base_path(first_path):
            BASE_PATH = first_path + "{}.{}".format(settings.BASE_FILE_NAME, settings.WRITE_EXTENSION)
            while True:
                if os.path.isfile(BASE_PATH):
                    break
                l = BASE_PATH.split(self.SLASH)[:-2] + [BASE_PATH.split("/")[-1]]
                BASE_PATH = os.path.join(*l) # base.ansysファイルの場所を一段下げる
            return BASE_PATH
        if self.BASE_PATH == "":
            self.BASE_PATH = _get_new_base_path(self.first_path)
        with open(self.BASE_PATH, encoding="utf-8_sig") as f: # 読み取り
            data_lines = f.readlines()
        replace_word_dict = self._get_replace_word_dict(output_path)
        data_lines = self._replace_word(data_lines=data_lines, replace_word_dict=replace_word_dict)
        with open(output_path, mode="w", encoding="utf-8_sig") as f: # 書き込み
            f.writelines(data_lines)


    def _make_damy_files(self):
        # ダミーファイルを作成する．
        self._make_dir()
        if self.all:
            path_list = self._make_path_all()
        else:
            path_list = self._make_path()
        for path in path_list:
            path = os.path.normcase(path) # パスのバグの修正
            make_permission = True
            for files in glob.glob(path + "*"):
                if self.kind == os.path.splitext(files)[1][1:]:
                    make_permission = False # 既存ファイルがある場合にファイルを作成しなくなる．
                if self.make_file_all_path:
                    if self.DIR_STRUCTURE[self.first_path][-1][0] != files.split(self.SLASH)[-2].split("=")[0]:
                        make_permission = False
            if make_permission:
                if self.kind == self.WRITE_EXTENSION: # 指定ファイルのみ
                    pathlib.Path(path + "damy_file.{}".format(self.kind)).touch()
                    self.write(output_path=path+"damy_file.{}".format(self.kind))
                else:
                    pathlib.Path(path + "damy_file.{}".format(self.kind)).touch()
            else:
                continue


    def delete_files(self):
        # ファイルとディレクトリが重複するファイルをまとめて削除する．
        path_list = os.listdir(self.first_path)
        path_list = [path for path in path_list if os.path.isfile(os.path.join(self.first_path, path))] # ファイルだけに絞る
        path_list = [path for path in path_list if os.path.splitext(path)[-1][1:] in settings.FILE_EXTENSION]  # 特定の拡張子に絞る
        path_list = [path for path in path_list if path not in settings.OMISSION] # 特定のファイルを削除する．
        path_list = [os.path.join(self.first_path, path) for path in path_list] # ファイル名にパスをつける
        for path in path_list:
            print("delete: {}".format(path))
            os.remove(path)