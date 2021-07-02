import pandas as pd


SPEED = 0.001 #[m/s]
LENGTH = 0.12 #[m]
CROSS_SECTIONAL_AREA = 48.60 #[mm2]


# dataframeの整理
df = pd.read_csv("20210702.csv")
df = df.iloc[:,0].apply(lambda x: pd.Series(x.split()))
df = df.iloc[2:,:2]
df.columns = ["TIME", "FX"]

def clean(x):
    try:
        return float(x)
    except:
        return None
 
df.loc[:,"TIME"] = df.loc[:,"TIME"].map(clean)
df.loc[:,"FX"] = df.loc[:,"FX"].map(clean)
df = df.dropna(how="any")

# 歪みの追加
df["strain"] = df.loc[:,"TIME"] * SPEED / LENGTH
# 荷重の変換
df["FX"] = df.loc[:,"FX"] * (-1)
# 応力の追加
df["stress"] = df.loc[:,"FX"] / CROSS_SECTIONAL_AREA


#EXCELファイルへ書き出し
df.to_excel("cleaned.xlsx", index=False)

print(df)
