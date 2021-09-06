import os
import sys

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
        pre_path_list = self.get_pre_path()
        post_path_list = self.get_post_path(pre_path_list)

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



class MakeFiles:


    DIR_STRUCTURE = settings.DIR_STRUCTURE

    def __init__(self) -> None:
        pass

    




def refresh():
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

    # 拡張子の選択
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



if __name__ == '__main__':
    refresh()