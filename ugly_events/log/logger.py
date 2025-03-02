"""log"""

import logging
import logging.config
import pathlib
from .filters import filter_maker # pylint: disable=import-error

SYSTEM_LOG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(module)-8s[%(lineno)3d]: %(levelname)-8s - %(message)s"},
        "detailed": {
            "format": "%(module)8s/%(funcName)8s[%(lineno)3d]: [%(asctime)s] %(levelname)-8s - %(message)s"  # pylint: disable=line-too-long
        },
    },
    "filters": {
        "stdout_fltr": {
            "()": filter_maker,
            "level": "ERROR"
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "detailed",
            "stream": "ext://sys.stdout",
            "filters": ["stdout_fltr"]
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "detailed",
            "stream": "ext://sys.stderr",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": str(pathlib.Path("transient") / "system.log"),
            "mode": "w",
        },
    },
    "loggers": {
        "system": {"level": "DEBUG", "handlers": ["stderr", "stdout", "file"], "propagate": False},
    },
}


logging.config.dictConfig(SYSTEM_LOG)
system = logging.getLogger("system")

debug, info, warning, error, critical = (
    system.debug,
    system.info,
    system.warning,
    system.error,
    system.critical,
)

logging.info("Logging initialized")
