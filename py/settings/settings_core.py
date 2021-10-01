########### settings/settings_core.py ##############

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
    'sample.ansys'
]





# WriteAnsysFile
# BASE_FILE_NAME + "." + WRITE_EXTENSION
# デフォルトの書き込みの元の対象ファイル名（BASE_PATH==""の時），特に変更する必要はない．
BASE_FILE_NAME = "base"

# 書き込み対象の拡張子
WRITE_EXTENSION = "ansys"




### auto_analysis
# 実行ディレクトリパス
PY_DIR_PATH = "C:\\Users\\matlab\\Documents\\ansys-management\\"

# ansysデータの保存先のディレクトリ(windows)
CWD_PATH = "C:\\Users\\matlab\\ansys_kajimoto\\"
