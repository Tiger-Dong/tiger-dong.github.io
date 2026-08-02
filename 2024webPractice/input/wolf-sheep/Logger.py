from logging.handlers import RotatingFileHandler
import logging
import os


def init_logger(logger_name="root", base_dir='', log_file_name="", file_handler_level=logging.INFO):
    log_format = '%(asctime)s: %(levelname)s: %(message)s'
    formatter = logging.Formatter(log_format)
    log_file_name = "{}.log".format(logger_name) if not log_file_name else log_file_name

    handler_console = logging.StreamHandler()
    handler_console.setFormatter(formatter)
    handler_console.setLevel(logging.INFO)

    if not base_dir:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.join(base_dir, "log")
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    log_path = os.path.join(base_dir, log_file_name)
    handler_file = RotatingFileHandler(log_path, maxBytes=20 * 1024 * 1024, backupCount=20)
    handler_file.setFormatter(formatter)
    handler_file.setLevel(file_handler_level)

    logger = logging.getLogger(logger_name)
    logger.addHandler(handler_console)
    logger.addHandler(handler_file)
    logger.setLevel(logging.DEBUG)
    return logger
