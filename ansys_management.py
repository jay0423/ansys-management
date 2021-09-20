import sys

import settings
from files_management import Refresh, WriteAnsysFile
from make_stress_strain import MakeStressStrain



def refresh_main():
    OS = settings.OS
    if OS == "mac":
        SLASH = "/"
    elif OS == "windows":
        SLASH = "\ ".replace(" ", "")


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
        first_path += SLASH

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




if __name__ == '__main__':
    print("\n!!!　実行する作業の選択　!!!")
    print("0： ファイル名の更新")
    print("1： ファイルの自動生成")
    print("2： 応力ひずみ線図の作成")
    a = input("入力してください：")
    if a == "0":
        refresh_main()
    elif a == "1":
        write_ansys_file_main()
    elif a == "2":
        path_multiple_stress_strain_main()
    else:
        print("やり直してください．")
        sys.exit()
