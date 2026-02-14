# src/reporting/pdf_builder.py
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional, Sequence, Mapping

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, PageBreak, Flowable
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen.canvas import Canvas

import pandas as pd


# ============================================================================
# フォント登録（日本語CIDフォント） ※全テキストに適用すること
# ============================================================================
JP_SANS = "HeiseiKakuGo-W5"  # ゴシック
JP_SERIF = "HeiseiMin-W3"    # 明朝

def _ensure_japanese_fonts() -> None:
    """ReportLab に日本語の CID フォントを登録。未登録なら登録する。"""
    try:
        pdfmetrics.getFont(JP_SANS)
    except Exception:
        pdfmetrics.registerFont(UnicodeCIDFont(JP_SANS))
    try:
        pdfmetrics.getFont(JP_SERIF)
    except Exception:
        pdfmetrics.registerFont(UnicodeCIDFont(JP_SERIF))


# ============================================================================
# スタイル
# ============================================================================
def _build_styles() -> dict[str, ParagraphStyle]:
    """日本語フォント適用済みの Paragraph スタイル群を生成。"""
    base = getSampleStyleSheet()
    styles: dict[str, ParagraphStyle] = {}

    # 既定（本文）はゴシックを採用
    styles["Body"] = ParagraphStyle(
        "Body",
        parent=base["Normal"],
        fontName=JP_SANS,
        fontSize=10.5,
        leading=14,         # 行送り
        spaceAfter=6,
        textColor=colors.black,
    )
    styles["Small"] = ParagraphStyle(
        "Small", parent=styles["Body"], fontSize=9, leading=12, spaceAfter=4
    )
    styles["H1"] = ParagraphStyle(
        "H1", parent=styles["Body"], fontName=JP_SANS, fontSize=18,
        leading=22, spaceAfter=10
    )
    styles["H2"] = ParagraphStyle(
        "H2", parent=styles["Body"], fontName=JP_SANS, fontSize=14,
        leading=18, spaceAfter=8
    )
    styles["H3"] = ParagraphStyle(
        "H3", parent=styles["Body"], fontName=JP_SANS, fontSize=12.5,
        leading=16, spaceAfter=6
    )
    styles["Caption"] = ParagraphStyle(
        "Caption", parent=styles["Small"], textColor=colors.HexColor("#555")
    )
    return styles


# ============================================================================
# ページ装飾（ヘッダー／フッター）
# ============================================================================
def _header_footer(canvas: Canvas, doc: SimpleDocTemplate, title: str, footer_right: str = "") -> None:
    """全ページにページ番号とタイトル（ヘッダー）を描画。"""
    canvas.saveState()
    canvas.setFont(JP_SANS, 9)

    # 余白
    left = doc.leftMargin
    right = doc.pagesize[0] - doc.rightMargin
    top_y = doc.pagesize[1] - doc.topMargin + 8
    bottom_y = doc.bottomMargin - 14

    # ヘッダー：タイトル
    canvas.drawString(left, top_y, title)

    # フッター：ページ番号・右側テキスト
    page_txt = f"{canvas.getPageNumber()}"
    canvas.drawString(left, bottom_y, f"Page {page_txt}")
    if footer_right:
        text_width = canvas.stringWidth(footer_right, JP_SANS, 9)
        canvas.drawString(right - text_width, bottom_y, footer_right)

    canvas.restoreState()


# ============================================================================
# Flowableヘルパ
# ============================================================================
def _sp(h: float = 6) -> Spacer:
    return Spacer(1, h)

def _auto_image(path: Path, max_w: float, max_h: float) -> RLImage:
    """縦横比を維持したまま、最大サイズ内に収める画像 Flowable を返す。"""
    img = RLImage(str(path))
    # ReportLab は画像読み込み後に _width/_height を持つ
    w, h = img.imageWidth, img.imageHeight
    if w <= 0 or h <= 0:
        # 異常時はそのまま返す（ReportLab 側で例外になることも）
        return img
    scale = min(max_w / float(w), max_h / float(h))
    img.drawWidth = w * scale
    img.drawHeight = h * scale
    return img


# ============================================================================
# 表（DataFrame → Table）
# ============================================================================
def dataframe_table(
    df: pd.DataFrame,
    col_widths: Optional[Sequence[float]] = None,
    header_bg: colors.Color = colors.HexColor("#f0f2f6"),
    row_alt_bg: colors.Color = colors.HexColor("#fafafa"),
    font_name: str = JP_SANS,
    font_size: float = 9.5,
    padding: float = 4,
) -> Table:
    """
    pandas.DataFrame を ReportLab Table へ変換してスタイルを適用。
    """
    data = [list(map(str, df.columns))]
    data += [list(map(lambda x: "" if pd.isna(x) else str(x), row)) for _, row in df.iterrows()]

    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    style = TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#222")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [row_alt_bg, colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#c9ced6")),
        ("LEFTPADDING", (0, 0), (-1, -1), padding),
        ("RIGHTPADDING", (0, 0), (-1, -1), padding),
        ("TOPPADDING", (0, 0), (-1, -1), padding),
        ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
    ])
    tbl.setStyle(style)
    return tbl


