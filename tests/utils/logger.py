"""
HireMatch SDET Automation — Custom Logger Utility
──────────────────────────────────────────────────
Provides structured, colored console logging with file rotation
for test execution traceability. Integrates with pytest for
automatic test-step and assertion logging.

Author: Anirudh Gupta
"""

import os
import logging
import sys
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler

LOGS_DIR = Path(__file__).parent.parent.parent / "reports" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


class ColorFormatter(logging.Formatter):
    """Custom formatter with ANSI colors for terminal readability."""
    
    COLORS = {
        logging.DEBUG: "\033[36m",    # Cyan
        logging.INFO: "\033[32m",     # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",    # Red
        logging.CRITICAL: "\033[91m", # Bright Red
    }
    RESET = "\033[0m"
    BOLD = "\033[1m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        record.colored_levelname = f"{color}{self.BOLD}{record.levelname:<8}{self.RESET}"
        record.colored_msg = f"{color}{record.getMessage()}{self.RESET}"
        return (
            f"[{self.formatTime(record, '%H:%M:%S')}] "
            f"{record.colored_levelname} | "
            f"{record.name:<25} | {record.colored_msg}"
        )


class TestLogger:
    """
    Centralized test logger with console + file output.
    
    Usage:
        from tests.utils.logger import TestLogger
        logger = TestLogger("API.Auth").get()
        
        logger.info("Starting login test")
        logger.step("Sending POST /auth/login")
        logger.assert_pass("Status code is 200")
        logger.assert_fail("Response time > SLA", extra="took 2.3s")
    """
    
    _loggers: dict = {}
    
    def __init__(self, name: str = "HireMatch"):
        self.name = name
        if name not in TestLogger._loggers:
            self._setup(name)
    
    def _setup(self, name: str):
        logger = logging.getLogger(f"hirematch.{name}")
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()
        
        # ─── Console Handler ───
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        console.setFormatter(ColorFormatter())
        logger.addHandler(console)
        
        # ─── File Handler (rotating, 5MB max) ───
        timestamp = datetime.now().strftime("%Y-%m-%d")
        log_file = LOGS_DIR / f"test_run_{timestamp}.log"
        
        file_handler = RotatingFileHandler(
            str(log_file),
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            "[%(asctime)s] %(levelname)-8s | %(name)-25s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        logger.addHandler(file_handler)
        
        TestLogger._loggers[name] = logger
    
    def get(self) -> logging.Logger:
        """Return the configured logger instance."""
        return TestLogger._loggers[self.name]
    
    @staticmethod
    def step(logger: logging.Logger, step_description: str):
        """Log a discrete test step for traceability."""
        logger.info(f"📋 STEP → {step_description}")
    
    @staticmethod
    def assert_pass(logger: logging.Logger, assertion: str, detail: str = ""):
        """Log a passing assertion with optional detail."""
        msg = f"✅ PASS → {assertion}"
        if detail:
            msg += f" | {detail}"
        logger.info(msg)
    
    @staticmethod
    def assert_fail(logger: logging.Logger, assertion: str, detail: str = ""):
        """Log a failing assertion with optional detail."""
        msg = f"❌ FAIL → {assertion}"
        if detail:
            msg += f" | {detail}"
        logger.error(msg)
    
    @staticmethod
    def api_call(logger: logging.Logger, method: str, url: str, status: int, time_ms: float):
        """Log an API call with method, URL, status, and response time."""
        emoji = "✅" if 200 <= status < 400 else "⚠️" if 400 <= status < 500 else "❌"
        logger.info(f"{emoji} {method} {url} → {status} ({time_ms:.0f}ms)")
    
    @staticmethod
    def separator(logger: logging.Logger, title: str = ""):
        """Log a visual separator for test sections."""
        line = "═" * 60
        if title:
            logger.info(f"\n{line}\n  {title}\n{line}")
        else:
            logger.info(line)
