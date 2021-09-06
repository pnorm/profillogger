from datetime import datetime


def datetime_to_str(o) -> str:
    """ Datetime object to string conversion. """
    if isinstance(o, datetime):
        return o.isoformat()


def str_to_datetime(log_date: str) -> datetime:
    """ String to datetime object conversion. """
    try:
        return datetime.strptime(log_date, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        return datetime.strptime(log_date, "%Y-%m-%dT%H:%M:%S.%f")
