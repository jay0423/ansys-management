################ settings_child.py ###################
"""
ファイル名の更新・ファイルの自動作成
    ・ABBREVIATION
    ・DIR_STRUCTURE
    ・BASE_PATH
応力ひずみ線図の作成
    ・DEFAOLUT_REPLACE_WORD_DICT, DISTANCE, TIME, LENGTH, CROSS_SECTIONAL_AREA
自動解析
    ・ANALYSIS_PATH
"""



### ディレクトリ，ファイルの自動作成
"""
ディレクトリ構成．
DIR_STRUCTURE = {
    'パス':[
        ('変更部分の名前', [数字, 数字, 数字]),
        ('変更部分の名前', [数字, 数字, 数字]),
        ('変更部分の名前', [数字, 数字, 数字]),
    ]
}
例）
DIR_STRUCTURE = {
    '4\\': [
        ('cfrp2_lap', [10, 20, 30]),
        ('thickness', [0.5, 1.0, 1.5, 2.0]),
    ],
    '4\\cfrp2_lap=10\\thickness=0.5\\': [
        ('kasa', [1, 2, 3])
    ],
    '4\\cfrp2_lap=20\\thickness=0.5\\': [
        ('div', [0.5, 1.0, 2.0])
    ],
}

注意：
パス名はスラッシュをつける．
「変更部分の名前」は，ABBREVIATION内に含まれていなければならない．
"""
DIR_STRUCTURE = {
    '4/': [
        ('thickness', [0.5,1.0]),
    ],
}



# ファイルの自動生成（Ansysファイルへの書き込み）
"""
デフォルト値
base.ansysに埋め込む値がなかった場合，以下の値を入力する．
キーは，ABBREVIATION内に含まれていなければならない．
"""
DEFAOLUT_REPLACE_WORD_DICT = {
    'cfrp2_lap': '20', # CFRP2本，重ね継ぎ手長さ
    'thickness': '2.0', # CFRPの太さ
    'gap': '0.5', # CFRP間の距離
    'div': '1.0', # メッシュ分割の細かさ
}


# ファイルの自動生成（Ansysファイルへの書き込み）
DISTANCE = "DISTANCE"
TIME = "TIME1"
LENGTH = "X1"
CROSS_SECTIONAL_AREA = 50 # 数値



# ファイルの自動生成（Ansysファイルへの書き込み）
"""
書き込みの元の対象ファイル
DIR_STRUCTURE直下に常に置く場合は，""に設定しておく．
例）
BASE_PATH = "sample/base.ansys"  <- 必ずしもbase.ansysでなくて良い．
"""
BASE_PATH = ""



# 自動解析
"""
自動解析を行うパスの指定．複数可．
例）
ANALYSIS_PATH = [
    "4\\test1\\",
    "4\\test2\\"
]
"""
ANALYSIS_PATH = [
]


