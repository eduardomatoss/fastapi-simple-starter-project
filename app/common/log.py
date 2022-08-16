from logging import config, StreamHandler, Formatter  # noqa: F401
from traceback import format_exception
from json import dumps
from socket import gethostname
from os import getenv

from sentry_sdk import init as init_sentry
from sentry_sdk import set_tag as setting_tag_for_sentry
from dynaconf import settings


def get_application_log_level():
    app_log_level = getenv("LOG_LEVEL", settings.get("default_log_level", "INFO"))
    return (
        app_log_level
        if app_log_level in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
        else "INFO"
    )


def get_application_access_log():
    access_log_env = getenv("ACCESS_LOG")
    if access_log_env in ["True", "False"]:
        return True if access_log_env == "True" else False
    else:
        return settings.as_bool("default_access_log")


def create_logger():
    app_env = settings.get("ENV_FOR_DYNACONF", "")
    log_level = get_application_log_level()
    handlers = ["stdout"]
    if app_env == "prod":
        init_sentry(dsn=settings.get("sentry_dsn"))

    dict_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"jsonlog": {"()": LogFormatter}},
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "formatter": "jsonlog",
                "stream": "ext://sys.stdout",
                "level": log_level,
            }
        },
        "loggers": {"": {"handlers": handlers, "propagate": True, "level": log_level}},
    }
    config.dictConfig(dict_config)


def get_level_num(string_level):
    return {
        "CRITICAL": 2,
        "ERROR": 3,
        "WARNING": 4,
        "INFO": 6,
        "DEBUG": 7,
        "NOTSET": 6,
    }[string_level]


class LogFormatter(Formatter):
    def __init__(self):
        self._env = getenv("ENV_FOR_DYNACONF")
        self._host = gethostname()

    def format(self, record):
        log = {
            "timestamp": record.created,
            "_application": "fastapi-simple-starter-project",
            "_environment": self._env,
            "_log_type": "application",
            "host": self._host,
            "level": get_level_num(record.levelname),
            "short_message": str(record.msg),
        }

        if record.levelname == "ERROR" and record.exc_info is not None:
            lines = format_exception(
                record.exc_info[0], record.exc_info[1], record.exc_info[2]
            )
            log["full_message"] = "".join("" + line for line in lines)

        for attr in vars(record):
            if attr[0] == "_":
                log[attr] = getattr(record, attr)
                setting_tag_for_sentry(attr, log[attr])

        return dumps(log)
