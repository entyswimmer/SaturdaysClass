#以下にはmodelsのインポートが不足しています
#Strage()の書き方を真似してみましょう
from .storage import Storage

import csv

class FinanceService:
    @staticmethod
    def add_entry(is_revenue, trans_data):
        transaction = #Transactionクラスを使ってみよう(引数に**をつけること)
        type_name = "revenue" if is_revenue else "expenses"
        #Storageクラスのsaveメソッドを使ってみよう
        return transaction

    @staticmethod
    def delete_monthly_file(is_revenue, year_month):
        type_name = "revenue" if is_revenue else "expenses"
        Storage.delete_file(type_name, year_month)

    
    @staticmethod
    def get_monthly_data(is_revenue, year_month):
        type_name = "revenue" if is_revenue else "expenses"
        path = Storage.get_path(type_name, year_month)
        
        rows = []
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row: rows.append(row)
        return rows