# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE

from requests import get
from time import time, sleep


class ThrottledRequest(object):
    def __init__(self, request_per_second: int) -> None:
        self._request_cycletime = 1 / request_per_second
        self._time = time()

    def get(self, url: str):
        time_diff = time() - self._time
        sleep_time = self._request_cycletime - time_diff
        if sleep_time > 0:
            sleep(sleep_time)
        self._time = time()
        return get(url)
