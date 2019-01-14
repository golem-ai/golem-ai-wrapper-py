#!/usr/bin/python3
#coding=utf-8

"""
This module is included in the package golem_ai.
It is composed by a list method that manage the logging system
used in this package.
"""
import logging
import logging.config
import os

  
def setup():
    # Init Global Var
    global GOLEM_LOG
    GOLEM_LOG = None if not "GOLEM_LOG" in os.environ or not len(os.environ["GOLEM_LOG"]) else os.environ["GOLEM_LOG"]
    if bool(GOLEM_LOG):
        # Check and setup log folder
        if os.path.isfile(GOLEM_LOG):
            from .exceptions import GConfigException
            raise GConfigException("$GOLEM_LOG (actual value: '{}') must be a directory".format(GOLEM_LOG))
        elif not os.path.isdir(GOLEM_LOG):
            try:
                os.mkdir(GOLEM_LOG)
            except Exception as err:
                raise GConfigException("$GOLEM_LOG (actual value: '{}') cannot be created because: {}".format(GOLEM_LOG, err))
        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "NormalFormatter": {
                    "format": "%(asctime)s [%(levelname)s]: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "FullHandler": {
                    "level": "DEBUG",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": os.path.join(GOLEM_LOG, "golem_ai-full.log"),
                    "maxBytes": 10000000,
                    "formatter": "NormalFormatter",
                },
                "InfoHandler": {
                    "level": "INFO",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": os.path.join(GOLEM_LOG, "golem_ai-info.log"),
                    "maxBytes": 10000000,
                    "formatter": "NormalFormatter",
                },
                "ErrorHandler": {
                    "level": "WARNING",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": os.path.join(GOLEM_LOG, "golem_ai-error.log"),
                    "maxBytes": 10000000,
                    "backupCount": 10,
                    "formatter": "NormalFormatter",
                }
            },
            "loggers": {
                "Default": {
                    "handlers": ["FullHandler", "InfoHandler", "ErrorHandler"],
                    "level": "DEBUG",
                    "propagate": True,
                }
            },
        }
        logging.config.dictConfig(config)

def get_log_details():
    return bool(GOLEM_LOG), GOLEM_LOG

def debug(message):
    if bool(GOLEM_LOG):
        logging.getLogger("Default").debug(message)

def info(message):
    if bool(GOLEM_LOG):
        logging.getLogger("Default").info(message)

def warning(message):
    if bool(GOLEM_LOG):
        logging.getLogger("Default").warning(message)

def error(message):
    if bool(GOLEM_LOG):
        logging.getLogger("Default").error(message)

def critical(message):
    if bool(GOLEM_LOG):
        logging.getLogger("Default").critical(message)
