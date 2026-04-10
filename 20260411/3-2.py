#modules.pyをmsという名前でインポートする


#自分の鍵ファイルを開き、鍵情報を取得してみよう

message = ms.str_to_int("署名するメッセージ")

#以下の#を外してコードを完成させてみよう

#key1 = 
#key2 = 
#sign = 

with open('ans3-2.txt', 'w') as f: 
    print(f"{message}", file=f)
    print(f"{sign}", file=f)

