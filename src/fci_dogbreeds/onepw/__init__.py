"""init file for 1Password functions."""

import logging
import os
import sys
from importlib.metadata import PackageNotFoundError, version
from typing import ClassVar

from dotenv import load_dotenv

load_dotenv(override=True)

__project__ = "get_breeds"

try:
    __version__ = version(__project__)
except PackageNotFoundError:
    # This happens when the package is not yet installed locally
    __version__ = "0.0.0-dev"

# ... (Keep your existing imports and dotenv logic above exactly the same) ...

DEFAULT_LOG_FILES = [f"{__project__}.log", f"{__project__}-debug.log"]
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class _ColorFormatter(logging.Formatter):
    LEVEL_STYLES: ClassVar[dict[str, str]] = {
        "DEBUG": "\x1b[34m",
        "INFO": "\x1b[32m",
        "WARNING": "\x1b[33m",
        "ERROR": "\x1b[31m",
        "CRITICAL": "\x1b[41;97m",
    }
    RESET = "\x1b[0m"

    def format(self, record: logging.LogRecord) -> str:
        # Create a copy of the levelname to prevent modifying the
        # original record (this keeps the log files clean!)
        orig_levelname = record.levelname
        color = self.LEVEL_STYLES.get(orig_levelname, "")

        # Apply color only when formatting this specific string
        record.levelname = f"{color}{orig_levelname}{self.RESET}"
        result = super().format(record)

        # Immediately restore the original for the next handlers (the FileHandlers)
        record.levelname = orig_levelname
        return result


def _resolve_log_files() -> list[str]:
    """Reads the log files from the environment.

    Example in .env: GETBREED_LOG=output.log, troubleshooting.log
    """
    env_value = os.getenv("GETBREED_LOG_FILES", "").strip()
    if not env_value:
        return DEFAULT_LOG_FILES[:]

    # Split the comma-separated list and strip any spaces around the names
    files = [part.strip() for part in env_value.split(",") if part.strip()]
    return files if files else DEFAULT_LOG_FILES[:]


def _default_log_level() -> int:
    level = os.getenv("GETBREED_LOG_LEVEL", DEFAULT_LOG_LEVEL).strip().upper()
    if level.isdigit():
        return int(level)
    return getattr(logging, level, logging.INFO)


def _configure_logger() -> logging.Logger:
    # Get the ROOT logger so all submodules automatically benefit
    root_logger = logging.getLogger()

    if root_logger.handlers:
        return logging.getLogger("gdrive-fetch")

    # ALWAYS set the root logger base to DEBUG, so nothing is filtered too early
    root_logger.setLevel(logging.DEBUG)

    # 1. Console Handler (Standard output for the user)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(_default_log_level())
    console_handler.setFormatter(
        _ColorFormatter(DEFAULT_LOG_FORMAT, DEFAULT_DATE_FORMAT)
    )
    root_logger.addHandler(console_handler)

    # 2. File Handlers (Dynamically built based on the environment)
    for file_path in _resolve_log_files():
        try:
            file_handler = logging.FileHandler(file_path, encoding="utf-8")

            # Smart filter: if 'debug' is in the filename, log everything.
            # Otherwise filter at the regular INFO level.
            if "debug" in file_path.lower():
                file_handler.setLevel(logging.DEBUG)
            else:
                file_handler.setLevel(logging.INFO)

            file_handler.setFormatter(
                logging.Formatter(DEFAULT_LOG_FORMAT, DEFAULT_DATE_FORMAT)
            )
            root_logger.addHandler(file_handler)
        except OSError as e:
            # Prevent the entire application from crashing if a log path (e.g. in a test) is not
            # writable
            sys.stderr.write(f"Warning: Could not create log file '{file_path}': {e}\n")

    # Return a specific logger for your module to work with
    return logging.getLogger("gdrive-fetch")


logger = _configure_logger()

__all__ = ["logger"]
