# ansysmanagement

#### Ansys Mechanical APDL
#### 本ライブラリを用いれば，複数のAnsys解析・結果の作成を自動的に行うことを可能にし，Ansys解析の効率を大幅に向上させることができます．
#### 具体的には以下３つの機能を持っています．
  - Ansysのディレクトリ構成管理・ファイルの自動生成
  - 自動解析
  - 応力ーひずみ線図の生成

---

### Ansysのディレクトリ構成管理・ファイルの自動生成
  ここで定めるルールに従い，ディレクトリとファイルを自動生成します．特にansysファイルにおいては，変更したい数値の部分を自動で埋め込み，作成してくれます．


### 自動解析
  Ansys Mechanical APDLのAPIを利用し，解析を自動的に行います．ansysを実行する際，複数のパラメータを変更させて解析を行いたい場合があると思います．
  手動の場合，一つ一つのパラメータを変更させて解析を行うため，解析が終わるごとに解析の設定をし直さなければならず，とても非効率です．
  そこで，本ライブラリを用いることで，自動的に複数の解析を一気に行い，無駄な時間を省くことができます．


### 応力ーひずみ線図の生成
  解析結果のcsvファイルから，応力ひずみ線図を自動的に生成し，一つのエクセルファイルにまとめます．


## ソフトウェアバージョン ・ Pythonライブラリ
  - Visual Studio Code推奨（.ansys拡張子の拡張機能があるため）
  - Ansys Mechanical APDL 17.2以降
  - Python 3.8.8
  - IPython 7.22.0
  - [ansys-mapdl-core](https://mapdldocs.pyansys.com/getting_started/running_mapdl.html)（IPython上でpipからinstall）
  - pandas
  - numpy


## Set Up
上記ソフトウェア，ライブラリをpipあるいはcondaによってインストールします．
```bash
git clone "https://github.com/jay0423/ansys_management.git"
ipython ansys_management/start.py
```


## 使用方法
###### 詳しくはMANUAL.mdを参照してください．
初期設定完了後，以下の手順により，処理を実行することができます．
  - ```settings_child.py```にて設定を完了させる．
  - 下記コマンドをコマンドプロンプトで実行する．
```bash
ipython ansys_managemet.py
```


## 注意点
- Ansys Mechanical APDLを複数バージョンインストールしているとき，自動解析が行われずエラーが生じてしまう可能性があります．
複数インストールしている場合，コマンドプロンプトからipythonを起動し，以下コマンドを打ち込み，表示されるAnsysバージョンとライセンスを取得しているAnsysバージョンが一致していることを必ず確認してください．

```ipython
from ansys.mapdl.core import launch_mapdl
mapdl = launch_mapdl()
print(mapdl.version)
```

ライセンスを取得しているものとバージョンが一致していない場合，そのAnsysはアンインストールしてください．

- python3.6, python3.7, python3.8にのみ対応しています．
最新のanacondaはpython3.9をインストールしてしまうため，古いバージョンをインストールするか，anacondaのbase(root)におけるpythonバージョンを下げる必要があります．

- NPROCのコア数を上げすぎると動かなくなります．４以下推奨
