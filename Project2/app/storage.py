import csv
import os
from pathlib import Path

class Storage:
    BASE_DIR = Path("data")

    # ファイルパスの取得
    @classmethod
    def get_path(cls, type_name: str, year_month: str):
        return cls.BASE_DIR / type_name / f"{type_name}_{year_month}.csv"

    #保存
    @classmethod
    def save(cls, type_name, transaction):
        ym = transaction.date.strftime("%Y_%m")
        path = cls.get_path(type_name, ym)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(transaction.to_list())

    #消去
    @classmethod
    def delete_file(cls, type_name, year_month):
        path = cls.get_path(type_name, year_month)
        if path.exists():
            path.unlink()