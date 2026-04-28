# 2026 04 28 宿題
---

## 次回までに必ずインストールしておくこと

- 次回からはJupyter Notebookを使用します。以下コマンドでインストールしてください。
  
```shell
pip install jupyter
```

- 起動方法は以下のコマンドです
  
```shell
jupyter lab
```

---

## 仮想環境の作成

- 以下のコマンドを順に実行してください。

```shell
sudo apt update

sudo apt install python3-venv

py -m venv venv

//起動する際は以下
.\venv\Script\activate

//必要ライブラリのインストール
python -m pip install numpy jupyter

//終了
deactivate
```

#### 注意事項
1. まずは仮想環境が作成できるようにしてください
2. 不可能だった場合はC:user/owner/Python/にてcursorを起動して以下のプロンプトを入力してください。
```markdown
sample_venvディレクトリを作成して、そこに仮想環境を作成して、numpyをインストールして。
numpyが使えるかの確認コードも作成すること。
```
3. それでも不可能だった場合はグローバル環境にjupyterを入れてください

