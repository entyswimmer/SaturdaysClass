import modules as ms
import teachers as ta

#メッセージは以下で固定
message = "先生がこのメッセージを解読できたらクリアです!!"

#文字列を数字に変換
m_int = ms.str_to_int(message)

key1 = ta.T_public_key[0]
key2 = ta.T_public_key[1]
key3 = ta.T_secret_key

#暗号化(ms.rsaEnc(平文(int型), 公開鍵1, 公開鍵2)を使用する)
#以下の#を外してコードを完成させてみよう

cryptro = 

#暗号文を出力してみよう

#作成した暗号文を保存
with open('ans3-1.txt', 'w') as file1: 
	print(f"{cryptro}", file=file1)
