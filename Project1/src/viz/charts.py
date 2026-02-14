# src/viz/charts.py
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional, Sequence

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from .themes import use_default_theme

# 既定テーマ（ダーク表示・保存は白背景）を適用
use_default_theme()

# アクセントカラー（UIと統一したい場合はここを変更）
ACCENT = "#00b894"
PALETTE = sns.color_palette([ACCENT])


# ────────────────────────────────────────────────────────────────────────────────
# ヘルパ
# ────────────────────────────────────────────────────────────────────────────────

def _ensure_str_index(series: pd.Series) -> pd.Series:
    """index を文字列化（日本語カテゴリの安定表示のため）"""
    s = series.copy()
    s.index = [str(i) for i in s.index]
    return s

def _safe_ylim(ax, values: Iterable[float], pad_ratio: float = 1.15) -> None:
    """棒グラフの上限を安全に設定（0件ばかりの時の見栄え対策）"""
    vals = list(values)
    vmax = max(vals) if vals else 0
    ax.set_ylim(0, vmax * pad_ratio if vmax > 0 else 1)

def _save_fig(fig: plt.Figure, out: Optional[Path]) -> None:
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out)


# ────────────────────────────────────────────────────────────────────────────────
# 円グラフ
# ────────────────────────────────────────────────────────────────────────────────

def pie_from_counts(
    series: pd.Series,
    title: str = "",
    out: Optional[Path] = None,
    autopct: str = "%1.1f%%",
    startangle: int = 90,
) -> plt.Figure:
    """
    件数 Series を円グラフにする。
    - series.index: ラベル、series.values: 件数
    - 日本語ラベル対応
    """
    s = _ensure_str_index(series.dropna())
    fig, ax = plt.subplots()
    ax.pie(s.values, labels=s.index, autopct=autopct, startangle=startangle)
    ax.set_title(title)
    ax.axis("equal")  # 真円
    fig.tight_layout()
    _save_fig(fig, out)
    return fig


def donut_from_counts(
    series: pd.Series,
    title: str = "",
    out: Optional[Path] = None,
    autopct: str = "%1.1f%%",
    startangle: int = 90,
    width: float = 0.35,
) -> plt.Figure:
    """
    ドーナツ（穴あき）円グラフ。中央に空白を作って情報量の多い凡例でも見やすく。
    """
    s = _ensure_str_index(series.dropna())
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        s.values, labels=s.index, autopct=autopct, startangle=startangle, wedgeprops=dict(width=1.0)
    )
    # ドーナツ化：内側に白円を重ねる
    circle = plt.Circle((0, 0), 1.0 - width, color="white")
    ax.add_artist(circle)
    ax.set_title(title)
    ax.axis("equal")
    fig.tight_layout()
    _save_fig(fig, out)
    return fig


# ────────────────────────────────────────────────────────────────────────────────
# 棒グラフ（単変量）
# ────────────────────────────────────────────────────────────────────────────────

def bar_from_counts(
    series: pd.Series,
    title: str = "",
    xlabel: str = "カテゴリ",
    ylabel: str = "件数",
    out: Optional[Path] = None,
    color: str = ACCENT,
    rotation: int = 20,
) -> plt.Figure:
    """
    件数 Series を棒グラフで表示。
    """
    s = _ensure_str_index(series)
    fig, ax = plt.subplots()
    sns.barplot(x=s.index, y=s.values, ax=ax, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    _safe_ylim(ax, s.values)
    plt.xticks(rotation=rotation)
    fig.tight_layout()
    _save_fig(fig, out)
    return fig


def bar_from_percent(
    series: pd.Series,
    title: str = "",
    xlabel: str = "カテゴリ",
    ylabel: str = "割合(%)",
    out: Optional[Path] = None,
    color: str = ACCENT,
    rotation: int = 20,
) -> plt.Figure:
    """
    割合 Series を棒グラフで表示。
    """
    s = _ensure_str_index(series)
    fig, ax = plt.subplots()
    sns.barplot(x=s.index, y=s.values, ax=ax, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, 100)
    plt.xticks(rotation=rotation)
    fig.tight_layout()
    _save_fig(fig, out)
    return fig


# ────────────────────────────────────────────────────────────────────────────────
# 棒グラフ（グループ集計）
# ────────────────────────────────────────────────────────────────────────────────

def bar_group_mean(
    series_mean: pd.Series,
    title: str = "",
    xlabel: str = "グループ",
    ylabel: str = "平均",
    out: Optional[Path] = None,
    color: str = ACCENT,
    rotation: int = 0,
) -> plt.Figure:
    """
    groupby した平均値 Series を棒グラフに。
    例：mean_by(df, "年代", "満足度") の返り値を渡す。
    """
    s = _ensure_str_index(series_mean)
    fig, ax = plt.subplots()
    sns.barplot(x=s.index, y=s.values, ax=ax, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    _safe_ylim(ax, s.values)
    plt.xticks(rotation=rotation)
    fig.tight_layout()
    _save_fig(fig, out)
    return fig


def stacked_bar_from_dataframe(
    df_counts: pd.DataFrame,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "件数",
    out: Optional[Path] = None,
    palette: Optional[Sequence[str]] = None,
    rotation: int = 0,
) -> plt.Figure:
    """
    クロス集計（件数）の DataFrame を積み上げ棒グラフにする。
    行が x 軸、列がカテゴリになる想定。
    例：crosstab_counts(df, "年代", "性別") を渡す。
    """
    if palette is None:
        # 列数に合わせてシーケンシャルな色を生成（アクセントを基点）
        # seaborn の deep で十分見やすい配色を使用
        palette = sns.color_palette("deep", n_colors=df_counts.shape[1])

    fig, ax = plt.subplots()
    bottom = None
    for i, col in enumerate(df_counts.columns):
        values = df_counts[col].values
        ax.bar(df_counts.index.astype(str), values, bottom=bottom, label=str(col), color=palette[i])
        bottom = values if bottom is None else (bottom + values)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=rotation)
    ax.legend(title="カテゴリ", bbox_to_anchor=(1.02, 1.0), loc="upper left")
    fig.tight_layout()
    _save_fig(fig, out)
    return fig
