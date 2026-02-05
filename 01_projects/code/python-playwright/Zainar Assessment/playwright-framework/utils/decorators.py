"""Useful decorators for test automation"""
import functools
import time
from utils.logger import logger

def retry_on_failure(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    logger.info(
                        f"{func.__name__} failed (attempt {attempt}/{max_attempts}): {e}"
                    )
                    time.sleep(delay)
        return wrapper
    return decorator


def log_test_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        logger.info(f"Starting {func.__name__}")
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start
            logger.info(f"Completed {func.__name__} in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start
            logger.error(f"Failed {func.__name__} after {duration:.2f}s: {e}")
            raise
    return wrapper
