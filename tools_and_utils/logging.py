import datetime as dt
import os
import random
import string
import sys
from xml.etree.ElementTree import QName
import dotenv

import logging
from logging.handlers import RotatingFileHandler

ROOT_DIR = os.path.abspath(__file__).split("services")[0]
sys.path.insert(0, ROOT_DIR)

dotenv.load_dotenv()

class Formats:
    short = "%(asctime)s-L%(lineno)d\t%(message)s"
    long = "%(asctime)s:%(levelname)s:(%(filename)s:%(lineno)d) – %(message)s"


_log_cdpr = os.environ.get("LOG_CDPR_SENSITIVE_DATA", False)
LOG_CDPR_SENSITIVE_DATA = True if _log_cdpr == "True" or _log_cdpr == True else False

log_file = f'logs/{dt.datetime.now().strftime("%Y-%m-%d")}.log'

if not os.path.exists('./logs'):
    os.makedirs('./logs')

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    purple = "\x1b[35;20m"

    _format = Formats.short # Change if necessary

    FORMATS = {
        logging.DEBUG: grey + _format + reset,
        logging.INFO: grey + _format + reset,
        logging.WARNING: yellow + _format + reset,
        logging.ERROR: red + _format + reset,
        logging.CRITICAL: bold_red + _format + reset,
        logging.WARN: purple + _format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        datefmt = '%H_%M_%S'
        formatter = logging.Formatter(log_fmt, datefmt=datefmt)
        return formatter.format(record)
    

class LoggingUtil:
    def __init__(self, name, log_file=log_file, level=logging.INFO):
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        name=name+random_chars
        self.logger = logging.getLogger(name)
        
        log_formatter_color = CustomFormatter()
        formatter = logging.Formatter(Formats.long, datefmt='%H:%M:%S')
        
        
        self.logger.setLevel(level)
        file_handler = RotatingFileHandler(log_file, maxBytes=10_000_000, backupCount=1) # 10 MB
        file_handler = logging.FileHandler(log_file)
        
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setFormatter(log_formatter_color)
        self.logger.addHandler(stream_handler)

    
    def get_logger(self):
        return self.logger

    def cdpr_sens(self, message, *args, **kwargs):
        if LOG_CDPR_SENSITIVE_DATA:
            self.logger._log(logging.INFO, f"CDPR_SENSITIVE: {message}", args, **kwargs)


class PColor:
    def Red(skk): return "\033[91m{}\033[00m".format(skk)
    def Green(skk): return "\033[92m{}\033[00m".format(skk)
    def Yellow(skk): return "\033[93m{}\033[00m".format(skk)
    def LightPurple(skk): return "\033[94m{}\033[00m".format(skk)
    def Purple(skk): return "\033[95m{}\033[00m".format(skk)
    def Cyan(skk): return "\033[96m{}\033[00m".format(skk)
    def LightGray(skk): return "\033[97m{}\033[00m".format(skk)
    def Black(skk): return "\033[98m{}\033[00m".format(skk)

def print_warning(message):
    print("")
    print("\t******************** WARNING **********************")
    print("\t"+PColor.Red(message))
    print("\t**************************************************")
    print("")



if LOG_CDPR_SENSITIVE_DATA:
    print_warning("CDPR_SENSITIVE_DATA logging enabled. This should only be used in testing environments.")