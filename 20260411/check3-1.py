import teachers as ta
import modules as ms

with open('ans3-1.txt', 'r') as f: 
	cryptro = int(f.read())


#復号結果チェック
m_int = ms.rsaDec(cryptro, ta.T_public_key[0], ta.T_secret_key)
print(ms.int_to_str(m_int))