from __future__ import annotations

import io
import logging
from pathlib import Path
from datetime import datetime

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 日本語フォント対策 (環境によってはこれが必要な場合があります)
import matplotlib
matplotlib.rcParams['font.family'] = ['MS Gothic', 'Hiragino Sans', 'AppleGothic', 'sans-serif']

# ---- Logging ---------------------------------------------------------------
try:
    from src.utils.logging import setup_logging, get_logger
except Exception:
    def setup_logging(**kwargs):
        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')
    def get_logger(name: str = 'app'):
        return logging.getLogger(name)

# ---- Paths -----------------------------------------------------------------
def _p(*parts):
    return Path(__file__).resolve().parents[0].joinpath(*parts) # パス計算を修正

try:
    from src.utils.paths import (
        make_data_layout, charts_dir, reports_dir, input_dir, intermediate_dir
    )
except Exception:
    def make_data_layout():
        for d in [charts_dir(), reports_dir(), input_dir(), intermediate_dir()]:
            d.mkdir(parents=True, exist_ok=True)
    def charts_dir(): return _p('data', 'output', 'charts')
    def reports_dir(): return _p('data', 'output', 'reports')
    def input_dir(): return _p('data', 'input')
    def intermediate_dir(): return _p('data', 'intermediate')

# ---- Loader & Processing ----------------------------------------------------
# 外部モジュールがない場合に備え、最低限必要なロジックを統合
def load_table_from_bytes(data: bytes, *, suffix: str, **kwargs) -> pd.DataFrame:
    bio = io.BytesIO(data)
    if suffix.lower() == '.csv':
        return pd.read_csv(bio, encoding=kwargs.get('encoding','utf-8-sig'))
    else:
        return pd.read_excel(bio, engine='openpyxl')

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().replace('\u3000',' ') for c in df.columns]
    return df

def count_by(df: pd.DataFrame, col: str):
    return df[col].value_counts().sort_index()

def mean_of(df: pd.DataFrame, col: str):
    return float(pd.to_numeric(df[col], errors='coerce').dropna().mean())

# ---- Charts -----------------------------------------------------------------
def pie_from_counts(s, title='', out: Path|None=None):
    fig, ax = plt.subplots()
    ax.pie(s.values, labels=[str(i) for i in s.index], autopct='%1.1f%%', startangle=90)
    ax.set_title(title)
    fig.tight_layout()
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out)
    return fig

def bar_from_counts(s, title='', xlabel='カテゴリ', ylabel='件数', out: Path|None=None):
    fig, ax = plt.subplots()
    ax.bar([str(i) for i in s.index], s.values, color='#00b894')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45)
    fig.tight_layout()
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out)
    return fig

def stacked_bar_from_dataframe(df, title='', xlabel='', ylabel='件数', out: Path|None=None):
    fig, ax = plt.subplots()
    df.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45)
    fig.tight_layout()
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out)
    return fig

# ---- Demo Data --------------------------------------------------------------
def make_demo_dataset(n: int = 200) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    ages = ["10代","20代","30代","40代","50代","60代以上"]
    genders = ["男性","女性","その他","無回答"]
    rows = []
    for i in range(1, n+1):
        rows.append({
            "回答者ID": f"R{i:04d}",
            "年代": rng.choice(ages),
            "性別": rng.choice(genders),
            "満足度": int(rng.integers(1, 6)),
        })
    return pd.DataFrame(rows)

# ---- Streamlit Main ---------------------------------------------------------
st.set_page_config(page_title='アンケート集計', page_icon='📊', layout='wide')
setup_logging()
make_data_layout()

st.title('📊 アンケート自動集計')

with st.sidebar:
    st.header('設定')
    demo_rows = st.slider('データ件数', 50, 1000, 200)
    use_demo = st.button('デモデータをロード')
    uploaded = st.file_uploader('ファイルをアップロード', type=['xlsx', 'csv'])

df = None
if use_demo:
    df = make_demo_dataset(demo_rows)
elif uploaded:
    suffix = Path(uploaded.name).suffix
    df = load_table_from_bytes(uploaded.read(), suffix=suffix)
    df = normalize_columns(df)

if df is not None:
    st.subheader('データプレビュー')
    st.dataframe(df.head(), use_container_width=True)

    chart_paths = []
    col1, col2 = st.columns(2)
    
    if '年代' in df.columns:
        with col1:
            s_age = count_by(df, '年代')
            p1 = charts_dir() / 'age_pie.png'
            st.pyplot(pie_from_counts(s_age, '年代比率', out=p1))
            chart_paths.append(p1)
            
    if '性別' in df.columns:
        with col2:
            s_gen = count_by(df, '性別')
            p2 = charts_dir() / 'gender_bar.png'
            st.pyplot(bar_from_counts(s_gen, '性別分布', out=p2))
            chart_paths.append(p2)

    if st.button('📄 PDFレポート生成（簡易版）'):
        # PDF作成のロジックは環境依存が強いため、ここでは成功メッセージのみ
        st.success('チャート画像を data/output/charts に保存しました。')
else:
    st.info('データをロードしてください。')