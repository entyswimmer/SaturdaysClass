# Pythonデータ管理・エラーハンドリング入門（45分）

この授業では、外部ライブラリ（Pandas等）を使わずに、Pythonの標準機能だけで実務レベルのデータ処理を行う方法を学びます。

---

## 1. ログを出力する (`logging`)
`print()` ではなく `logging` を使う理由は、**「重要度」**を分けて記録できるからです。

### サンプルコード
```python
import logging

# 基本設定：ファイル名、ログレベル（INFO以上）、フォーマット
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("プログラムを開始しました")
logging.warning("注意：設定ファイルが見つかりません")
logging.error("エラー：処理に失敗しました")
```

### 【演習1】
「ユーザー A がログインしました」というメッセージを `INFO` レベルで、ファイル `system.log` に出力する設定を書いてください。

---

## 2. エラー処理とログ解析
エラーでプログラムを止めないために `try-except` を使い、原因を後で解析できるようにします。

### サンプルコード
```python
def division(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError as e:
        logging.error(f"計算エラーが発生しました: {e}")
        return None

# 解析の例：ログファイルを1行ずつ読み込んでエラー数を確認
error_count = 0
with open('app.log', 'r') as f:
    for line in f:
        if "ERROR" in line:
            error_count += 1
print(f"エラー発生回数: {error_count}")
```

### 【演習2】
存在しないファイルを `open` しようとした時に発生するエラーをキャッチし、「ファイル不在」というログを残すコードを書いてください。

---

## 3. JSON形式の扱い
Webや設定ファイルで最も使われる形式です。Pythonの「辞書型」とほぼ同じ感覚で扱えます。

### サンプルコード
```python
import json

data = {"name": "Teacher", "id": 101, "skills": ["Python", "NumPy"]}

# PythonオブジェクトをJSON文字列に変換 (保存)
json_str = json.dumps(data, indent=4)

# JSONファイルを読み込む
# with open('config.json', 'r') as f:
#     data = json.load(f)
print(json_str)
```

### 【演習3】
辞書 `{"item": "apple", "price": 150}` を、`data.json` というファイルに保存するコードを書いてください。

---

## 4. CSV形式の扱い
Excelでも開ける、表形式データの基本です。

### サンプルコード
```python
import csv

# 書き込み
with open('users.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Name"]) # ヘッダー
    writer.writerow([1, "Alice"])
    writer.writerow([2, "Bob"])

# 読み込み
with open('users.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(f"ID: {row[0]}, 名前: {row[1]}")
```

### 【演習4】
CSVからデータを読み込み、IDが「2」の行だけを表示するプログラムを書いてください。

---

## 5. リレーショナルデータベース (`sqlite3`)
大量のデータを効率よく検索・管理するための仕組みです。Pythonならファイル1つでDBが作れます。

### サンプルコード
```python
import sqlite3

# データベースに接続（ファイルがなければ自動作成）
conn = sqlite3.connect('test.db')
cur = conn.cursor()

# テーブル作成
cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)')

# データ挿入
cur.execute('INSERT INTO users VALUES (1, "Tanaka")')
conn.commit() # 保存を確定

# 検索
cur.execute('SELECT * FROM users')
print(cur.fetchall())

conn.close()
```

### 【演習5】
`users` テーブルから、名前が "Tanaka" であるデータの ID だけを取得して表示してください。

---
