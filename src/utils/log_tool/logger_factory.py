# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 3/10/23
"""
import os
import datetime
import pytz
import logging
import logging.handlers


class CustomFormatter(logging.Formatter):
    __LEVEL_COLORS = [
        (logging.DEBUG, '\x1b[40;1m'),
        (logging.INFO, '\x1b[34;1m'),
        (logging.WARNING, '\x1b[33;1m'),
        (logging.ERROR, '\x1b[31m'),
        (logging.CRITICAL, '\x1b[41m'),
    ]
    __FORMATS = None

    timezone = 'Asia/Taipei'

    @classmethod
    def get_formats(cls):
        if cls.__FORMATS is None:
            cls.__FORMATS = {
                level: logging.Formatter(
                    f'%(asctime)s {color}%(levelname)-3s\x1b[0m \x1b[35m%(name)s\x1b[0m 📝 %(message)s',
                    '%Y-%m-%d %H:%M:%S'
                )
                for level, color in cls.__LEVEL_COLORS
            }
        return cls.__FORMATS

    def format(self, record):
        formatter = self.get_formats().get(record.levelno)
        if formatter is None:
            formatter = self.get_formats()[logging.DEBUG]
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f'\x1b[31m{text}\x1b[0m'

        if self.timezone:
            # print(f"self.timezone = {self.timezone}")
            tz = pytz.timezone(self.timezone)
            print(f"orig ts = {record.created}, target = {datetime.datetime.fromtimestamp(record.created, tz=tz).timestamp()}")
            dt = datetime.datetime.fromtimestamp(record.created, tz=tz)
            # dt += datetime.timedelta(hours=8) # !@# debug
            record.created = dt.timestamp()
            print(f"final created = {datetime.datetime.fromtimestamp(record.created)}")

        output = formatter.format(record)
        record.exc_text = None
        return output


class FileHandler(logging.FileHandler):
    def __init__(self, log_file):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        super().__init__(log_file, encoding='utf-8')


class ConsoleHandler(logging.StreamHandler):
    pass


formatter = CustomFormatter()
# file_handler = FileHandler('./logs')
console_handler = ConsoleHandler()


def create_logger(name, log_lv=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(log_lv)

    # file_handler.setLevel(log_lv)
    # file_formatter = logging.Formatter('⏰ %(asctime)s <%(name)s> [%(levelname)s] 📝 %(message)s')
    # file_handler.setFormatter(file_formatter)
    # logger.addHandler(file_handler)

    console_handler.setLevel(log_lv)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
