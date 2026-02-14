# Excel操作の自動化
--

## 1. 環境構築

絶対やらなきゃいけないわけではありませんが、gitを使った開発に慣れておくと
プログラミングの仕事をする時に役立ちます。

(難しくてよくわからなかったら手動でファイルをダウンロードでok)


#### 1. 自分のリモートリポジトリを作成
1. GitHubで新しいリポジトリの作成
2. 名前はSaturdaysClassにする
3. README.mdは作成しない
4. .gitignoreはpythonのデフォルトのものを選択
5. 作成を押す

#### 2. リポジトリのクローン
`home/python/`で以下を実行

```powershell
git clone git@github.com:entyswimmer/SaturdaysClass.git
```
#### 3. 仮想環境の作成

**注意**
今回は実行不要だが, 普段はやっておくと良い

```powershell
//仮想環境の作成
py -3.11 venv -m venv .venv

//アクティベート
.\venv\Scripts\activate

//パッケージやライブラリのインストール
pip install -r requirements.txt

//これは全体の作業の終了の時に忘れずにやること(今は不要)
deactivate
```

#### 4. GitHubに接続(以下の順に実行)
```powershell
git remote remove origin

git remote add origin https://github.com/自分のユーザー名/SaturdaysClass.git

git add .

git commit -m "メッセージ"

git push origin main

git pull origin main
```

・作業する前にgit pull origin mainを実行<br>
・作業が終わったらgit push origin mianを実行<br>

-

## 2. 作成するアプリケーション

**アンケート結果を自動でグラフ化＆レポート生成**

アンケート結果の表の例


