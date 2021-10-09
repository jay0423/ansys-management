import sys
import os
import time

# ファイル自動作成または自動解析が実行されたとき，py/のsettings.pyへsettings_child.pyとpy/settings/settings_core.pyをコピペする．
with open(os.path.normcase("py/settings/settings_core.py"), encoding="utf-8_sig") as f: # 読み取り
    data_lines_core = f.readlines()
with open(os.path.normcase("settings_child.py"), encoding="utf-8_sig") as f: # 読み取り
    data_lines_child = f.readlines()
with open(os.path.normcase("py/settings/settings.py"), mode="w", encoding="utf-8_sig") as f: # 書き込み
    f.writelines(data_lines_child + data_lines_core)

from py.settings import settings_check
from py.settings import settings
from py.core.get_path import GetPath
from py.core.files_management import Refresh, WriteAnsysFile
from py.core.make_stress_strain import MakeStressStrain, MakeStressStrainFromAnsysFile
from py.core.auto_analysis import AutoAnalysis


SLASH = os.path.normcase("a/")[-1]


################ 設定の管理 ###################

def settings_copy_to_child():
    """
    ファイル自動作成または自動解析が終了したとき，settings_child.pyへ
    py/settings/settings_copy_base.pyをコピペする．
    """
    with open(os.path.normcase("py/settings/settings_copy_base.py"), encoding="utf-8_sig") as f: # 読み取り
        data_lines_copy_base = f.readlines()
    with open(os.path.normcase("settings_child.py"), mode="w", encoding="utf-8_sig") as f: # 書き込み
        f.writelines(data_lines_copy_base)


def settings_memo(first_path):
    with open(os.path.normcase("py/settings/settings_core.py"), encoding="utf-8_sig") as f: # 読み取り
        data_lines_core = f.readlines()
    with open(os.path.normcase("settings_child.py"), encoding="utf-8_sig") as f: # 読み取り
        data_lines_child = f.readlines()
    with open(os.path.normcase(first_path + "settings_memo.py"), mode="w", encoding="utf-8_sig") as f: # 書き込み
        f.writelines(data_lines_child + data_lines_core)






################ 更新・自動生成・応力ひずみ線図・自動解析 ###################

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
        print("{}： {}{}".format(i+1, l, SLASH))
    first_path = int(input("入力してください："))
    try:
        first_path = files_dir[first_path-1] + SLASH
    except:
        print("やり直してください．")
        sys.exit()

    a = Refresh(first_path)
    a.refresh()


# def make_files_main():
#     a = MakeFiles()
#     a.make_files()


# def _find_first_path():
#     # 初期ディレクトリのパスを選択する．
#     print("\n初期パスの選択")
#     key_list = list(settings.DIR_STRUCTURE.keys())
#     for i, key in enumerate(key_list):
#         print("{}： {}".format(i, key))
#     j = int(input("入力してください："))
#     first_path = key_list[j]
#     return first_path


def write_ansys_file_main():
    # ファイルの自動生成とbase.ansysの書き込み
    key_list = list(settings.DIR_STRUCTURE.keys())
    for i, first_path in enumerate(key_list):
        print(first_path)
        if i == 0:
            settings_memo(first_path)
        settings_check.base_path(first_path)
        settings_check.find_solve(first_path)
        a = WriteAnsysFile(first_path)
        if i != 0:
            # 重複するファイルを削除する．
            a.delete_files()
        a.make_files()
    permission = input("settings_child.pyを初期化しますか？\n0: はい\n1: いいえ\n入力してください：")
    if permission == "0":
        settings_copy_to_child()



def path_multiple_stress_strain_main():
    # 応力ひずみ線図の生成
    a = MakeStressStrain()
    a.make_stress_strain()



