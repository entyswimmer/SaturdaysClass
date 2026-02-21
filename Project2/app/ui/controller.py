from tkinter import messagebox
from datetime import datetime

class MainController:
    def __init__(self, view, service):
        self.view = view
        self.service = service
        self.view.btn_add.config(command=self.handle_add)
        self.view.btn_delete_row.config(command=self.handle_delete_row)
        self.view.btn_delete_file.config(command=self.handle_delete_file)
        self.load_current_month_data()

    def load_current_month_data(self):
        now = datetime.now()
        ym = now.strftime("%Y_%m")
        
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)

        for is_rev in [True, False]:
            rows = self.service.get_monthly_data(is_rev, ym)
            for row in rows:
                self.view.tree.insert("", "end", values=row)

    def handle_add(self):
        data = self.view.get_input_data()
        if not data["category"] or not data["amount"]:
            messagebox.showwarning("入力エラー", "必須項目を入力してください。")
            return

        try:
            trans_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
            
            transaction = self.service.add_entry(
                is_revenue=data["is_revenue"],
                trans_data={
                    "date": trans_date,
                    "category": data["category"],
                    "amount": int(data["amount"]),
                    "note": data["note"]
                }
            )
            self.view.tree.insert("", "end", values=transaction.to_list())
            self.view.clear_inputs()
        except ValueError:
            messagebox.showerror("エラー", "日付または金額の形式が不正です。")

    def handle_delete_file(self):
        data = self.view.get_input_data()
        try:
            dt = datetime.strptime(data["date"], "%Y-%m-%d")
            ym = dt.strftime("%Y_%m")
            type_label = "歳入" if data["is_revenue"] else "歳出"

            if messagebox.askyesno("警告", f"{ym}の{type_label}データを全て削除しますか？"):
                self.service.delete_monthly_file(data["is_revenue"], ym)
                
                # UI更新
                for item in self.view.tree.get_children():
                    self.view.tree.delete(item)
                messagebox.showinfo("完了", "ファイルを削除しました。")
        except Exception as e:
            messagebox.showerror("エラー", f"削除失敗: {e}")

    def handle_delete_row(self):
        # 画面上の行削除
        selected = self.view.tree.selection()
        if selected:
            if messagebox.askyesno("確認", "表示を削除しますか？"):
                for s in selected:
                    self.view.tree.delete(s)