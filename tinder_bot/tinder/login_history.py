from dataclasses import dataclass, field
import datetime


@dataclass
class LoginHistory:
    last_fln_dt: datetime.datetime = field(default=None)
    last_fln_msg: str = field(default=None)

    def update_fln_data(self, dt: datetime.datetime, msg: str):
        self.last_fln_dt = dt
        self.last_fln_msg = msg

    def last_fln_is_over_x_minutes(self, curr_dt: datetime.datetime, minutes=30) -> bool:
        if self.last_fln_dt is None:
            return True

        td = curr_dt - self.last_fln_dt

        if td.total_seconds() > 60 * minutes:
            return True
        else:
            return False
