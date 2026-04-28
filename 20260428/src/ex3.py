import json

data = {"name": "Teacher", "id": 101, "skills": ["Python", "NumPy"]}

# PythonオブジェクトをJSON文字列に変換 (保存)
json_str = json.dumps(data, indent=4)

# JSONファイルを読み込む
# with open('config.json', 'r') as f:
#     data = json.load(f)
print(json_str)