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

了解、Yoshiokaさん！  
ここでは \*\*生徒向けの「平均値・分散などの統計量をアプリに追加する手順書」\*\*を、授業でそのまま配布できるレベルに整理しました。  
コードのどこを編集するか、どのように考えるか、段階的に理解できる構成になっています。

***

# 📘 **アプリ拡張演習：統計量（平均・分散）表示機能の追加**

### ― 手順書 ―

（Project1 / Streamlit アンケート集計アプリ）


# 🎯 **目的**

この演習では、既存のアンケート集計アプリに **統計量（平均・分散・標準偏差など）を追加表示**する機能を実装します。

この課題を通じて：

*   データフレーム（pandas DataFrame）の扱い
*   統計量（mean, var, std）の取得方法
*   Streamlit でのメトリック表示
*   既存コードへの機能追加の流れ

が理解できるようになります。

***

# 📦 **前提**

*   Project1 が手元にある
*   `src/app.py` が動作している
*   `pandas` が使える
*   `src/processing/aggregations.py` を編集できる

***

# 🗂️ **演習の流れ（全体）**

1.  **集計関数を追加する**（aggregations.py に variance, std を追加）
2.  **app.py に統計表示エリアを作る**
3.  **統計量を画面に表示する（st.metric / st.write）**
4.  （発展）複数項目の統計量を DataFrame 表として表示

***

***

# 🧩 **STEP 1：aggregations.py に統計関数を追加**

編集するファイル：

    Project1/src/processing/aggregations.py

### 追加する関数（平均はすでにあるので、分散・標準偏差を追加）

```python
def var_of(df: pd.DataFrame, col: str, *, dropna: bool = True) -> float:
    """数値列の分散を返す"""
    if col not in df.columns:
        raise KeyError(f"列が見つかりません: {col}")
    s = df[col].dropna() if dropna else df[col]
    return float(s.var())

def std_of(df: pd.DataFrame, col: str, *, dropna: bool = True) -> float:
    """数値列の標準偏差を返す"""
    if col not in df.columns:
        raise KeyError(f"列が見つかりません: {col}")
    s = df[col].dropna() if dropna else df[col]
    return float(s.std())
```

***

***

# 🧩 **STEP 2：app.py に「統計量表示」セクションを追加**

編集するファイル：

    Project1/src/app.py

挿入場所：

🔎 **平均満足度を表示している部分の直後に追加**

（元のコード）

```python
if '満足度' in df.columns:
    avg = mean_of(df, '満足度')
    st.metric('平均満足度', f'{avg:.2f} / 5')
```

👇 **ここに追加**

```python
from src.processing.aggregations import var_of, std_of

if '満足度' in df.columns:
    st.markdown("### 統計量（満足度）")

    avg = mean_of(df, '満足度')
    var = var_of(df, '満足度')
    std = std_of(df, '満足度')

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("平均", f"{avg:.2f}")
    col_b.metric("分散", f"{var:.3f}")
    col_c.metric("標準偏差", f"{std:.3f}")
```

***

***

# 🧩 **STEP 3：追加動作の確認**

Streamlit を再起動：

**Windows**

```powershell
./scripts/run_app.ps1
```

**macOS/Linux**

```bash
./scripts/run_app.sh
```

画面に以下の3つのメトリックが表示されれば成功：

*   平均
*   分散
*   標準偏差

***

***

# 📈 **STEP 4（発展課題）：複数列の統計表を自動生成**

生徒に追加課題として出せる内容：

### 例）数値列すべてから統計表を作る

```python
numeric_cols = df.select_dtypes(include='number').columns

stats = []
for c in numeric_cols:
    stats.append({
        "項目": c,
        "平均": mean_of(df, c),
        "分散": var_of(df, c),
        "標準偏差": std_of(df, c),
    })

stats_df = pd.DataFrame(stats)
st.dataframe(stats_df)
```

***

***

# 🎓 **この演習で身につくこと**

*   pandas の統計 API の基礎
    *   `mean()`, `var()`, `std()`

*   Python の例外処理（KeyError）

*   Streamlit の UI 作り（metrics, columns, dataframe）

*   既存コードへの追加改修の仕方

***

# 📝 **先生向け：評価項目の提案**

### 必修

*   mean／var／std の3つが正しく計算される
*   Streamlit 画面に表示される
*   列名チェックが行える（KeyError を避ける）

### 加点

*   表形式（DataFrame）で複数列まとめて表示
*   選択式 UI（例：どの列の統計量を出すかユーザーが選べる）
*   PDF レポートへ統計表を追加した場合

### 発展

*   年代ごとの満足度平均・分散など「グループ別統計」
*   箱ひげ図などの統計可視化を追加
*   コメントの自動生成（例：「若年層は分散が大きい」）

***
