""" Decorators Module """

from datetime import datetime, timedelta
from functools import lru_cache, wraps
from time import time
from typing import Any, Callable

from loguru import logger


def timeit(f: Callable) -> Callable:
    """Decorator to measure time"""

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time()
        result = f(*args, **kwargs)
        end = time()
        logger.info(
            "%s execution duration: %.0f ms", f.__name__, (end - start) * 10**3
        )
        return result

    return wrapper


def timed_lru_cache(timeout: int, maxsize: int = 128, typed: bool = False)-> Any:
    """
    Extension of functools lru_cache with a timeout

    Parameters:
    timeout (int): Timeout in seconds to clear the WHOLE cache, default = 10 minutes
    maxsize (int): Maximum Size of the Cache
    typed (bool): Same value of different type will be a different entry

    Example:
    @timed_lru_cache(maxsize=12, timeout=15)
    """
    def wrapper_cache(func:Callable)->Any:
        func = lru_cache(maxsize=maxsize, typed=typed)(func)
        func.delta = timedelta(seconds=timeout)  # type: ignore
        func.expiration = datetime.utcnow() + func.delta  # type: ignore

        @wraps(func)
        def wrapped_func(*args:Any, **kwargs:Any)->Any:
            if datetime.utcnow() >= func.expiration:  # type: ignore
                func.cache_clear()  # type: ignore
                func.expiration = datetime.utcnow() + func.delta  # type: ignore

            return func(*args, **kwargs)

        wrapped_func.cache_info = func.cache_info  # type: ignore
        wrapped_func.cache_clear = func.cache_clear  # type: ignore
        return wrapped_func

    return wrapper_cache
