# src/data/generator.py
from pathlib import Path
import argparse
import random
import pandas as pd

AGES = ["10代", "20代", "30代", "40代", "50代", "60代", "70代"]
GENDERS = ["男性", "女性", "その他"]
SATISFACTION = [1, 2, 3, 4, 5]

def make_dataset(n: int = 200, seed: int | None = 42) -> pd.DataFrame:
    random.seed(seed)
    rows = []
    for i in range(1, n + 1):
        rows.append({
            "回答者ID": f"R{i:04d}",
            "年代": random.choice(AGES),
            "性別": random.choice(GENDERS),
            "満足度": random.choice(SATISFACTION),
            # 必要なら他の項目も追加
            "コスパ満足度": random.choice(SATISFACTION),
            "接客満足度": random.choice(SATISFACTION),
            "利用頻度": random.choice(["毎日", "週3", "週1", "月数回", "ほとんど使わない"]),
            "良かった点": random.choice(["店内がきれい", "スタッフが親切", "価格が妥当", "品揃えが豊富"]),
            "改善してほしい点": random.choice(["価格が高い", "品切れが多い", "待ち時間が長い"]),
        })
    return pd.DataFrame(rows)

def main():
    ap = argparse.ArgumentParser(description="デモ用アンケートデータ生成")
    ap.add_argument("--rows", type=int, default=200)
    ap.add_argument("--output", type=Path, default=Path("data/input/demo.xlsx"))
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    df = make_dataset(args.rows, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(args.output, index=False, engine="openpyxl")
    print("generated", args.output)

if __name__ == "__main__":
    main()

