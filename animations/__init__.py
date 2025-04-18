import logging
from logging import NullHandler
from .main import app

__version__ = "1.0.0"

__all__ = ["app"]

logging.getLogger(__name__).addHandler(NullHandler())