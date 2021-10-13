########### settings/settings_core.py ##############
"""
ファイル名の更新・ファイルの自動作成
    ・DIR_IGNORE
    ・FILE_EXTENSION
    ・OMMISION
    ・BBASE_FILE_NAME
    ・WRITE_EXTENSION
応力ひずみ線図の作成
    ・PATH_FILE_NAME
自動解析
    ・PY_DIR_PATH
    ・CWD_PATH
"""


# 無視するディレクトリリスト
DIR_IGNORE = [
    'etc',
    '__pycache__',
    '.git',
    'py'
]




### make_stress_strain.MakeStressStrain
PATH_FILE_NAME = "path.xlsx"




### Refresh
# ファイル名をルール通りに作成する対象ファイルの拡張子
FILE_EXTENSION = [
    "ansys",
    "csv"
]



# ファイル名を変更しないファイルリスト
OMISSION = [
    'base.ansys',
    'sample.ansys',
    'settings_memo.py',
    'README.md',
    'README.txt'
]





# WriteAnsysFile
# BASE_FILE_NAME + "." + WRITE_EXTENSION
# デフォルトの書き込みの元の対象ファイル名（BASE_PATH==""の時），特に変更する必要はない．
BASE_FILE_NAME = "base"

# 書き込み対象の拡張子
WRITE_EXTENSION = "ansys"




### auto_analysis
# 実行ディレクトリパス
# PY_DIR_PATH = "C:\\Users\\matlab\\Documents\\ansys-management\\"
PY_DIR_PATH = "/Users/jay0423/Documents/GitHub/ansys-management/"

# ansysデータの保存先のディレクトリ(windows)
CWD_PATH = "C:\\Users\\matlab\\ansys_kajimoto\\"



# ディレクトリ名の略称の定義
"""
「=」がない場合はそのまま，ある場合は「=」より左側を入力する．
略称は他と被っては行けない．
大文字禁止
"""
import os
import json
ABBREVIATION = json.load(open(PY_DIR_PATH + os.path.join("py", "settings", "abbreviation.json"), "r"))["ABBREVIATION"]