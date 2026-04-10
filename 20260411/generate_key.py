import modules as ms

#素数の生成
p = ms.fermat_primegen2(1024, 1)
q = ms.fermat_primegen2(1024, 1)

#公開鍵: public_key, 秘密鍵: secret_key　とする
my_public_key, my_secret_key = ms.rsaKeygen(p, q)

print(f"自分の公開鍵:\n {my_public_key}\n")
print(f"自分の秘密鍵:\n {my_secret_key}\n")

#自分の鍵を保存
with open("my_key.txt", 'w') as f:
    print(f"{my_public_key[0]}", file=f)
    print(f"{my_public_key[1]}", file=f)
    print(f"{my_secret_key}\n", file=f)