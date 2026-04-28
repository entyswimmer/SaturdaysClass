# Python データ管理・ログ解析 チートシート
---

## 1. ログ管理 (`logging`)
「いつ」「どこで」「何が」起きたかを記録します。

| レベル | 用途 |
| :--- | :--- |
| `DEBUG` | 開発中の細かい動作確認 |
| `INFO` | 正常な動作の記録 |
| `WARNING` | 注意（今は動くが放置すると危険） |
| `ERROR` | エラー発生（一部の処理が失敗） |
| `CRITICAL` | 致命的な不具合（プログラム停止） |

```python
import logging
# 基本設定
logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s [%(levelname)s] %(message)s')
# 実行
logging.info("起動完了")
```

---

## 2. エラー処理と解析
プログラムを落とさず、原因を特定するための構文です。

* **基本構文**:
    ```python
    try:
        # 失敗するかもしれない処理
    except SpecificError as e:
        # エラーが起きた時の処理
    finally:
        # 成功・失敗に関わらず最後に必ず実行
    ```
* **ログ解析の定石**:
    ```python
    # ログからERRORだけを抽出
    with open('app.log', 'r') as f:
        errors = [line for line in f if "ERROR" in line]
    ```

---

## 3. JSON形式
Webや設定ファイルに強い、辞書型の保存形式です。

* **読み書き早見表**:

| 動作 | 関数 | 説明 |
| :--- | :--- | :--- |
| **保存 (File)** | `json.dump(obj, f)` | ファイルに直接書き込む |
| **変換 (String)** | `json.dumps(obj)` | 文字列（テキスト）に変換する |
| **読込 (File)** | `json.load(f)` | ファイルから読み込む |
| **解析 (String)** | `json.loads(s)` | 文字列を辞書型に変換する |

```python
# 美しく保存する（字下げ）
json.dumps(data, indent=4)
```

---

## 4. CSV形式
Excelで開ける、シンプルで軽量な表形式データです。

* **読み込み**:
    ```python
    import csv
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row[0]) # 1列目にアクセス
    ```
* **書き込み**:
    ```python
    with open('out.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name"]) # 1行ずつリストで渡す
    ```

---

## 5. データベース (`sqlite3`)
大量のデータを検索・整理する「小さなプロ仕様」DB。

* **基本の流れ**:
    1.  **接続**: `conn = sqlite3.connect('db.sqlite')`
    2.  **操作役**: `cur = conn.cursor()`
    3.  **実行**: `cur.execute("SQL文")`
    4.  **確定**: `conn.commit()`（更新・挿入時のみ）
    5.  **終了**: `conn.close()`

* **SQL基本コマンド**:
    * `CREATE TABLE テーブル名 (カラム名 型, ...)`
    * `INSERT INTO テーブル名 VALUES (?, ?)`
    * `SELECT * FROM テーブル名 WHERE 条件`

> [!TIP]
> **セキュリティの鉄則** > `execute("... WHERE name = " + user_input)` は禁止！  
> `execute("... WHERE name = ?", (user_input,))` と「プレースホルダ」を使いましょう。

---

### 💡 困った時のチェックリスト
- [ ] **パスは合っているか？**（ファイルが見つからないエラー）
- [ ] **エンコードは大丈夫か？**（WindowsのExcel CSVは `encoding='utf-8-sig'` が必要かも）
- [ ] **データ型は合っているか？**（CSVやJSONから読み込んだ数字は `str` になっていることが多い）

---
