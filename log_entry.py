from datetime import datetime


class LogEntry:
    """
    A class for storing the log entry.
    """
    def __init__(self, date: datetime, level: str, msg: str) -> None:
        self.date = date
        self.level = level
        self.msg = msg

    def __repr__(self):
        return f"<LogEntry: {self.msg}, {self.level}, {self.date}>"
