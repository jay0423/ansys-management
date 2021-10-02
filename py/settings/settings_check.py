from . import settings
import os
import sys
import pprint


### settings.pyのチェック

def dir_ignore():
    pass


def path_file_name():
    pass


def file_extension():
    pass


def abbrebiation():
    pass

def dir_ignore():
    pass

def omission():
    pass


def dir_structure():
    pass


def base_file_name():
    pass


def write_extension():
    pass


def default_replace_word_dict():
    pass


def py_dir_path():
    if settings.PY_DIR_PATH[-1] == "/" or settings.PY_DIR_PATH[-1] == "\ ".replace(" ", ""):
        pass
    elif settings.PY_DIR_PATH == "":
        pass
    else:
        print("error: settings.PY_DIR_PATH -> パスの最後にスラッシュをつけてください．")
        pprint.pprint(settings.PY_DIR_PATH)
        sys.exit()


def cwd_path():
    pass


### 初期チェック
def base_path(first_path):
    # BASE_PATHに入力されていない場合，そこにbase.ansysファイルがあるのかを検証．
    BASE_PATH = settings.BASE_PATH
    if BASE_PATH == "": # ファーストパス直下にある場合
        BASE_PATH = os.path.normcase(first_path + "{}.{}".format(settings.BASE_FILE_NAME, settings.WRITE_EXTENSION))
        if os.path.isfile(BASE_PATH):
            pass
        else:
            SLASH = os.path.normcase("a/")[-1]
            BASE_PATH = os.path.normcase(first_path.split(SLASH)[0] + SLASH + settings.BASE_FILE_NAME + "." + settings.WRITE_EXTENSION) # 初期パスの最初のディレクトリにファイルがあるか確認する．
            if os.path.isfile(BASE_PATH):
                pass
            else:
                print("Error：{}が存在しません．settings.pyのBASE_PATHを正しく設定してください．".format(BASE_PATH))
                sys.exit()
    else: # BASE_PATHにbase.ansysがある場合
        if os.path.isfile(BASE_PATH):
            pass
        else:
            print("Error：{}が存在しません．settings.pyのBASE_PATHを正しく設定してください．".format(first_path))
            sys.exit()



def find_solve(first_path):
    BASE_PATH = settings.BASE_PATH
    if BASE_PATH == "":
        BASE_PATH = first_path + "{}.{}".format(settings.BASE_FILE_NAME, settings.WRITE_EXTENSION)
    try:
        with open(BASE_PATH, encoding="utf-8_sig") as f: # 読み取り
            data_lines = f.readlines()
    except: # 2週目以降
        SLASH = os.path.normcase("a/")[-1]
        BASE_PATH = first_path.split(SLASH)[0] + SLASH + settings.BASE_FILE_NAME + "." + settings.WRITE_EXTENSION # 初期パスの最初のディレクトリにファイルがあるか確認する．
        with open(BASE_PATH, encoding="utf-8_sig") as f: # 読み取り
            data_lines = f.readlines()

    for line in data_lines:
        if "solve" in line.lower():
            print("Warning：{}に'SOLVE'が含まれておりバグの原因となります．'SOLVE'以降のansysコードを削除して再度実行してください．".format(os.path.basename(BASE_PATH)))
            a = input("0: やり直す(推奨)\n1: 警告を無視する\n入力：")
            if a == "0":
                print("'SOLVE'以降を削除してください．")
                sys.exit()
            else:
                print("生成したansysファイルには'SOLVE'が含まれています．")


def check_all():
    abbrebiation()
    dir_structure()
    default_replace_word_dict()
    # base_path()
    dir_ignore()
    path_file_name()
    file_extension()
    omission()
    base_file_name()
    write_extension()
    py_dir_path()
    cwd_path()