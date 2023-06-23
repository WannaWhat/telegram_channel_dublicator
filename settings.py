import logging
import sys
from os import environ, path
from typing import Union

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

load_dotenv(path.join('configs', '.env'))

console_handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(filename='channel_dublicator.log', filemode='a')
root_logger = logging.getLogger()
root_logger.addHandler(console_handler)
root_logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class EnvConfigsModel(BaseModel):
    APP_API_ID: Union[int]
    APP_API_HASH: Union[str]
    OLD_CHANNEL_ID: Union[int]
    NEW_CHANNEL_ID: Union[int]


try:
    app_configs = EnvConfigsModel(**environ)
except ValidationError as e:
    logger.critical('env validation error', exc_info=e)
    sys.exit(-1)
except Exception as e:
    logger.critical('env validation error', exc_info=e)
    sys.exit(-1)
