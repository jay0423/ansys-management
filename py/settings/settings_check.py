from . import settings
import os
import sys
import platform
import pprint
import json
from importlib import reload


SLASH = os.path.normcase("a/")[-1]


### settings.pyのチェック

class FIRST_CHECK:

    def __init__(self) -> None:
        pass


    def dir_ignore(self):
        pass


    def path_file_name(self):
        pass


    def file_extension(self):
        pass


    def abbreviation(self):
        pass

    def dir_ignore(self):
        pass

    def omission(self):
        pass


    def dir_structure(self):
        DIR_STRUCTURE = settings.DIR_STRUCTURE
        for dir in DIR_STRUCTURE:
            if SLASH not in dir: # スラッシュがwindowsまたはmacに対応していない場合．
                print("Settings error: DIR_STRUCTUREのスラッシュが'{}'になっていません．".format(SLASH))
                sys.exit()
            if dir[-1] != SLASH:
                print("Settings error: DIR_STRUCTUREのパスの最後にスラッシュを入れてください．")
                sys.exit()
            
        if len(DIR_STRUCTURE) > 1:
            # if DIR_STRUCTURE[0] != sorted(DIR_STRUCTURE)[0]: # 書き順
            #     print("Settings error: DIR_STRUCTUREの順番を入れ替えてください．")
            #     sys.exit()
            
            dir_0 = list(DIR_STRUCTURE.keys())[0].split(SLASH)[0]
            for dir in DIR_STRUCTURE:
                if dir.split(SLASH)[0] != dir_0:
                    print("Settings error: DIR_STRUCTUREの初期バスのディレクトリ名が一致していません．")
                    sys.exit()

        # DIR_STRUCTURE内のディレクトリ名がABBREVIATIONに含まれていない場合，エラーを発生させる．
        for path in DIR_STRUCTURE:
            for pair in DIR_STRUCTURE[path]:
                if pair[0] not in settings.ABBREVIATION:
                    print("\nDIR_STRUCTUREに含まれるディレクトリ名(変数)がABBREVIATIONに存在していません．：{}".format(pair[0]))
                    a = input("新たに追加しますか？\n0: はい\n1: いいえ\n入力してください：")
                    if a == "0":
                        f = open(settings.ABBREVIATION_PATH, 'r')
                        new_ABBREVIATION = json.load(f)
                        f.close()
                        while True: # 重複しない省略ワードを入力するまで繰り返す．
                            new_word = input("\n'{}'の省略ワードを入力してください．例）thickness -> th\n入力してください：".format(pair[0]))
                            if new_word not in new_ABBREVIATION["ABBREVIATION"].values():
                                new_ABBREVIATION["ABBREVIATION"][pair[0]] = new_word # dictに新たなキーと値を追加した．
                                f2 = open(settings.ABBREVIATION_PATH, 'w')
                                json.dump(new_ABBREVIATION, f2, indent=4, ensure_ascii=False)
                                f2.close()
                                print('"{}": "{}"を追加しました．変更したい場合はpy/settings/abbreviation.jsonファイルから変更してください．'.format(pair[0], new_word))
                                break
                            else:
                                print("その省略値は既に存在しています．他の値を入力してください．")
                    else:
                        print("やり直してください．")
                        sys.exit()
        reload(settings)


    def base_file_name(self):
        pass


    def write_extension(self):
        pass


    def default_replace_word_dict(self):
        pass


    def py_dir_path(self):
        if settings.PY_DIR_PATH[-1] == "/" or settings.PY_DIR_PATH[-1] == "\ ".replace(" ", ""):
            pass
        elif settings.PY_DIR_PATH == "":
            pass
        else:
            print("Settings error: settings.PY_DIR_PATH -> パスの最後にスラッシュをつけてください．")
            pprint.pprint(settings.PY_DIR_PATH)
            sys.exit()


    def cwd_path(self):
        if platform.system() == "windows": # windowsのみ確認する．
            if not os.path.exists(settings.CWD_PATH):
                print("Settings error: {}のパスが存在していません．CWD_PATHを設定し直してください．".format(settings.CWD_PATH))
                sys.exit()



    def check_first_all(self):
        self.abbreviation()
        self.dir_structure()
        self.default_replace_word_dict()
        # base_path()
        self.dir_ignore()
        self.path_file_name()
        self.file_extension()
        self.omission()
        self.base_file_name()
        self.write_extension()
        self.py_dir_path()
        self.cwd_path()






