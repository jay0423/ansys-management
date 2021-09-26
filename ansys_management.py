import sys
import os

import settings
import settings_check
from files_management import Refresh, WriteAnsysFile
from make_stress_strain import MakeStressStrain
from auto_analysis import AutoAnalysis


def refresh_main():

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


def write_ansys_file_main():
    a = WriteAnsysFile()
    a.make_files()


def path_multiple_stress_strain_main():
    a = MakeStressStrain()
    a.make_stress_strain()


def auto_analysis():
    first_path = "sample/"
    a = AutoAnalysis(first_path=first_path)
    a.dir_name = input("プロジェクト名を入力：")
    a.multiple_auto_analysis()



if __name__ == '__main__':
    settings_check.check_all()

    print("\n!!!　実行する作業の選択　!!!")
    print("0： ファイル名の更新")
    print("1： ファイルの自動生成")
    print("2： 応力ひずみ線図の作成")
    print("3： 自動解析")
    a = input("入力してください：")
    if a == "0":
        refresh_main()
    elif a == "1":
        write_ansys_file_main()
    elif a == "2":
        path_multiple_stress_strain_main()
    elif a == "3":
        auto_analysis()
    else:
        print("やり直してください．")
        sys.exit()
