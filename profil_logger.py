from datetime import datetime
from typing import List, Optional

# library/app specific imports
from handlers import Handler
from log_entry import LogEntry


class ProfilLogger:
    def __init__(self, handlers: List[Handler]) -> None:
        self.handlers = handlers
        self.levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    def set_log_level(self, minimal_level: str) -> None:
        """ Set minimal log level. """
        log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        try:
            self.levels = log_levels[log_levels.index(minimal_level.upper()):]
        except ValueError:
            raise Exception("This level doesn't exist.")

    def logger(self, msg: str, level: str) -> None:
        """ Logs a message. """
        date = datetime.now()
        log_entry = LogEntry(date, level, msg)
        if level.upper() in self.levels:
            self.store_log(log_entry)

    def info(self, msg: str) -> None:
        """ Logs a message with level INFO. """
        self.logger(msg, "INFO")

    def warning(self, msg: str) -> None:
        """ Logs a message with level WARNING. """
        self.logger(msg, "WARNING")

    def debug(self, msg: str) -> None:
        """ Logs a message with level DEBUG. """
        self.logger(msg, "DEBUG")

    def critical(self, msg: str) -> None:
        """ Logs a message with level CRITICAL. """
        self.logger(msg, "CRITICAL")

    def error(self, msg: str) -> None:
        """ Logs a message with level ERROR. """
        self.logger(msg, "ERROR")

    def store_log(self, log_entry: 'LogEntry') -> None:
        """ Store log entry in given handlers. """
        for handler in self.handlers:
            handler.save_msg(log_entry)
