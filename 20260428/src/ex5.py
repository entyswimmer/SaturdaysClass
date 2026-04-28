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