# src/utils/paths.py
from __future__ import annotations

from pathlib import Path
import sys
import os
from typing import Optional


# ------------------------------------------------------------------------------
# 実行環境判定（PyInstaller でビルドされたバイナリかどうか）
# ------------------------------------------------------------------------------
IS_FROZEN: bool = getattr(sys, "frozen", False)

def _meipass() -> Optional[Path]:
    """
    PyInstaller の一時展開ディレクトリ（_MEIPASS）を返す。
    バイナリ実行時だけ存在する。
    """
    if IS_FROZEN and hasattr(sys, "_MEIPASS"):
        return Path(getattr(sys, "_MEIPASS"))
    return None


# ------------------------------------------------------------------------------
# プロジェクトルート決定
# ------------------------------------------------------------------------------
def project_root() -> Path:
    """
    プロジェクトのルートディレクトリを返す。

    - 開発時（ソース実行）: このファイルから 2 つ上がルート（…/src/utils/ → ルート）
    - PyInstallerバイナリ: 実行ファイルの親ディレクトリをルートとみなす
      （Windows: app.exe のある場所、macOS: app.app/Contents/MacOS/ の親など）
    """
    if IS_FROZEN:
        # バイナリの場所を基準に（配布物の同梱 assets/data を隣に置く想定）
        return Path(sys.executable).resolve().parent

    # ソース実行時は src/utils/ から 2階層上がルート
    return Path(__file__).resolve().parents[2]


# ------------------------------------------------------------------------------
# リソース取得（assets などを PyInstaller の展開先／プロジェクトから安全に参照）
# ------------------------------------------------------------------------------
def resource_path(relative: str | Path) -> Path:
    """
    配布後（PyInstaller）でも開発時でも、相対パスで同梱リソースを取得する。
    - バイナリ実行時: _MEIPASS（展開先）を優先
    - ソース実行時  : project_root を基準に結合
    """
    rel = Path(relative)
    mp = _meipass()
    if mp:
        p = mp / rel
        if p.exists():
            return p

    # _MEIPASS に無ければ、プロジェクトルートを基準に
    return project_root() / rel


# ------------------------------------------------------------------------------
# 主要ディレクトリ（Project1 の構成に準拠）
# ------------------------------------------------------------------------------
def data_dir() -> Path:
    return project_root() / "data"

def input_dir() -> Path:
    return data_dir() / "input"

def output_dir() -> Path:
    return data_dir() / "output"

def charts_dir() -> Path:
    return output_dir() / "charts"

def reports_dir() -> Path:
    return output_dir() / "reports"

def intermediate_dir() -> Path:
    return data_dir() / "intermediate"

def assets_dir() -> Path:
    return project_root() / "assets"

def fonts_dir() -> Path:
    return assets_dir() / "fonts"

def styles_dir() -> Path:
    return assets_dir() / "styles"


# ------------------------------------------------------------------------------
# ユーティリティ
# ------------------------------------------------------------------------------
def ensure_dir(p: str | Path) -> Path:
    """
    ディレクトリが無ければ作成して Path を返す。
    """
    path = Path(p)
    path.mkdir(parents=True, exist_ok=True)
    return path


def resolve_path(*parts: str | Path) -> Path:
    """
    project_root を起点に、可読性の高い結合を行う。
    例: resolve_path("data", "output", "charts", "age_pie.png")
    """
    return project_root().joinpath(*map(Path, parts))


def make_data_layout() -> None:
    """
    data/output/charts, data/output/reports など、必要な出力先の雛形作成。
    配布直後や初回起動時に呼ぶと安全。
    """
    for d in (data_dir(), input_dir(), output_dir(), charts_dir(), reports_dir(), intermediate_dir()):
        ensure_dir(d)


# ------------------------------------------------------------------------------
# 例：このモジュール単独で動かしたい時の簡易テスト
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("IS_FROZEN:", IS_FROZEN)
    print("project_root:", project_root())
    print("data_dir:", data_dir())
    print("input_dir:", input_dir())
    print("output_dir:", output_dir())
    print("charts_dir:", charts_dir())
    print("reports_dir:", reports_dir())
    # ひな形作成
    make_data_layout()
    print("✔ パスの初期化が完了しました。")
