# src/viz/themes.py
from __future__ import annotations

import matplotlib as mpl
from contextlib import contextmanager
from typing import Literal, Dict, Any


# ---- 共通の基本パラメータ -------------------------------------------------------

# 日本語フォントの優先順（OS によって存在チェックされる）
# 先頭から順に利用可能なものが使われる
JP_FONT_STACK = [
    "Hiragino Sans",        # macOS
    "Hiragino Kaku Gothic ProN",  # macOS (一部環境)
    "Yu Gothic",            # Windows
    "Meiryo",               # Windows
    "Noto Sans CJK JP",     # Google/Noto
    "Noto Sans JP",         # Noto (環境による)
    "DejaVu Sans",          # フォールバック
]

BASE_RC: Dict[str, Any] = {
    # 図サイズ・解像度
    "figure.figsize": (6.4, 4.0),
    "figure.dpi": 120,

    # フォント周り
    "font.size": 11,
    "font.family": JP_FONT_STACK,
    "axes.unicode_minus": False,  # マイナス記号を正しく表示

    # 余白やグリッド
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "legend.fontsize": 10,

    # 保存時のデフォルト（PNG など）
    "savefig.dpi": 120,
    "savefig.bbox": "tight",   # 不要な余白を削る
    "savefig.pad_inches": 0.1,
}


# ---- ライト／ダーク テーマ -------------------------------------------------------

LIGHT_RC: Dict[str, Any] = {
    "axes.facecolor": "white",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "text.color": "#222",
    "axes.edgecolor": "#444",
    "axes.labelcolor": "#222",
    "xtick.color": "#222",
    "ytick.color": "#222",
    "grid.color": "#bbb",
    "lines.linewidth": 1.5,
}

DARK_RC: Dict[str, Any] = {
    # 画面上はダークだが、保存は白背景のまま（PDF/Word貼り付け用）
    "axes.facecolor": "#171A21",
    "figure.facecolor": "#171A21",
    "savefig.facecolor": "white",   # ここがポイント：保存は白背景
    "text.color": "#eaeaea",
    "axes.edgecolor": "#e0e0e0",
    "axes.labelcolor": "#eaeaea",
    "xtick.color": "#eaeaea",
    "ytick.color": "#eaeaea",
    "grid.color": "#3a3f4b",
    "lines.linewidth": 1.5,
}


def _apply_rc(rc: Dict[str, Any]) -> None:
    """rcParams をまとめて更新する内部ヘルパ。"""
    mpl.rcParams.update(rc)


def use_theme(mode: Literal["light", "dark"] = "light") -> None:
    """
    テーマを適用する（ライト／ダーク）。
    保存画像は常に白背景になるように設定（報告書向け）。
    """
    _apply_rc(BASE_RC)
    if mode == "dark":
        _apply_rc(DARK_RC)
    else:
        _apply_rc(LIGHT_RC)


def use_default_theme() -> None:
    """
    既定のテーマ（ダーク）を適用。
    Streamlit ダークテーマと自然に馴染む配色。
    """
    use_theme("dark")


def reset_to_mpl_default() -> None:
    """Matplotlib のデフォルトに戻す（必要なら）。"""
    mpl.rcParams.update(mpl.rcParamsDefault)


@contextmanager
def theme_context(mode: Literal["light", "dark"] = "light"):
    """
    一時的にテーマを適用するためのコンテキストマネージャ。
    例：
        with theme_context("light"):
            ... グラフ作成 ...
    """
    rc_backup = mpl.rcParams.copy()
    try:
        use_theme(mode)
        yield
    finally:
        mpl.rcParams.update(rc_backup)