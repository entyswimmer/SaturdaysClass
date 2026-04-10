import secrets
import hashlib
import string

# 1. パスワードの生成 (16桁のランダム文字列)
# 英数字 + 記号を混ぜる設定
alphabet = string.ascii_letters + string.digits + string.punctuation

#.join関数の引数をalphabetから16文字選ぶように書こう
password = ''.join()

# 2. パスワードのハッシュ化 (SHA-256を使用)
hashed_password = 

#保存
with open("ans3-3.txt", "w") as f:
    print(f"{password}", file=f)
    print(f"{hashed_password}", file=f)