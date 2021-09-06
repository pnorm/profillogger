import csv
import json
import os
import sqlite3
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
        with open(self.name, 'w'):
            pass

    @staticmethod
    def convert_to_objects(log_entries: List[Dict]) -> List[LogEntry]:
        """ Convert List[Dict] to List[LogEntry]. """
        log_objects = []
        for log_entry in log_entries:
            log_object = LogEntry(
                date=log_entry["date"], level=log_entry["level"],
                msg=log_entry["msg"])
            log_objects.append(log_object)
        return log_objects

    def read_msg(self):
        pass


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

    def read_msg(self) -> List[Dict]:
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

        with open(self.name, 'w', newline='') as csv_file:
            fieldnames = ['date', 'level', 'msg']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            logs.append(log_entry.__dict__)

            writer.writeheader()
            for log in logs:
                writer.writerow(log)

    def read_msg(self) -> List[Dict]:
        """ Reads all logs from the file. """
        with open(self.name, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            logs = []
            for log in reader:
                logs.append(log)
        return logs


class SQLLiteHandler(Handler):
    """
    Handler that stores and retrieves the list of LogEntry in sqlite
    database.
    """

    def _create_file(self) -> None:
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        c.execute(""" CREATE TABLE logs (
                        date text,
                        level text,
                        msg text) """)
        conn.commit()
        conn.close()

    def save_msg(self, log_entry: 'LogEntry') -> None:
        conn = sqlite3.connect(self.name)
        c = conn.cursor()

        c.execute("INSERT INTO logs VALUES (?,?,?)",
                  (datetime_to_str(log_entry.date), log_entry.level,
                   log_entry.msg))
        conn.commit()
        conn.close()

    def read_msg(self) -> List[dict]:
        conn = sqlite3.connect(self.name)
        c = conn.cursor()

        query = c.execute("SELECT * FROM logs")
        col_name = [d[0] for d in query.description]
        result = [dict(zip(col_name, r)) for r in query.fetchall()]

        conn.commit()
        conn.close()
        return result
