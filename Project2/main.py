import os
from pathlib import Path
from config.theme import Theme
from app.ui.view import MainView
from app.ui.controller import MainController
from app.services import FinanceService

def setup_directories():
    """アプリ実行に必要なディレクトリ構造を事前に作成する"""
    dirs = [
        Path("data/expense"),
        Path("data/revenue"),
        Path("log"),
        Path("config")
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Directory checked/created: {d}")

def main():
    setup_directories()
    view = MainView()
    service = FinanceService()
    controller = MainController(view, service)
    print("Application starting...")
    view.mainloop()

if __name__ == "__main__":
    main()