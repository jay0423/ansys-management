import os
import sys
import pandas as pd

import settings
import get_path


class Refresh:

    ABBREVIATION = settings.ABBREVIATION

    def __init__(self, first_path, kind="ansys"):
        self.first_path = first_path
        self.kind = kind


    def get_pre_path(self):
        # 変更前のパスを取得し，変更後のパスを作成する．
        pre_path_list = get_path.get_list(self.first_path, kind=self.kind) #ファイルリスト
        return pre_path_list


    def get_post_path(self, pre_path_list):
        # 変更前のパスを受け取り，変更後のパスを作成する．
        pre_path_list_list = [pre_path.split("/") for pre_path in pre_path_list]
        post_path_list = []
        for pre_path in pre_path_list_list:
            new_file_name = ""
            for path in pre_path[1:-1]: # 最初のパスとファイル名を省いたものをループで回している．
                try:
                    new_file_name += "_" + self.ABBREVIATION[path.split("=")[0]] + path.split("=")[-1] # 略称からファイル名を取得する．
                except:
                    print("ディレクトリ名がまちがえています．やり直してください．")
                    print(path)
                    sys.exit()
            new_file_name = "/".join(pre_path[:-1]) + "/" + new_file_name[1:] + ".{}".format(self.kind)
            post_path_list.append(new_file_name)

        return post_path_list


    def refresh(self):
        # ディレクトリ名の従ってファイル名を更新する．
        pre_path_list = self.get_pre_path()
        post_path_list = self.get_post_path(pre_path_list)

        if pre_path_list == post_path_list:
            print("変更なし")
            sys.exit()
        
        for pre_path, post_path in zip(pre_path_list, post_path_list):
            if pre_path != post_path:
                os.rename(pre_path, post_path)
                print("変更前：", pre_path)
                print("変更後：", post_path)
                print("\n")




if __name__ == '__main__':
    print("本プログラムを実行する際，必ず事前にgitでコミットしておいてください．")
    completion = input("完了: 0, 未完了: 1　：")
    if completion != "0":
        print("やり直してください．")
        sys.exit()


    first_path = "1/"
    kind = input("ansys: 0, csv: 1　：")
    if kind == "0":
        kind = "ansys"
    elif kind == "1":
        kind = "csv"
    else:
        print("やり直してください．")
        sys.exit()
    print()

    a = Refresh(first_path, kind)
    a.refresh()
