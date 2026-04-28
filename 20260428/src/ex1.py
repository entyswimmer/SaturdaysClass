import logging

# 基本設定：ファイル名、ログレベル（INFO以上）、フォーマット
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("プログラムを開始しました")
logging.warning("注意：設定ファイルが見つかりません")
logging.error("エラー：処理に失敗しました")