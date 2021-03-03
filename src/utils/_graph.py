"""
DO NOT USE LOGGING IN THIS FILE.

This file is internal to the graph and tries to get around the mess
that is matplotlib's implementation of backends.
"""

import os
from _tkinter import TclError
from multiprocessing import Process

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

BACKEND_TIMEOUT = 5


def check_backend():
    """
    If fails will return False and change the backend to headless.
    :return:
    """
    tk = True
    x = np.arange(0, 5, 0.1)
    y = np.sin(x)
    p1 = Process(target=plt.plot, args=(x, y))
    try:
        p1.start()
        p1.join(timeout=BACKEND_TIMEOUT)
        if p1.exitcode is None:
            raise TclError("pyplot timed out: could not find DISPLAY \"%s\"" % os.environ['DISPLAY'])
        matplotlib.use("TKAgg", force=True)
        tk = True
    except TclError as e:
        print(e)
        matplotlib.use("Agg", force=True)
        tk = False
    finally:
        p1.kill()
        plt.close()
        print("Set backend to %s" % matplotlib.get_backend())
        return tk

