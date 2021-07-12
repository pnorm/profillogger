from datetime import datetime
from pprint import pprint
import re
from typing import Dict, List, Optional

from date_conversion import str_to_datetime
from date_validation import start_before_end
from handlers import Handler
from profil_logger import LogEntry


class ProfilLoggerReader:
    """ Class for reading and filtering logs. """
    def __init__(self, handler: Handler):
        self.handler = handler
        self.data = self.handler.read_msg()
        self.converted_data = self.handler.convert_to_objects(self.data)

    def find_by_text(self, text: str, start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None) -> List[LogEntry]:
        """
        Find log entries that contain given text. If any datetime is given,
        filter logs according to that datetime.
        """
        start_date, end_date = start_before_end(start_date, end_date)

        filtered_logs = []
        for log in self.converted_data:
            if log.msg.find(text) != -1:
                converted_date = str_to_datetime(log.date)
                if (start_date < converted_date) and (end_date > converted_date):
                    filtered_logs.append(log)

        return filtered_logs

    def find_by_regex(self, regex: str, start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None) -> List[LogEntry]:
        """
        Finds logs by a given regexp. If any datetime is given, filter logs
        according to that datetime.
        """
        start_date, end_date = start_before_end(start_date, end_date)

        filtered_logs = []
        for log in self.converted_data:
            if re.search(regex, log.msg):
                converted_date = str_to_datetime(log.date)
                if (start_date < converted_date) and (end_date > converted_date):
                    filtered_logs.append(log)

        return filtered_logs

    def groupby_level(self, start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None
                     ) -> Dict[str, List[LogEntry]]:
        """
        Group logs by level. If any datetime is given, filter logs according to
        that datetime.
        """
        start_date, end_date = start_before_end(start_date, end_date)

        grouped_logs = {
            "info": [], "warning": [], "debug": [], "critical": [], "error": []
            }
        for log in self.converted_data:
            converted_date = str_to_datetime(log.date)
            if (start_date < converted_date) and (end_date > converted_date):
                grouped_logs[log.level.lower()].append(log)

        return grouped_logs

    def groupby_month(self, start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None
                     )-> Dict[str, List[LogEntry]]:
        """
        Group logs by month. If any datetime is given, filter logs according to
        that datetime.
        """
        start_date, end_date = start_before_end(start_date, end_date)

        grouped_logs = {}
        for log in self.converted_data:
            converted_date = str_to_datetime(log.date)
            if (start_date < converted_date) and (end_date > converted_date):
                group = f"{converted_date.year}-{converted_date.month}"
                try:
                    grouped_logs[group].append(log)
                except KeyError:
                    grouped_logs[group] = [log]

        return grouped_logs
