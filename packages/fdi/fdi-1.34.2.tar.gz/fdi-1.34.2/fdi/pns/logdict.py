# -*- coding: utf-8 -*-
import getpass

# different user has different log file to allow multiple user
logfile = '/tmp/server_' + getpass.getuser() + '.log'
logdict = {
    "version": 1,
    "formatters": {
        "short": {
            "format": "%(funcName)s() %(message)s"
        },
        "full": {
            "format": "%(asctime)s %(name)s %(levelname)s %(process)d %(threadName)s %(args)s %(funcName)s():%(lineno)s - %(message)s",
            # 'datefmt': '%Y%m%d %H:%M:%S'
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
            "level": "INFO",
            "formatter": "full",
            "filename": logfile,
            "maxBytes": 20000000,
            "backupCount": 3
        }
    },
    "loggers": {
        "": {
            "level": "WARN",
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
