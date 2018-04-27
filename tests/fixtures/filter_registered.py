from time import time

from .utils import build_data


HOUR = 60 * 60
DAY = HOUR * 24

mock_registered_1 = (
    build_data(created=(time() - HOUR)),  # TODAY
    build_data(created=(time() - DAY * 2 + HOUR)),  # YESTERDAY
    build_data(created=(time() - DAY * 3 + HOUR)),  # FOR_3_DAYS
    build_data(created=(time() - DAY * 7 + HOUR)),  # FOR_WEEK
    build_data(created=(time() - DAY * 32 + HOUR)),  # FOR_MONTH
    build_data(created=(time() - DAY * 367 + HOUR)),  # FOR_YEAR
)
