from datetime import datetime
from pprint import pprint

from handlers import JsonHandler, CSVHandler, SQLLiteHandler
from profil_logger import ProfilLogger
from profil_logger_reader import ProfilLoggerReader


json_handler = JsonHandler("logs.json")
csv_handler = CSVHandler("logs.csv")
sql_handler = SQLLiteHandler("logs.db")

# Saving logs to json and csv file
logger = ProfilLogger(handlers=[json_handler, csv_handler, sql_handler])

logger.set_log_level("debug")
logger.info("Some info message")
logger.warning("Some warning message")
logger.debug("Some debug message")
logger.critical("Some critical message")
logger.error("Some error message")

# Reading logs from csv file
log_reader = ProfilLoggerReader(handler=sql_handler)

# Finding by text
pprint(log_reader.find_by_text("info message"))
pprint(log_reader.find_by_text("info message", datetime(2021, 7, 11), datetime(2021, 7, 13)))
# Below raise exception
# pprint(log_reader.find_by_text("info message", datetime(2021, 7, 10, 16), datetime(2021, 7, 10, 15)))

# Find by regular expression
pprint(log_reader.find_by_regex("[gr]{1} message"))
pprint(log_reader.find_by_regex("[gr]{1} message", datetime(2021, 7, 12), datetime(2021, 7, 13)))

# Group by level
pprint(log_reader.group_by_level())

# Group by month
pprint(log_reader.groupby_month())
