import argparse
import logging
import pathlib
from typing import Union

from . import DFLT_LOG_PATH, LOG_LV_DICT
from .ichase_logger import ICHASELogger
from .logger_factory import create_logger
from ..hash import get_md5


def get_mem_md5_id(o: object, length=6, upper=True, lower=False) -> str:
    id_str = get_md5(str(id(o)))[:length]
    if upper:
        id_str = id_str.upper()
    elif lower:
        id_str = id_str.lower()
    return id_str


def get_cls_instance_logger_name(cls_instance: object, length=6, upper=True) -> str:
    cls_emoji = getattr(cls_instance, 'CLS_EMOJI', None)
    if cls_emoji is not None:
        logger_name = f"{cls_emoji} {cls_instance.__class__.__name__}-{get_mem_md5_id(cls_instance, length, upper=upper)}"
    else:
        logger_name = f"{cls_instance.__class__.__name__}-{get_mem_md5_id(cls_instance, length, upper=upper)}"

    return logger_name


def get_cls_instance_logger(
        cls_instance: object,
        log_lv=logging.DEBUG,
        log_path: Union[pathlib.Path, str] = 'default',
        logger_prefix=None,
        logger_suffix=None,
        logger_id_len=6,
        logger_id_upper=True) -> ICHASELogger:
    logger_name = get_cls_instance_logger_name(
        cls_instance,
        length=logger_id_len,
        upper=logger_id_upper
    )

    if logger_prefix is not None:
        logger_name = f"{logger_prefix}{logger_name}"

    if logger_suffix is not None:
        logger_name = f"{logger_name}{logger_suffix}"

    logger = create_logger(logger_name, log_lv=log_lv, log_path=log_path)

    return logger


def clear_dflt_log():
    if DFLT_LOG_PATH.exists():
        try:
            DFLT_LOG_PATH.unlink()
        except FileNotFoundError:
            pass
        msg = f"old default log has been cleared, {DFLT_LOG_PATH}"
    else:
        msg = f"default log path is not exists, {DFLT_LOG_PATH}"

    print(msg)


def msg_add_banner(msg: str, banner_letter='=', banner_len=30) -> str:
    return f"{msg}\n{banner_letter * banner_len}\n"


def get_args_log_lv(args) -> int:
    assert args.log_lv is not None
    return LOG_LV_DICT[args.log_lv]


def add_log_lv_arg_to_parser(parser: argparse.ArgumentParser, dflt_lv='debug'):
    parser.add_argument('--log_lv', choices=LOG_LV_DICT.keys(), default=dflt_lv)


def get_new_paragraph_msg(msg: str, bar_len=45) -> str:
    bar = '=' * bar_len
    s = f"{msg}\n{bar}\n"
    return s


def get_block_msg(msg: str, bar_len=45) -> str:
    bar = '=' * bar_len
    s = f"{bar}\n{msg}\n{bar}"
    return s