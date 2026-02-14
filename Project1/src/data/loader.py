# src/data/loader.py
from __future__ import annotations
from pathlib import Path
from io import BytesIO
from typing import Iterable, Literal
import pandas as pd


ExcelSuffix = Literal[".xlsx", ".xlsm", ".xls"]
CsvSuffix = Literal[".csv"]
SupportedSuffix = ExcelSuffix | CsvSuffix

#CSVの欠損値として扱う文字
DEFAULT_NA_VALUES: list[str] = [
    "", "NA", "N/A", "NaN", "null", "NULL", "-", "--", "無回答"
]

def _ensure_path(p: Path | str) -> Path:
    path = Path(p)
    if not path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {path}")
    return path


def _read_excel(
    source: Path | BytesIO,
    sheet: int | str | None = 0,
    header: int = 0,
    na_values: Iterable[str] = DEFAULT_NA_VALUES,
) -> pd.DataFrame:
    """Excel 読み込み（.xlsx/.xlsm/.xls）"""
    try:
        df = pd.read_excel(
            source,
            sheet_name=sheet,
            header=header,
            engine="openpyxl",  #xlsの場合はxlrdが必要だが、一般には xlsx/xlsm を想定
            na_values=list(na_values),
        )
        
        #sheet_name 指定で単一シートなら DataFrame、複数なら dict になる

        if isinstance(df, dict):  #ユーザーが複数シートを指定した場合
            #ここでは「先頭シートを採用」にします
            first_key = next(iter(df))
            df = df[first_key]
        return df
    except Exception as e:
        raise ValueError(f"Excel 読み込みに失敗しました: {e}") from e


def _read_csv_with_fallback(
    source: Path | BytesIO,
    header: int = 0,
    na_values: Iterable[str] = DEFAULT_NA_VALUES,
    encoding: str | None = None,
) -> pd.DataFrame:
    """CSV を UTF-8-SIG → CP932(Shift_JIS) の順でフォールバックして読む"""
    encodings_to_try = [encoding] if encoding else ["utf-8-sig", "cp932"]
    last_error: Exception | None = None
    for enc in encodings_to_try:
        try:
            return pd.read_csv(
                source,
                header=header,
                encoding=enc,
                na_values=list(na_values),
            )
        except Exception as e:
            last_error = e
    raise ValueError(f"CSV 読み込みに失敗しました（encoding={encodings_to_try}）: {last_error}") from last_error


def load_table(
    path: Path | str,
    *,
    sheet: int | str | None = 0,
    header: int = 0,
    na_values: Iterable[str] = DEFAULT_NA_VALUES,
    encoding: str | None = None,
) -> pd.DataFrame:
    """
    ファイルパスから DataFrame を読み込む。
    - Excel: sheet / header をサポート
    - CSV  : encoding フォールバック（utf-8-sig → cp932）
    """
    p = _ensure_path(path)
    suffix = p.suffix.lower()

    if suffix in (".xlsx", ".xlsm", ".xls"):
        return _read_excel(p, sheet=sheet, header=header, na_values=na_values)

    if suffix == ".csv":
        return _read_csv_with_fallback(p, header=header, na_values=na_values, encoding=encoding)

    raise ValueError(f"未対応の拡張子です: {suffix}")


def load_table_from_bytes(
    data: bytes,
    *,
    suffix: SupportedSuffix,
    sheet: int | str | None = 0,
    header: int = 0,
    na_values: Iterable[str] = DEFAULT_NA_VALUES,
    encoding: str | None = None,
) -> pd.DataFrame:
    """
    バイト列（Streamlit の file_uploader など）から DataFrame を読み込む。
    suffix でファイル種別（.xlsx/.csv など）を指定する。
    """
    bio = BytesIO(data)
    suffix = suffix.lower()  # type: ignore[assignment]

    if suffix in (".xlsx", ".xlsm", ".xls"):
        return _read_excel(bio, sheet=sheet, header=header, na_values=na_values)

    if suffix == ".csv":
        # BytesIO は read_csv でもそのまま読める
        return _read_csv_with_fallback(bio, header=header, na_values=na_values, encoding=encoding)

    raise ValueError(f"未対応の拡張子です: {suffix}")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    列名の軽微な正規化（前後空白の除去・全角空白→半角など）
    日本語列名の保持を前提に、破壊的な正規化は行わない。
    """
    def _norm(s: str) -> str:
        # 前後空白除去 + 全角空白を半角へ
        return s.strip().replace("\u3000", " ")

    df = df.copy()
    df.columns = [_norm(str(c)) for c in df.columns]
    return df