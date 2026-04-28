import logging

def division(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError as e:
        logging.error(f"計算エラーが発生しました: {e}")
        return None

# 解析の例：ログファイルを1行ずつ読み込んでエラー数を確認
error_count = 0
with open('app.log', 'r') as f:
    for line in f:
        if "ERROR" in line:
            error_count += 1
print(f"エラー発生回数: {error_count}")