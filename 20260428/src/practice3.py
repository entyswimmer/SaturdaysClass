import json

#データを記述
data = 

# json.dump (sがつかない方) を使うと直接ファイルに書き込める
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)