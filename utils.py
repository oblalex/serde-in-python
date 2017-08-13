# coding: utf-8

import time

import humanize
import inflection
import psutil

from concurrent.futures import as_completed
from concurrent.futures import ProcessPoolExecutor

from schemas import Flight


def get_rss(process=None):
    if process is None:
        process = psutil.Process()

    mem = process.memory_info()
    return mem.rss


def format_time(value):
    return "{:.3f} s".format(value)


def format_rss(rss=None):
    if rss is None:
        rss = get_rss()

    return humanize.naturalsize(rss, binary=True, format='%.3f')


def measure(cycles, fn, *args, **kwargs):
    total_time_delta = 0
    total_rss_delta = 0

    max_workers = psutil.cpu_count(logical=True)
    left = cycles

    while left > 0:
        with ProcessPoolExecutor(max_workers=max_workers) as pool:
            workers = min(max_workers, left)

            futures = [
                pool.submit(with_measurements, fn, *args, **kwargs)
                for i in range(workers)
            ]

            for future in as_completed(futures):
                time_delta, rss_delta = future.result()
                total_time_delta += time_delta
                total_rss_delta += rss_delta

            left -= workers

    time_delta = total_time_delta / cycles
    rss_delta = total_rss_delta / cycles

    return (time_delta, rss_delta)


def with_measurements(fn, *args, **kwargs):
    process = psutil.Process()

    rss_start = get_rss(process)
    time_start = time.monotonic()

    result = fn(*args, **kwargs)

    time_end = time.monotonic()
    rss_end = get_rss(process)

    time_delta = time_end - time_start
    rss_delta = rss_end - rss_start

    return (time_delta, rss_delta)


def to_camel(s):
    s = s.title().replace('_', '')
    return s[0].lower() + s[1:]


def from_camel(s):
    return inflection.underscore(s).upper()


def validate(items):
    for item in items:
        Flight(item).validate()
