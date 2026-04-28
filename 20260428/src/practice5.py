import sqlite3

conn = sqlite3.connect('test.db')
cur = conn.cursor()

# WHERE句を使ってフィルタリング
# セキュリティのため、本来は ? を使うのが実務上の定石
name_to_search = "Tanaka"

#以下にSQL文を記述

results = cur.fetchall()
for row in results:
    print(f"TanakaさんのID: {row[0]}")

# 接続を必ず切ること
