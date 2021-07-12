import csv
from datetime import datetime
import json
import os
from typing import Dict, List

from date_conversion import datetime_to_str
from log_entry import LogEntry


class Handler:
    """
    Handler that stores and retrieves the list of LogEntry.
    """
    def __init__(self, name: str) -> None:
        self.name = name
        if self.name not in os.listdir():
            self._create_file()

    def _create_file(self) -> None:
        """ Creates empty file. """
        with open(self.name, 'w') as f:
            pass

    def convert_to_objects(self, log_entries: List[Dict]) -> List[LogEntry]:
        """ Convert List[Dict] to List[LogEntry]. """
        log_objects = []
        for log_entry in log_entries:
            log_object = LogEntry(
                date=log_entry["date"], level=log_entry["level"],
                msg=log_entry["msg"])
            log_objects.append(log_object)
        return log_objects


class JsonHandler(Handler):
    """
    Handler that stores and retrieves the list of LogEntry in a JSON file.
    """
    def _create_file(self) -> None:
        with open(self.name, 'w') as f:
            json.dump([], f)


    def save_msg(self, log_entry: 'LogEntry') -> None:
        """ Save message to the JSON File. """
        data = self.read_msg()
        data.append(log_entry.__dict__)

        with open(self.name, 'w') as f:
            json.dump(data, f, default=datetime_to_str)

    def read_msg(self) -> List[LogEntry]:
        """ Reads all logs from the file. """
        with open(self.name, 'r+') as f:
            data = json.load(f)
        return data


class CSVHandler(Handler):
    """
    Handler that stores and retrieves the list of LogEntry in a CSV file.
    """
    def save_msg(self, log_entry: 'LogEntry') -> None:
        """ Save message to the CSV File. """
        logs = self.read_msg()

        with open(self.name, 'w', newline='') as csvfile:
            fieldnames = ['date', 'level', 'msg']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            logs.append(log_entry.__dict__)

            writer.writeheader()
            for log in logs:
                writer.writerow(log)

    def read_msg(self) -> List[LogEntry]:
        """ Reads all logs from the file. """
        with open(self.name, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            logs = []
            for log in reader:
                logs.append(log)
        return logs


class SQLLiteHandler(Handler):
    """
    Handler that stores and retrieves the list of LogEntry in sqlite
    database.
    """
    # def save_msg(self, log_entry: 'LogEntry'):
    #     pass
    pass


class FileHandler(Handler):
    """
    Handler that stores and retrieves the list of LogEntry in text file.
    """
    # def save_msg(self, log_entry: 'LogEntry'):
    #     pass
    pass
