## Recruitment Task - backend internship 06-2021

Hi! My name is Paweł Normann
This is my solution of the recruitment task posted at
https://git.profil-software.com/recruitment-06-2021/recruitment-task-backend-internship

#### 1. Clone repository
```sh
$ git clone https://github.com/pnorm/profillogger.git
```

#### 2. Create and activate virtual environment
```sh
~/profillogger$ python3.8 -m venv env
~/profillogger$ source env/bin/activate
```

### 3. Examples how to use script
 - Example 1
```py
from datetime import datetime
from pprint import pprint

from handlers import JsonHandler, CSVHandler, SQLLiteHandler, FileHandler
from profil_logger import ProfilLogger
from profil_logger_reader import ProfilLoggerReader


json_handler = JsonHandler("logs.json")
csv_handler = CSVHandler("logs.csv")

# Saving logs to json and csv file
logger = ProfilLogger(handlers=[json_handler, csv_handler])

logger.set_log_level("debug")
logger.info("Some info message")
logger.warning("Some warning message")
logger.debug("Some debug message")
logger.critical("Some critical message")
logger.error("Some error message")

# Reading logs from csv file
log_reader = ProfilLoggerReader(handler=csv_handler)

# Finding by text
pprint(log_reader.find_by_text("info message"))
pprint(log_reader.find_by_text("info message", datetime(2021, 7, 11), datetime(2021, 7, 13)))
# Below raise exception (Start date before end date)
# pprint(log_reader.find_by_text("info message", datetime(2021, 7, 10, 16), datetime(2021, 7, 10, 15)))

# Find by regular expression
pprint(log_reader.find_by_regex("[gr]{1} message"))
pprint(log_reader.find_by_regex("[gr]{1} message", datetime(2021, 7, 12), datetime(2021, 7, 13)))

# Groupby level
pprint(log_reader.groupby_level())

# Groupby month
pprint(log_reader.groupby_month())
```

