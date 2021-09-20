
### OS
# mac または windows
OS = "mac"



### make_stress_strain.MakeStressStrain
PATH_FILE_NAME = "path.xlsx"




### Refresh
# ファイル名をルール通りに作成する対象ファイルの拡張子
FILE_EXTENSION = [
    "ansys",
    "csv"
]


# ディレクトリ名の略称の定義
# 「=」がない場合はそのまま，ある場合は「=」より左側を入力
ABBREVIATION = {
    'CFRP0': 'C0', # CFRPなし
    'CFRP1': 'C1', # CFRP1本
    'CFRP2_lap': 'C2_l', # CFRP2本，重ね継ぎ手長さ
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
    'CFRP': 'CFRP',
    'epoxy': 'epoxy',
    'PLA': 'PLA',
}


# ファイル名を変更しないファイルリスト
OMISSION = [
    'base.ansys'
]





### MakeFiles

DIR_STRUCTURE = {
    '2/': [
        ('CFRP2_lap', [10, 20, 30, 40]),
        ('thickness', [0.5, 1.0, 1.5, 2.0]),
    ],
    '3/': [
        ('CFRP2_lap', [10, 20, 30]),
        ('thickness', [0.5, 1.0, 1.5, 2.0]),
    ],
}




### WriteAnsysFile

# 書き込みの元の対象ファイル
# DIR_STRUCTURE直下に常に置く場合は，""に設定しておく．
BASE_PATH = ""

# デフォルトの書き込みの元の対象ファイル名（BASE_PATH==""の時），特に変更する必要はない．
BASE_FILE_NAME = "base"

# 書き込み対象の拡張子
WRITE_EXTENSION = "ansys"


# デフォルト値
DEFAOLUT_REPLACE_WORD_DICT = {
    'CFRP2_lap': '20', # CFRP2本，重ね継ぎ手長さ
    'thickness': '2.0', # CFRPの太さ
    'gap': '0.5', # CFRP間の距離
    'div': '1.0', # メッシュ分割の細かさ
}
