import logging
import datetime

from ..utils.log_tool.tool import get_cls_instance_logger


class LikeCooldownHandler:
    CLS_EMOJI = '⏳'

    def __init__(self, log_lv=logging.DEBUG, log_path=None):
        self.logger = get_cls_instance_logger(
            self,
            log_lv=log_lv,
            log_path=log_path
        )

        self.allowed_dt: datetime.datetime = None

    def update_allowed_dt(self):
        curr_dt = datetime.datetime.now()
        self.allowed_dt = curr_dt + datetime.timedelta(hours=1)

    def can_like_now(self) -> bool:
        if self.allowed_dt is None:
            return True

        curr_dt = datetime.datetime.now()

        if curr_dt >= self.allowed_dt:
            return True
        else:
            remaining_td = self.allowed_dt - curr_dt
            remaining_minutes = int(remaining_td.total_seconds() // 60)
            remaining_seconds = int(remaining_td.total_seconds() % 60)

            msg = f"still have to wait: {remaining_minutes}:{remaining_seconds:02}"
            self.logger.info(msg)

            return False
