from ._logs import _basic_config, get_logger
from .answers import get_answer

_basic_config()

__all__ = ["get_logger", "get_answer"]
