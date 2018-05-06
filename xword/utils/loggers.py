import sys
import logging
import logging.handlers

from pythonjsonlogger import jsonlogger


MAX_OLD_LOG_FILES = 7


def get_logger(name, log_level=None):
    """Gets a formatted logger."""
    log_level = log_level or getattr(logging, 'INFO')
    log = logging.getLogger(name)
    if not log.handlers:
        log.propagate = 0
        log.setLevel(log_level)

        # handler = logging.handlers.TimedRotatingFileHandler(
        #     '{}{}'.format(
        #         '/var/log/xword-app/', 'xword.log'
        #     ),
        #     when='midnight',
        #     backupCount=MAX_OLD_LOG_FILES
        # )

        handler = logging.StreamHandler(sys.stdout)

        handler.setFormatter(_create_formatter())
        log.addHandler(handler)
    return log


def _create_formatter():
    supported_keys = [
        'asctime',
        'filename',
        'funcName',
        'levelname',
        'lineno',
        'module',
        'message',
        'name',
        'pathname',
    ]

    custom_format = ' '.join(['%({0:s})'.format(i) for i in supported_keys])
    return jsonlogger.JsonFormatter(custom_format)
