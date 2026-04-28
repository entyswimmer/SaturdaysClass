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