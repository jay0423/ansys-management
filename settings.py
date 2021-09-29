# 無視するディレクトリリスト
DIR_IGNORE = [
    'etc',
    '__pycache__',
    '.git'
]




### make_stress_strain.MakeStressStrain
PATH_FILE_NAME = "path.xlsx"




### Refresh
# ファイル名をルール通りに作成する対象ファイルの拡張子
FILE_EXTENSION = [
    "ansys",
    "csv"
]


# ディレクトリ名の略称の定義
"""
「=」がない場合はそのまま，ある場合は「=」より左側を入力する．
略称は他と被っては行けない．
大文字禁止
"""
ABBREVIATION = {
    'cfrp0': 'c0', # CFRPなし
    'cfrp1': 'c1', # CFRP1本
    'cfrp2_lap': 'c2_l', # CFRP2本，重ね継ぎ手長さ
    'thickness': 'th', # CFRPの太さ
    'gap': 'g', # CFRP間の距離
    'div': 'd', # メッシュ分割の細かさ
    'kasa': 'kasa', # 傘形状
    ###########################################
    'time_distance': 't', # 引張速度と引張距離
    'correction': 'cor', # 修正バージョン
    'length': 'len', # 試験片長さ
    'solid185': 's185', # solid185
    'solid186': 's186', # solid186
    'cfrp_tensile': 'cfr', # CFRPの強度
    'epo_tensile': 'epo', # epoxyの強度
    'super': 'sup', # その他改良
    'cfrp': 'cfrp',
    'epoxy': 'epoxy',
    'pla': 'pla',
}


# ファイル名を変更しないファイルリスト
OMISSION = [
    'base.ansys'
]





### WriteAnsysFile
### MakeFiles
"""
ディレクトリ構成．
'パス':[
    ('変更部分の名前', [数字, 数字, 数字]),
    ('変更部分の名前', [数字, 数字, 数字]),
    ('変更部分の名前', [数字, 数字, 数字]),
]

注意：
パス名はスラッシュをつける．
「変更部分の名前」は，ABBREVIATION内に含まれていなければならない．
"""
DIR_STRUCTURE = {
    '2/': [
        ('cfrp2_lap', [10, 20, 30, 40]),
        ('thickness', [0.5, 1.0, 1.5, 2.0]),
    ],
    '3/': [
        ('cfrp2_lap', [10, 20, 30]),
        ('thickness', [0.5, 1.0, 1.5, 2.0]),
    ],
    '3/cfrp2_lap=10/thickness=0.5/': [
        ('kasa', [1, 2, 3])
    ],
    'sample/': [
        ('cfrp2_lap', [10, 20]),
        ('thickness', [0.5, 1.0, 1.5]),
    ],
}

# WriteAnsysFile
# 書き込みの元の対象ファイル
# DIR_STRUCTURE直下に常に置く場合は，""に設定しておく．
BASE_PATH = ""

# デフォルトの書き込みの元の対象ファイル名（BASE_PATH==""の時），特に変更する必要はない．
BASE_FILE_NAME = "base"

# 書き込み対象の拡張子
WRITE_EXTENSION = "ansys"


# デフォルト値
"""
base.ansysに埋め込む値がなかった場合，以下の値を入力する．
キーは，ABBREVIATION内に含まれていなければならない．
"""
DEFAOLUT_REPLACE_WORD_DICT = {
    'cfrp2_lap': '20', # CFRP2本，重ね継ぎ手長さ
    'thickness': '2.0', # CFRPの太さ
    'gap': '0.5', # CFRP間の距離
    'div': '1.0', # メッシュ分割の細かさ
}



### auto_analysis
# 実行ディレクトリパス
PY_DIR_PATH = "C:\\Users\\matlab\\Documents\\ansys-management\\"

# ansysデータの保存先のディレクトリ(windows)
CWD_PATH = "C:\\Users\\matlab\\ansys_kajimoto\\"
