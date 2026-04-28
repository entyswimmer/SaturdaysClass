各セクションの演習問題に対する解答コードをまとめました。教材の「解答編」としてそのままお使いいただけます。

---

## 演習問題：解答コード集

### 【演習1】Loggingの使い方
**問題：** 「ユーザー A がログインしました」というメッセージを `INFO` レベルで `system.log` に出力する設定。

```python
import logging

# system.logに出力する設定
logging.basicConfig(
    filename='system.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

logging.info("ユーザー A がログインしました")
```

---

### 【演習2】エラー・ログの解析
**問題：** 存在しないファイルを `open` しようとした時にエラーをキャッチし、「ファイル不在」というログを残す。

```python
import logging

def open_file_safely(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        # FileNotFoundErrorを具体的に指定するのがベストプラクティス
        logging.error("ファイル不在: " + filename)
        return None

open_file_safely("non_existent.txt")
```

---

### 【演習3】JSON形式
**問題：** 辞書 `{"item": "apple", "price": 150}` を、`data.json` というファイルに保存する。

```python
import json

data = {"item": "apple", "price": 150}

# json.dump (sがつかない方) を使うと直接ファイルに書き込める
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)
```

---

### 【演習4】CSV形式
**問題：** CSVからデータを読み込み、ID（1列目）が「2」の行だけを表示する。

```python
import csv

# テスト用のファイル読み込み
with open('users.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        # row[0]は文字列として読み込まれるため、"2"と比較する
        if row and row[0] == "2":
            print(f"発見：{row}")
```

---

### 【演習5】RDB (sqlite3)
**問題：** `users` テーブルから、名前が "Tanaka" であるデータの ID だけを取得して表示する。

```python
import sqlite3

conn = sqlite3.connect('test.db')
cur = conn.cursor()

# WHERE句を使ってフィルタリング
# セキュリティのため、本来は ? を使うのが実務上の定石
name_to_search = "Tanaka"
cur.execute('SELECT id FROM users WHERE name = ?', (name_to_search,))

results = cur.fetchall()
for row in results:
    print(f"TanakaさんのID: {row[0]}")

conn.close()
```

---

### 解説ワンポイント

1.  **Logging**: `filename` を指定しないとコンソール（画面）に出ます。実務ではファイルに保存するのが基本です。
2.  **Error**: `except Exception:` と書くと何でも捕まえてしまいますが、今回のように `FileNotFoundError` と具体的に書く方が「何が起きたか」を正しく把握できます。
3.  **JSON**: `json.dumps` は「文字列」にするもの、`json.dump` は「ファイル」に書き込むもの。この違いはよく引っかかるので注意です。
4.  **CSV**: `row[0]` が文字列であることに注意させましょう（`if row[0] == 2:` は数値と文字列の比較になるので失敗します）。
5.  **SQLite**: `fetchall()` は結果が「タプルのリスト」になるため、`row[0]` で中身を取り出す必要があることを伝えてあげてください。

---
