import teachers as ta
import modules as ms

with open('ans3-2.txt', 'r') as f:
    lines = f.read().splitlines()
    message = int(lines[0])
    sign = int(lines[1])

ans = ms.rsaSignVerify(message, sign, ta.T_public_key[0], ta.T_public_key[1])

if ans == True:
    print("検証成功")
else:
    print("検証失敗")