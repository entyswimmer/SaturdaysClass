#homework.py例
def average(data):
    return sum(data) / len(data)

def main(list):
    select = input("1. 平均値を出す\n2. 最大値と最小値を出す\n3. 値の追加\n")
    if select == "1":
        print(average(list))
    elif select == "2":
        print(max(list), min(list))
    elif select == "3":
        value = input("追加する値を入力")
        list.append(value)
        print(list)
    else:
        print("正しい数字を入れてください")

#test
test_data = [92, 60, 75, 82, 59]
main(test_data)