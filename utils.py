import random
import pandas as pd
from functools import wraps
from time import sleep
from exceptions import RetryException

def random_sleep(average=1):
    _min, _max = average * 1 / 2, average * 3 / 2
    sleep(random.uniform(_min, _max))

def export_to_csv(result):
    df = pd.DataFrame(result).T.sort_values("followers")
    df.to_csv('result.csv',
              sep=',',
              na_rep='NaN')

def retry(attempt=10, wait=0.3):
    def wrap(func):
        @wraps(func)
        def wrapped_f(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except RetryException:
                if attempt > 1:
                    sleep(wait)
                    return retry(attempt - 1, wait)(func)(*args, **kwargs)
                else:
                    exc = RetryException()
                    exc.__cause__ = None
                    raise exc

        return wrapped_f

    return wrap

def text_to_num(text, bad_data_val = 0):
    text = text.replace(",", "")
    d = {
        'K': 1000,
        'M': 1000000,
        'B': 1000000000
    }
    if not isinstance(text, str):
        return bad_data_val
    elif text[-1].upper() in d:
        num, magnitude = text[:-1], text[-1].upper()
        return int(float(num) * d[magnitude])
    return int(text)