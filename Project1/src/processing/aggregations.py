# src/processing/aggregations.py
from __future__ import annotations

from typing import Iterable, Sequence, Mapping, Literal, Optional
import re
from collections import Counter

import pandas as pd


# ---- ユーティリティ（カテゴリ順の制御） --------------------------------------

def apply_category_order(
    ser: pd.Series,
    order: Optional[Sequence[str]] = None
) -> pd.Series:
    """
    カテゴリ列に「表示順」を適用する。
    order を指定しない場合は元のユニーク順（value_counts()とは独立）。
    """
    s = ser.copy()
    if order is None:
        return s
    s = s.astype(pd.CategoricalDtype(categories=list(order), ordered=True))
    return s


# ---- 単変量の基本集計 -----------------------------------------------------------

def count_by(
    df: pd.DataFrame,
    col: str,
    *,
    dropna: bool = True,
    order: Optional[Sequence[str]] = None
) -> pd.Series:
    """
    カテゴリ列の件数を返す（index=カテゴリ, values=件数）。
    - dropna=True で欠損を除外
    - order を指定すると、その順序で並ぶ
    """
    if col not in df.columns:
        raise KeyError(f"列が見つかりません: {col}")
    s = df[col]
    if dropna:
        s = s.dropna()
    s = apply_category_order(s, order)
    vc = s.value_counts(dropna=not dropna, sort=False)  # 並び順はカテゴリ順に合わせる
    # カテゴリ順が未指定の場合は index 昇順にしておく（日本語でも安定挙動に）
    if order is None:
        vc = vc.sort_index()
    return vc


def percent_by(
    df: pd.DataFrame,
    col: str,
    *,
    digits: int = 1,
    dropna: bool = True,
    order: Optional[Sequence[str]] = None
) -> pd.Series:
    """
    カテゴリ列の割合（%）を返す。合計100%（四捨五入誤差あり）。
    """
    counts = count_by(df, col, dropna=dropna, order=order)
    total = counts.sum()
    if total == 0:
        return counts.astype(float)
    perc = (counts / total * 100).round(digits)
    return perc


def mean_of(df: pd.DataFrame, col: str, *, dropna: bool = True) -> float:
    """数値列の平均を返す。"""
    if col not in df.columns:
        raise KeyError(f"列が見つかりません: {col}")
    s = df[col]
    return float(s.dropna().mean()) if dropna else float(s.mean())


def median_of(df: pd.DataFrame, col: str, *, dropna: bool = True) -> float:
    """数値列の中央値を返す。"""
    if col not in df.columns:
        raise KeyError(f"列が見つかりません: {col}")
    s = df[col]
    return float(s.dropna().median()) if dropna else float(s.median())


def mode_of(df: pd.DataFrame, col: str, *, dropna: bool = True) -> pd.Series:
    """
    最頻値（複数ある場合は複数返る）。返り値は Series。
    """
    if col not in df.columns:
        raise KeyError(f"列が見つかりません: {col}")
    s = df[col].dropna() if dropna else df[col]
    return s.mode()


# ---- グループ集計（クロス集計/平均・割合など） ----------------------------------

def mean_by(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    *,
    order: Optional[Sequence[str]] = None
) -> pd.Series:
    """
    group_col ごとの value_col の平均。
    """
    if group_col not in df.columns or value_col not in df.columns:
        raise KeyError(f"列が見つかりません: {group_col}, {value_col}")
    s_group = apply_category_order(df[group_col], order)
    g = pd.Series(df[value_col].values, index=s_group)
    out = g.groupby(level=0).mean()
    # カテゴリ順が未指定なら index 昇順
    if order is None:
        out = out.sort_index()
    return out


def crosstab_counts(
    df: pd.DataFrame,
    row: str,
    col: str,
    *,
    row_order: Optional[Sequence[str]] = None,
    col_order: Optional[Sequence[str]] = None,
    dropna: bool = True
) -> pd.DataFrame:
    """
    行×列の件数のクロス集計。
    """
    if row not in df.columns or col not in df.columns:
        raise KeyError(f"列が見つかりません: {row}, {col}")
    r = df[row]
    c = df[col]
    if dropna:
        mask = r.notna() & c.notna()
        r = r[mask]
        c = c[mask]
    r = apply_category_order(r, row_order)
    c = apply_category_order(c, col_order)
    tab = pd.crosstab(r, c, dropna=False)
    # 未指定なら index/columns 昇順
    if row_order is None:
        tab = tab.sort_index(axis=0)
    if col_order is None:
        tab = tab.sort_index(axis=1)
    return tab


