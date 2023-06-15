""" Decorators Module """

from functools import wraps
from time import time
from typing import Any, Callable

from app.utils.logger import configure_logger

logger = configure_logger()


def timeit(f: Callable) -> Callable:
    """Decorator to measure time"""

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time()
        result = f(*args, **kwargs)
        end = time()
        logger.info(f"{f.__name__} execution duration: {round((end - start) * 10**3,2)} ms")
        return result

    return wrapper