class FIRST_PATH_CHECK:

    def __init__(self, first_path):
        self.first_path = first_path


    ### first_path先に初期チェック
    def _get_new_base_path(self, first_path):
        BASE_PATH = first_path + "{}.{}".format(settings.BASE_FILE_NAME, settings.WRITE_EXTENSION)
        while True:
            if os.path.isfile(BASE_PATH):
                break
            l = BASE_PATH.split(SLASH)[:-2] + [BASE_PATH.split("/")[-1]]
            BASE_PATH = os.path.join(*l) # base.ansysファイルの場所を一段下げる
        return BASE_PATH


    def base_path(self):
        # BASE_PATHに入力されていない場合，そこにbase.ansysファイルがあるのかを検証．
        first_path = os.path.normcase(self.first_path)
        BASE_PATH = os.path.normcase(settings.BASE_PATH)
        if BASE_PATH == "": # ファーストパス直下にある場合
            try:
                BASE_PATH = self._get_new_base_path(first_path)
            except:
                print("Settings error：{}が存在しません．settings.pyのBASE_PATHを正しく設定してください．".format(BASE_PATH))
                sys.exit()
        else:
            if not os.path.isfile(BASE_PATH):
                print("Settings error：{}が存在しません．settings.pyのBASE_PATHを正しく設定してください．".format(first_path))
                sys.exit()


    def distance_time_length(self):
        # DISTANCE, TIME, LENGTH
        first_path = os.path.normcase(self.first_path)
        BASE_PATH = os.path.normcase(settings.BASE_PATH)
        if BASE_PATH == "": # ファーストパス直下にある場合
            BASE_PATH = self._get_new_base_path(first_path)

        def find_data(word):
            with open(BASE_PATH, encoding="utf-8_sig") as f: # 読み取り
                data_lines = f.readlines()
            for line in data_lines:
                if word in line:
                    try:
                        data = line.replace(" ", "")
                        data = data.split("=")[-1]
                        data = float(data.split("!")[0])
                        break
                    except:
                        pass
            return data

        try:
            DISTANCE = float(find_data(settings.DISTANCE))
        except:
            print("Settings error: DISTANCEが{}.{}に存在していません．".format(settings.BASE_PATH, settings.WRITE_EXTENSION))
            sys.exit()
        try:
            TIME = float(find_data(settings.TIME))
        except:
            print("Settings error: TIMEが{}.{}に存在していません．".format(settings.BASE_PATH, settings.WRITE_EXTENSION))
            sys.exit()
        try:
            LENGTH = float(find_data(settings.LENGTH))
        except:
            print("Settings error: LENGTHが{}.{}に存在していません．".format(settings.BASE_PATH, settings.WRITE_EXTENSION))
            sys.exit()



    def find_solve(self):
        # 引数のパスにあるbase.ansys内にSOLVEがないことを確認し，ある場合はエラーを発生させる．
        first_path = os.path.normcase(self.first_path)
        BASE_PATH = os.path.normcase(settings.BASE_PATH)
        if BASE_PATH == "":
            BASE_PATH = self._get_new_base_path(first_path)
        with open(BASE_PATH, encoding="utf-8_sig") as f: # 読み取り
            data_lines = f.readlines()

        for line in data_lines:
            if "solve" in line.lower():
                print("Warning: {}に'SOLVE'が含まれておりバグの原因となります．'SOLVE'以降のansysコードを削除して再度実行してください．".format(os.path.basename(BASE_PATH)))
                a = input("0: やり直す(推奨)\n1: 警告を無視する\n入力：")
                if a == "0":
                    print("'SOLVE'以降を削除してください．")
                    sys.exit()
                else:
                    print("生成したansysファイルには'SOLVE'が含まれています．")


    def check_write_ansys_file_main(self):
        self.base_path()
        self.find_solve()
        self.distance_time_length()