def crosstab_percent(
    df: pd.DataFrame,
    row: str,
    col: str,
    *,
    normalize: Literal["all", "index", "columns"] = "index",
    digits: int = 1,
    row_order: Optional[Sequence[str]] = None,
    col_order: Optional[Sequence[str]] = None,
    dropna: bool = True
) -> pd.DataFrame:
    """
    行×列の割合のクロス集計。
    normalize:
      - "index": 行内で100%（行方向の割合）
      - "columns": 列内で100%（列方向の割合）
      - "all": 全体100%
    """
    tab = crosstab_counts(
        df, row, col,
        row_order=row_order, col_order=col_order, dropna=dropna
    )
    denom = {
        "index": tab.sum(axis=1).replace(0, pd.NA),
        "columns": tab.sum(axis=0).replace(0, pd.NA),
        "all": tab.values.sum()
    }
    if normalize == "all":
        total = float(denom["all"] or 0.0)
        out = (tab / total * 100) if total > 0 else tab.astype(float)
    elif normalize == "index":
        out = (tab.T / denom["index"]).T * 100
    else:
        out = tab / denom["columns"] * 100
    return out.round(digits)


# ---- Likert（1〜5など）向けの集計 ------------------------------------------------

def likert_summary(
    df: pd.DataFrame,
    col: str,
    *,
    scale: Sequence[int] = (1, 2, 3, 4, 5),
    labels: Optional[Mapping[int, str]] = None,
    digits: int = 1,
) -> pd.DataFrame:
    """
    Likert 尺度（例：1〜5）を想定したサマリー。
    出力：各スコアの件数・割合・平均・中央値
    """
    if col not in df.columns:
        raise KeyError(f"列が見つかりません: {col}")
    s = df[col].dropna()
    # スコア外の値を除外（安全運転）
    s = s[s.isin(scale)]
    counts = s.value_counts().reindex(scale, fill_value=0)
    perc = (counts / counts.sum() * 100).round(digits) if counts.sum() > 0 else counts.astype(float)
    out = pd.DataFrame({
        "件数": counts,
        "割合(%)": perc
    })
    if labels:
        out.index = [labels.get(int(i), str(i)) for i in out.index]
    stats = pd.Series({
        "平均": s.mean() if len(s) else float("nan"),
        "中央値": s.median() if len(s) else float("nan"),
        "回答数": int(len(s)),
    })
    return out, stats


# ---- NPS（推奨度 0〜10） -------------------------------------------------------

def nps(
    df: pd.DataFrame,
    col: str,
    *,
    digits: int = 1
) -> pd.Series:
    """
    NPS（Net Promoter Score）を算出する。
    - 0〜6: Detractors
    - 7〜8: Passives
    - 9〜10: Promoters
    返り値：カテゴリ割合と NPS 値（Promoters% - Detractors%）
    """
    if col not in df.columns:
        raise KeyError(f"列が見つかりません: {col}")
    s = df[col].dropna()
    s = s[s.between(0, 10)]  # 範囲外は除外
    if len(s) == 0:
        return pd.Series({"Promoters(%)": 0.0, "Passives(%)": 0.0, "Detractors(%)": 0.0, "NPS": 0.0})
    promoters = (s >= 9).mean() * 100
    passives = ((s >= 7) & (s <= 8)).mean() * 100
    detractors = (s <= 6).mean() * 100
    result = pd.Series({
        "Promoters(%)": round(promoters, digits),
        "Passives(%)": round(passives, digits),
        "Detractors(%)": round(detractors, digits),
        "NPS": round(promoters - detractors, digits)
    })
    return result


# ---- 自由記述の簡易頻出語 ------------------------------------------------------

_JA_TOKEN_SPLIT = re.compile(r"[\\s、。．,\\.／/・;；:：!！\\?？\\(\\)（）\\[\\]『』「」\"'`]")

def top_terms(
    df: pd.DataFrame,
    col: str,
    *,
    stopwords: Optional[Iterable[str]] = None,
    top_n: int = 20,
    min_len: int = 2
) -> pd.Series:
    """
    日本語の自由記述列からの簡易頻出語トップ。
    * 高度な形態素解析は使わず、空白/句読点/記号で分割するだけの簡易版。
    * 実運用では MeCab や Sudachi を使うと精度が上がる。
    """
    if col not in df.columns:
        raise KeyError(f"列が見つかりません: {col}")

    sw = set(stopwords or [])
    counter: Counter[str] = Counter()

    for v in df[col].dropna().astype(str):
        for token in _JA_TOKEN_SPLIT.split(v):
            t = token.strip()
            if len(t) < min_len:
                continue
            if t in sw:
                continue
            counter[t] += 1

    most = counter.most_common(top_n)
    return pd.Series({k: v for k, v in most})