def auto_analysis():
    # 自動解析の実行

    # ファーストパスの選択
    if settings.ANALYSIS_PATH == []:
        files_dir = [f for f in os.listdir() if os.path.isdir(os.path.join(f))]
        files_dir = [f for f in sorted(files_dir) if f not in settings.DIR_IGNORE]
        print("\nディレクトリの選択")
        for i, l in enumerate(files_dir):
            print("{}： {}{}".format(i+1, l, SLASH))
        first_path = int(input("入力してください："))
        try:
            first_path = files_dir[first_path-1]
        except:
            print("やり直してください．")
            sys.exit()
        first_path = os.path.normcase(first_path + SLASH)

    dir_name = input("\nプロジェクト名（ansysファイル格納ディレクトリ名）を入力：")
    os.mkdir(settings.CWD_PATH + SLASH + dir_name)
    # csvファイルへ時間と力の出力を実装するかの選択．
    output_csv = input("\ncsvファイルへ出力しますか？\n0: はい\n1: いいえ（ディレクトリ名を設定していない場合）\n入力してください：")
    if output_csv == "0":
        output_csv = True
    elif output_csv == "1":
        output_csv = False
    else:
        print("やり直してください．")
        sys.exit()

    # 実行ファイルのパスを取得
    if settings.ANALYSIS_PATH == []:
        a = GetPath(first_path=first_path, slash=SLASH)
        ansys_path_list = a.get_list("ansys", omission_files=settings.OMISSION)
    else:
        ansys_path_list = []
        for first_path in settings.ANALYSIS_PATH:
            a = GetPath(first_path=first_path, slash=SLASH)
            ansys_path_list += a.get_list("ansys", omission_files=settings.OMISSION)
    if output_csv: # csvに出力する場合
        csv_path_list = a.search_csv_files(ansys_path_list)
        path_list = [(ansys, csv) for ansys, csv in zip(ansys_path_list, csv_path_list)]
    else:
        path_list = [(ansys, csv) for ansys, csv in zip(ansys_path_list, [""]*len(ansys_path_list))]
    print("\n実行ファイルの確認")
    for path in path_list:
        print(path[0])
    completion = input("0: 実行, 1: やりなおす\n入力してください：")
    if completion != "0":
        print("やり直してください．")
        sys.exit()

    b = AutoAnalysis(output_csv=output_csv)
    b.dir_name = dir_name
    t1 = time.time()
    b.multiple_auto_analysis(path_list)
    t2 = time.time()
    elapsed_time = t2-t1
    print(f"経過時間：{elapsed_time}s")

    # 最終処理
    permission = input("settings_child.pyを初期化しますか？\n0: はい\n1: いいえ\n入力してください：")
    if permission == "0":
        settings_copy_to_child()



def all():
    # ファイルの自動生成，自動解析，応力ひずみ線図の生成
    # 初期設定
    dir_name = input("\nプロジェクト名（ansysファイル格納ディレクトリ名）を入力：")
    os.mkdir(settings.CWD_PATH + SLASH + dir_name)


    # ファイルの自動生成とbase.ansysの書き込み
    for i, first_path in enumerate(settings.DIR_STRUCTURE):
        if i == 0:
            settings_memo(first_path)
        settings_check.base_path(first_path)
        settings_check.find_solve(first_path)
        settings_check.distance_time_length(first_path)
        a = WriteAnsysFile(first_path)
        # 重複するファイルを削除する．
        a.delete_files()
        a.make_files()
    print("ファイル作成完了\n")
    time.sleep(1)

    # 自動解析
    # 実行ファイルのパスを取得
    print("解析開始")
    # all()の場合，settings.pyのDIR_STRUCTUREからパスを取得し，その部分のみの解析を行う．
    def get_first_path_list():
        # パスのリストを取得する．
        DIR_STRUCTURE = sorted(settings.DIR_STRUCTURE)
        dir0 = DIR_STRUCTURE[0]
        first_path_list = [dir0]
        for dir in DIR_STRUCTURE[1:]:
            if dir0 not in dir:
                first_path_list.append(dir)
        return first_path_list
    first_path_list = get_first_path_list() # 解析するファーストパスのリストを取得する．
    elapsed_time = 0
    for first_path in first_path_list:
        b = GetPath(first_path=first_path, slash=SLASH)
        path_list = b.get_list_multiple(kind_list=["csv", "ansys"])
        path_list = b.get_pair_list(path_list, omission_files=settings.OMISSION)
        # 自動解析の実行
        c = AutoAnalysis(first_path=first_path)
        c.dir_name = dir_name
        t1 = time.time()
        c.multiple_auto_analysis(path_list)
        t2 = time.time()
        elapsed_time += t2-t1
    print(f"総解析時間：{elapsed_time}s")
    print("解析完了\n")


    # 応力ひずみ線図のエクセルファイルの生成
    a = MakeStressStrainFromAnsysFile(first_path)
    a.make_stress_strain()
    print("応力ひずみ線図作成の完了")

    # 最終処理
    permission = input("settings_child.pyを初期化しますか？\n0: はい\n1: いいえ\n入力してください：")
    if permission == "0":
        settings_copy_to_child()



if __name__ == '__main__':
    settings_check.check_all()

    print("\n!!!　実行する作業の選択　!!!")
    print("-----------------------------")
    print("1： ファイルの自動生成")
    print("2： 応力ひずみ線図の作成")
    print("3： 自動解析")
    print("4： All")
    print("-----------------------------")
    print("5： ファイル名の更新")
    print("6： settings_childの初期化")
    print("-----------------------------")
    a = input("入力してください：")
    if a == "1":
        write_ansys_file_main()
    elif a == "2":
        path_multiple_stress_strain_main()
    elif a == "3":
        auto_analysis()
    elif a == "4":
        all()
    elif a == "5":
        refresh_main()
    elif a == "6":
        settings_copy_to_child()
    else:
        print("やり直してください．")
        sys.exit()
