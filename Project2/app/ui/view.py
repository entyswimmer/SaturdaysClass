import tkinter as tk
from tkinter import ttk
from datetime import datetime
from config.theme import Theme

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(Theme.WINDOW_TITLE)
        self.geometry(Theme.GEOMETRY)
        self.configure(bg=Theme.BG_COLOR)

        self._setup_ui()

    def _setup_ui(self):
        # 1. 入力エリア (Frame)
        input_frame = ttk.LabelFrame(self, text="データ入力", padding=Theme.PADDING)
        input_frame.pack(fill="x", padx=10, pady=5)

        # 歳入/歳出 選択
        self.type_var = tk.StringVar(value="revenue")
        ttk.Radiobutton(input_frame, text="歳入", value="revenue", variable=self.type_var).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(input_frame, text="歳出", value="expenses", variable=self.type_var).grid(row=0, column=1, sticky="w")

        # 日付 (デフォルト本日)
        ttk.Label(input_frame, text="日付 (YYYY-MM-DD):").grid(row=1, column=0, sticky="e")
        self.ent_date = ttk.Entry(input_frame)
        self.ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.ent_date.grid(row=1, column=1, padx=5, pady=2)

        # カテゴリー
        ttk.Label(input_frame, text="カテゴリー:").grid(row=2, column=0, sticky="e")
        self.ent_category = ttk.Entry(input_frame)
        self.ent_category.grid(row=2, column=1, padx=5, pady=2)

        # 金額を表示するコードを上の例に従って書いてみよう。(text="金額:"にする)

        # 備考
        ttk.Label(input_frame, text="備考:").grid(row=4, column=0, sticky="e")
        self.ent_note = ttk.Entry(input_frame)
        self.ent_note.grid(row=4, column=1, padx=5, pady=2)

        # 2. ボタンエリア
        btn_frame = ttk.Frame(self, padding=Theme.PADDING)
        btn_frame.pack(fill="x")

        self.btn_add = ttk.Button(btn_frame, text="データ追加")
        self.btn_add.pack(side="left", padx=5)

        self.btn_delete_row = ttk.Button(btn_frame, text="選択行を削除")
        self.btn_delete_row.pack(side="left", padx=5)

        self.btn_delete_file = ttk.Button(btn_frame, text="今月のファイルを削除", style="Danger.TButton")
        self.btn_delete_file.pack(side="right", padx=5)

        # 3. 表示エリア (Treeview)
        table_frame = ttk.Frame(self, padding=Theme.PADDING)
        table_frame.pack(fill="both", expand=True)

        columns = ("date", "category", "amount", "note")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # カラムの見出し設定
        self.tree.heading("date", text="日付")
        self.tree.heading("category", text="カテゴリー")
        self.tree.heading("amount", text="金額")
        self.tree.heading("note", text="備考")

        # カラムの幅調整
        self.tree.column("date", width=100)
        self.tree.column("category", width=100)
        self.tree.column("amount", width=80, anchor="e")
        self.tree.column("note", width=200)

        # スクロールバー
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def get_input_data(self):
        """入力フィールドの値を辞書で返す"""
        return {
            "is_revenue": self.type_var.get() == "revenue",
            "date": self.ent_date.get(),
            "category": self.ent_category.get(),
            "amount": self.ent_amount.get(),
            "note": self.ent_note.get()
        }

    def clear_inputs(self):
        """入力フィールドをリセットする"""
        self.ent_category.delete(0, tk.END)
        self.ent_amount.delete(0, tk.END)
        self.ent_note.delete(0, tk.END)