#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2022-12-05 18:36
"""
import time
import dask
from distributed import Client, delayed
# python -m pip install "dask[distributed]" --upgrade    # or pip install
from os import cpu_count
dask.config.set(scheduler='threads')  # overwrite default with threaded scheduler
c = Client(n_workers=cpu_count())
from concurrent.futures import ThreadPoolExecutor
# with dask.config.set(pool=ThreadPoolExecutor(4)):
#     x.compute()
# 
# with dask.config.set(num_workers=4):
#     x.compute()

def inc(x):
    return x + 1

fut = c.submit(inc, 1)
# c.cluster
c.submit(inc, 1)

def dec(x):
    time.sleep(3)
    return x - 1

def add(x, y):
    time.sleep(7)
    return x + y

x = delayed(inc)(1)
y = delayed(dec)(2)
total = delayed(add)(x, y)
c.gather(fut)

# results = [future.result() for future in futures]
# results = client.gather(futures)  # this can be faster
# del future  # deletes remote data once future is garbage collected
# future.cancel()  # deletes data even if other futures point to it
# fire_and_forget(client.submit(func, *args)) Run tasks at least once, even if we release the futures