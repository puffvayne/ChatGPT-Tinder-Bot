import logging
import sys
import pathlib
import importlib
from typing import Union, Callable

from .. import var as VAR


class RichLogger:
    def __init__(self, logger: logging.Logger, log_path: Union[pathlib.Path, None]):
        self.logger = logger
        self.log_path = log_path
        if self.log_path is not None:
            self.has_log_file = True
        else:
            self.has_log_file = False
        self.name = self.logger.name
        self.log_lv = self.logger.level
        self.log_lv_name = logging.getLevelName(self.log_lv)

        msg = f"{self} created"
        self.info(msg)
        self.chmod_777_log_file()

    def __repr__(self):
        if self.log_path is not None:
            s = f"<{self.__class__.__name__} : {self.name} ({self.log_lv_name}) ({self.log_path})>"
        else:
            s = f"<{self.__class__.__name__} : {self.name} ({self.log_lv_name}) (no log path)>"
        return s

    def chmod_777_log_file(self):
        if self.has_log_file and self.log_path.is_file():
            self.log_path.chmod(0o777)

    def __do_log(self, msg: object, log_func: Callable):
        if self.has_log_file:
            log_func(msg)
            # curr_free_space_mb = get_free_space_mb()
            # if curr_free_space_mb > self.LOW_FREE_SPACE_THRESH_MB:
            #     log_func(msg)
            # else:
            #     print(f"[{log_func.__name__}] : {msg}")
            #     send_low_free_space_line_notify()
            #     raise RuntimeError('Low Free Space Danger Error')
        else:
            log_func(msg)

    def debug(self, msg: object):
        self.__do_log(msg, self.logger.debug)

    def info(self, msg: object):
        self.__do_log(msg, self.logger.info)

    def warning(self, msg: object):
        self.__do_log(msg, self.logger.warning)

    def error(self, msg: object):
        self.__do_log(msg, self.logger.error)

    def critical(self, msg: object):
        self.__do_log(msg, self.logger.critical)

    @property
    def handlers(self):
        return self.logger.handlers
