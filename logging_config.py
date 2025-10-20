"""Centralized logging configuration for PrismQ modules.

This module provides comprehensive logging capabilities including:
- Module identification and metadata logging
- System and environment information logging
- Structured logging with consistent formatting
- Support for both console and file logging
- Environment-specific configuration
"""

import logging
import os
import platform
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

try:
    import psutil
except ImportError:
    psutil = None

# Load environment variables
load_dotenv()


class ModuleLogger:
    """Enhanced logger with module metadata and system information.

    This class provides structured logging with automatic inclusion of:
    - Module name and version
    - Module location (file path)
    - Operating system and Python version
    - Hardware information
    - Environment (development/production)
    - Timestamp and log level
    """

    def __init__(
        self,
        module_name: str,
        module_version: str = "0.1.0",
        module_path: str | None = None,
    ) -> None:
        """Initialize the module logger.

        Args:
            module_name: Name of the module (e.g., 'PrismQ.IdeaCollector')
            module_version: Version of the module (default: '0.1.0')
            module_path: Path to module (default: current file location)
        """
        self.module_name = module_name
        self.module_version = module_version
        self.module_path = module_path or str(Path.cwd())

        # Get logging configuration from environment
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.log_file = os.getenv("LOG_FILE")
        self.app_env = os.getenv("APP_ENV", "development")

        # Initialize logger
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up the logger with appropriate handlers and formatters.

        Returns:
            Configured logger instance.
        """
        logger = logging.getLogger(self.module_name)
        logger.setLevel(getattr(logging, self.log_level, logging.INFO))

        # Remove existing handlers to avoid duplicates
        logger.handlers.clear()

        # Create formatter with detailed information
        formatter = logging.Formatter(
            fmt=(
                "%(asctime)s - %(name)s - %(levelname)s - "
                "[%(filename)s:%(lineno)d] - %(message)s"
            ),
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (if configured)
        if self.log_file:
            log_path = Path(self.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_path, encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    def log_module_startup(self) -> None:
        """Log comprehensive module startup information.

        Logs module identity, system information, and environment details.
        """
        separator = "=" * 80
        self.logger.info(separator)
        self.logger.info("MODULE STARTUP")
        self.logger.info(separator)

        # Module information
        self.logger.info("Module Information:")
        self.logger.info(f"  Name: {self.module_name}")
        self.logger.info(f"  Version: {self.module_version}")
        self.logger.info(f"  Location: {self.module_path}")
        self.logger.info(f"  Environment: {self.app_env}")

        # System information
        self.logger.info("System Information:")
        self.logger.info(f"  Operating System: {platform.system()} {platform.release()}")
        self.logger.info(f"  Platform: {platform.platform()}")
        self.logger.info(f"  Architecture: {platform.machine()}")
        self.logger.info(f"  Processor: {platform.processor() or 'Unknown'}")
        self.logger.info(f"  Python Version: {platform.python_version()}")
        self.logger.info(f"  Python Implementation: {platform.python_implementation()}")

        # Runtime information
        self.logger.info("Runtime Information:")
        self.logger.info(f"  Working Directory: {Path.cwd()}")
        self.logger.info(f"  Python Executable: {sys.executable}")
        self.logger.info(f"  Log Level: {self.log_level}")
        if self.log_file:
            self.logger.info(f"  Log File: {self.log_file}")

        # Hardware information (if available)
        self._log_hardware_info()

        self.logger.info(separator)

    def _log_hardware_info(self) -> None:
        """Log hardware information if available.

        Attempts to log CPU, RAM, and GPU information.
        Gracefully handles missing dependencies.
        """
        if psutil is not None:
            # CPU information
            cpu_count = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)
            self.logger.info(
                f"  CPU: {cpu_count} physical cores, {cpu_count_logical} logical cores"
            )

            # Memory information
            memory = psutil.virtual_memory()
            memory_gb = memory.total / (1024**3)
            self.logger.info(f"  RAM: {memory_gb:.2f} GB total")
        else:
            self.logger.debug("psutil not available - skipping detailed hardware info")

        # GPU information (NVIDIA specific)
        try:
            result = subprocess.run(
                ["/usr/bin/nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    self.logger.info(f"  GPU: {line.strip()}")
        except (FileNotFoundError, subprocess.SubprocessError):
            self.logger.debug("nvidia-smi not available - skipping GPU info")

    def log_module_shutdown(self) -> None:
        """Log module shutdown information."""
        separator = "=" * 80
        self.logger.info(separator)
        self.logger.info(f"MODULE SHUTDOWN: {self.module_name}")
        self.logger.info(separator)

    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance.

        Returns:
            Logger instance for use throughout the module.
        """
        return self.logger


def get_module_logger(
    module_name: str,
    module_version: str = "0.1.0",
    module_path: str | None = None,
    log_startup: bool = True,
) -> logging.Logger:
    """Get a configured logger for a PrismQ module.

    This is the recommended way to initialize logging in PrismQ modules.
    It automatically logs startup information if requested.

    Args:
        module_name: Name of the module (e.g., 'PrismQ.IdeaCollector')
        module_version: Version of the module (default: '0.1.0')
        module_path: Path to module (default: current file location)
        log_startup: Whether to log startup information (default: True)

    Returns:
        Configured logger instance ready for use.

    Example:
        >>> logger = get_module_logger("PrismQ.MyModule", "1.0.0")
        >>> logger.info("Processing started")
        >>> logger.warning("Low memory detected")
        >>> logger.error("Operation failed", exc_info=True)
    """
    module_logger = ModuleLogger(module_name, module_version, module_path)

    if log_startup:
        module_logger.log_module_startup()

    return module_logger.get_logger()


def setup_basic_logging(log_level: str = "INFO") -> None:
    """Set up basic logging for simple use cases.

    This is a simpler alternative to get_module_logger() for cases
    where detailed module information is not needed.

    Args:
        log_level: Logging level (default: 'INFO')
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