# ============================================================================
# ビルド関数（カバーページ＋本文）
# ============================================================================
def build_analysis_report(
    out_path: Path,
    *,
    title: str = "アンケート集計レポート",
    subtitle: str | None = None,
    author: str | None = None,
    meta: Optional[Mapping[str, str]] = None,
    overview_kv: Optional[Mapping[str, str | int | float]] = None,
    chart_paths: Optional[Sequence[Path]] = None,
    chart_cols: int = 2,
    tables: Optional[Mapping[str, pd.DataFrame]] = None,
    notes: Optional[Sequence[str]] = None,
    footer_right: str = "Generated by Project1",
) -> Path:
    """
    実用的な PDF レポートを生成する高水準API。
      - カバーページ：タイトル、サブタイトル、メタ情報
      - 本文：概要（Key-Value）、図（グリッド配置）、表（DataFrame）、所見
      - 全ページにページ番号とヘッダー/フッター
    """
    _ensure_japanese_fonts()
    styles = _build_styles()
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # ドキュメント設定
    page_w, page_h = A4
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=18*mm,
        title=title,
        author=author or "",
    )

    story: list[Flowable] = []

    # --- Cover ---
    story.append(Paragraph(title, styles["H1"]))
    if subtitle:
        story.append(Paragraph(subtitle, styles["H2"]))
    if author:
        story.append(_sp(2))
        story.append(Paragraph(f"作成者：{author}", styles["Body"]))

    if meta:
        story.append(_sp(8))
        story.append(Paragraph("メタ情報", styles["H3"]))
        meta_df = pd.DataFrame(list(meta.items()), columns=["項目", "値"])
        story.append(dataframe_table(meta_df, col_widths=[40*mm, 120*mm]))
    story.append(PageBreak())

    # --- Overview (Key-Value) ---
    if overview_kv:
        story.append(Paragraph("概要", styles["H2"]))
        kv_df = pd.DataFrame(
            [{"項目": k, "値": v} for k, v in overview_kv.items()]
        )
        story.append(dataframe_table(kv_df, col_widths=[40*mm, 120*mm]))
        story.append(_sp(8))

    # --- Charts Grid ---
    if chart_paths:
        story.append(Paragraph("グラフ", styles["H2"]))
        max_w = (page_w - doc.leftMargin - doc.rightMargin - (chart_cols - 1) * 6*mm) / chart_cols
        max_h = 60 * mm

        # グリッド配置
        row: list[Flowable] = []
        for i, p in enumerate(chart_paths, start=1):
            if p and Path(p).exists():
                img = _auto_image(Path(p), max_w=max_w, max_h=max_h)
                row.append(img)
            else:
                # 画像が無い場合は空スペーサで占位
                row.append(_sp(max_h))
            # 1行を確定
            if i % chart_cols == 0:
                # 画像を横に並べるため、Table を利用（枠線は消す）
                t = Table([row], colWidths=[max_w]*chart_cols, hAlign="LEFT")
                t.setStyle(TableStyle([("BOX", (0,0), (-1,-1), 0, colors.white)]))
                story.append(t)
                story.append(_sp(6))
                row = []
        if row:
            # 端数がある場合の最終行
            # 足りないカラムは空スペースで埋める
            while len(row) < chart_cols:
                row.append(_sp(max_h))
            t = Table([row], colWidths=[max_w]*chart_cols, hAlign="LEFT")
            t.setStyle(TableStyle([("BOX", (0,0), (-1,-1), 0, colors.white)]))
            story.append(t)
        story.append(_sp(8))

    # --- Tables ---
    if tables:
        story.append(Paragraph("表", styles["H2"]))
        for caption, df in tables.items():
            story.append(Paragraph(caption, styles["H3"]))
            story.append(dataframe_table(df))
            story.append(_sp(6))

    # --- Notes ---
    if notes:
        story.append(Paragraph("所見", styles["H2"]))
        for n in notes:
            story.append(Paragraph(f"・{n}", styles["Body"]))
        story.append(_sp(6))

    # ビルド（ヘッダ/フッタ適用）
    def _on_first_page(c: Canvas, d: SimpleDocTemplate):
        _header_footer(c, d, title, footer_right)

    def _on_later_pages(c: Canvas, d: SimpleDocTemplate):
        _header_footer(c, d, title, footer_right)

    doc.build(
        story,
        onFirstPage=_on_first_page,
        onLaterPages=_on_later_pages
    )
    return out_path


# ============================================================================
# 互換用：最小限のシンプル関数（既存コードからの移行も考慮）
# ============================================================================
def build_simple_report(out_path: Path, title: str, image_paths: Iterable[Path]) -> None:
    """
    以前のサンプル互換：タイトル＋画像並べ（1枚1段）。
    """
    _ensure_japanese_fonts()
    styles = _build_styles()
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=18*mm,
        title=title
    )
    story: list[Flowable] = [Paragraph(title, styles["H1"]), _sp(8)]
    max_w = A4[0] - doc.leftMargin - doc.rightMargin
    max_h = 70 * mm

    for p in image_paths:
        if Path(p).exists():
            story.append(_auto_image(Path(p), max_w=max_w, max_h=max_h))
            story.append(_sp(6))
    doc.build(story, onFirstPage=lambda c, d: _header_footer(c, d, title))