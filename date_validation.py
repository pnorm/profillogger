from datetime import datetime
from typing import Union


def start_before_end(start_date: Union[datetime, None],
                     end_date: Union[datetime, None]) -> datetime:
    if start_date == None:
        start_date = datetime(1970, 1, 1)
    if end_date == None:
        end_date = datetime.now()

    if start_date > end_date:
        raise Exception("Start date must be before end date")

    return start_date, end_date
