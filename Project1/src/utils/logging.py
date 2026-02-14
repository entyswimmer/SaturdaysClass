# src/utils/logging.py
from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path
from typing import Optional, Literal

from .paths import ensure_dir, project_root


# ─────────────────────────────────────────────────────────────────────────────
# 既定のフォーマット
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_FMT = "[%(levelname)s] %(asctime)s - %(name)s - %(message)s"
DEFAULT_DATEFMT = "%Y-%m-%d %H:%M:%S"

# Streamlit などで多重に初期化されないよう制御用フラグ
__LOGGING_CONFIGURED = False


def _make_console_handler(level: int, fmt: str, datefmt: str) -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
    return handler


def _make_rotating_file_handler(
    filepath: Path,
    level: int,
    fmt: str,
    datefmt: str,
    max_bytes: int = 5 * 1024 * 1024,  # 5MB
    backup_count: int = 3,
    encoding: str = "utf-8",
) -> logging.Handler:
    ensure_dir(filepath.parent)
    handler = logging.handlers.RotatingFileHandler(
        filename=str(filepath),
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding=encoding
    )
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
    return handler


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────
def setup_logging(
    *,
    console_level: int = logging.INFO,
    file_level: Optional[int] = None,
    file_path: Optional[Path] = None,
    fmt: str = DEFAULT_FMT,
    datefmt: str = DEFAULT_DATEFMT,
    root_level: int = logging.INFO,
    reset: bool = False,
) -> None:
    """
    ロギングの全体設定を行う。何度呼んでも安全（基本的に最初の1回でOK）。

    Parameters
    ----------
    console_level : int
        コンソール（標準出力）に出すログレベル。デフォルト INFO。
    file_level : Optional[int]
        ファイルに出すログレベル。None の場合はファイル出力しない。
    file_path : Optional[Path]
        ファイル出力を行う際の保存パス。未指定なら ./logs/app.log。
    fmt : str
        ログのフォーマット。
    datefmt : str
        日付フォーマット。
    root_level : int
        ルートロガーのレベル。
    reset : bool
        True の場合、既存のハンドラをすべて外して再設定。
    """
    global __LOGGING_CONFIGURED

    root_logger = logging.getLogger()
    if reset:
        for h in list(root_logger.handlers):
            root_logger.removeHandler(h)
        __LOGGING_CONFIGURED = False

    if __LOGGING_CONFIGURED:
        # 既に設定済みなら、レベルだけ合わせて早期return
        root_logger.setLevel(root_level)
        return

    root_logger.setLevel(root_level)

    # Console handler
    ch = _make_console_handler(console_level, fmt, datefmt)
    root_logger.addHandler(ch)

    # File handler (optional)
    if file_level is not None:
        if file_path is None:
            file_path = project_root() / "logs" / "app.log"
        fh = _make_rotating_file_handler(file_path, file_level, fmt, datefmt)
        root_logger.addHandler(fh)

    __LOGGING_CONFIGURED = True


def get_logger(name: str = "app") -> logging.Logger:
    """
    任意の名前でロガーを取得。ハンドラの二重付与は行わない。
    例: logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)
    return logger


def set_level(name: str, level: int) -> None:
    """
    指定ロガー（またはルート）のレベルを動的に変更。
    """
    logging.getLogger(name).setLevel(level)