# -*- coding: utf-8 -*-
import getpass
import os

# different user has different log file to allow multiple user
#logfile = '/tmp/fditest_' + getpass.getuser() + '_%d.log' % os.getpid()
logfile = '/tmp/fditest_' + getpass.getuser() + '.log'
logdict = {
    "version": 1,
    "formatters": {
        "short": {
            "format": "%S %(funcName)s() %(message)s"
        },
        "full": {
            "format": "%(asctime)s %(name)s %(levelname)s %(process)d %(threadName)s %(funcName)10s():%(lineno)3s - %(message)s",
            'datefmt': '%Y%m%d %H:%M:%S'
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "full",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "full",
            "filename": logfile,
            "maxBytes": 20000000,
            "backupCount": 3
        }
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
    'disable_existing_loggers': False
}
