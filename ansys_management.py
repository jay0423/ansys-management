import sys
import os
import time

import settings
import settings_check
from get_path import GetPath
from files_management import Refresh, WriteAnsysFile
from make_stress_strain import MakeStressStrain
from auto_analysis import AutoAnalysis


def refresh_main():
    # ファイル名の修正
    print("\n!!!　必ず事前にgitでコミットしておいてください　!!!")
    completion = input("完了: 0, 未完了: 1　：")
    if completion != "0":
        print("やり直してください．")
        sys.exit()

    # ファーストパスの選択
    files_dir = [f for f in os.listdir() if os.path.isdir(os.path.join(f))]
    files_dir = [f for f in sorted(files_dir) if f not in settings.DIR_IGNORE]
    for i, l in enumerate(files_dir):
        print("{}： {}".format(i, l))
    first_path = int(input("入力してください："))
    try:
        first_path = files_dir[first_path]
    except:
        print("やり直してください．")
        sys.exit()

    a = Refresh(first_path)
    a.refresh()


# def make_files_main():
#     a = MakeFiles()
#     a.make_files()


def _find_first_path():
    # 初期ディレクトリのパスを選択する．
    print("\n初期パスの選択")
    key_list = list(settings.DIR_STRUCTURE.keys())
    for i, key in enumerate(key_list):
        print("{}： {}".format(i, key))
    j = int(input("入力してください："))
    first_path = key_list[j]
    return first_path


def write_ansys_file_main():
    # ファイルの自動生成とbase.ansysの書き込み
    first_path = _find_first_path()
    a = WriteAnsysFile(first_path)
    a.make_files()


def path_multiple_stress_strain_main():
    # 応力ひずみ線図の生成
    a = MakeStressStrain()
    a.make_stress_strain()


def auto_analysis():
    # 自動解析の実行
    SLASH = os.path.normcase("a/")[-1]

    # ファーストパスの選択
    files_dir = [f for f in os.listdir() if os.path.isdir(os.path.join(f))]
    files_dir = [f for f in sorted(files_dir) if f not in settings.DIR_IGNORE]
    print("\nディレクトリの選択")
    for i, l in enumerate(files_dir):
        print("{}： {}{}".format(i, l, SLASH))
    first_path = int(input("入力してください："))
    try:
        first_path = files_dir[first_path]
    except:
        print("やり直してください．")
        sys.exit()
    first_path = os.path.normcase(first_path + SLASH)

    dir_name = input("\nプロジェクト名（ansysファイル格納ディレクトリ名）を入力：")
    os.mkdir(settings.CWD_PATH + SLASH + dir_name)
    # 実行ファイルのパスを取得
    a = GetPath(first_path=first_path, slash=SLASH)
    path_list = a.get_list_multiple(kind_list=["csv", "ansys"])
    path_list = a.get_pair_list(path_list, omission_files=settings.OMISSION)
    print("\n実行ファイルの確認")
    for path in path_list:
        print(path[0])
    completion = input("0: 実行, 1: やりなおす\n入力してください：")
    if completion != "0":
        print("やり直してください．")
        sys.exit()

    b = AutoAnalysis(first_path=first_path)
    b.dir_name = dir_name
    t1 = time.time()
    b.multiple_auto_analysis(path_list)
    t2 = time.time()
    elapsed_time = t2-t1
    print(f"経過時間：{elapsed_time}")


def all():
    # ファイルの自動生成，自動解析，応力ひずみ線図の生成
    SLASH = os.path.normcase("a/")[-1]
    first_path = _find_first_path()
    dir_name = input("\nプロジェクト名（ansysファイル格納ディレクトリ名）を入力：")
    os.mkdir(settings.CWD_PATH + SLASH + dir_name)

    a = WriteAnsysFile(first_path)
    a.make_files()
    print("ファイル作成完了\n")

    # 実行ファイルのパスを取得
    print("解析開始")
    b = GetPath(first_path=first_path, slash=SLASH)
    path_list = b.get_list_multiple(kind_list=["csv", "ansys"])
    path_list = b.get_pair_list(path_list, omission_files=settings.OMISSION)
    c = AutoAnalysis(first_path=first_path)
    c.dir_name = dir_name
    t1 = time.time()
    c.multiple_auto_analysis(path_list)
    t2 = time.time()
    elapsed_time = t2-t1
    print(f"総解析時間：{elapsed_time}")
    print("解析完了\n")

    path_multiple_stress_strain_main()
    print("応力ひずみ線図作成の完了")




if __name__ == '__main__':
    settings_check.check_all()

    print("\n!!!　実行する作業の選択　!!!")
    print("0： ファイル名の更新")
    print("1： ファイルの自動生成")
    print("2： 応力ひずみ線図の作成")
    print("3： 自動解析")
    print("4： all")
    a = input("入力してください：")
    if a == "0":
        refresh_main()
    elif a == "1":
        write_ansys_file_main()
    elif a == "2":
        path_multiple_stress_strain_main()
    elif a == "3":
        auto_analysis()
    elif a == "4":
        all()
    else:
        print("やり直してください．")
        sys.exit()
