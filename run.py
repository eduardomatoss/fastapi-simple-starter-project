from logging import getLogger

from uvicorn import run

from app.common.log import (
    create_logger,
    get_application_log_level,
    get_application_access_log,
)
from app.api import app as application


create_logger()
logger = getLogger()

if __name__ == "__main__":
    run(
        "run:application",
        host="0.0.0.0",
        port=8000,
        workers=4,
        log_level=get_application_log_level().lower(),
        access_log=get_application_access_log(),
    )