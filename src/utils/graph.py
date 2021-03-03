import os
from _tkinter import TclError
from multiprocessing import Process

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from utils.file import File
from utils.log import Log

BACKEND_TIMEOUT = 5


# TODO(M-Whitaker): This function is in a rubbish place however you can't pre-declare functions in python.
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
        Log.warning(e)
        matplotlib.use("Agg", force=True)
        tk = False
    finally:
        p1.kill()
        plt.close()
        Log.info("Set backend to %s" % matplotlib.get_backend())
        return tk


try:
    import _tkinter
    TK_IMPLEMENTED = check_backend()
except ImportError:
    TK_IMPLEMENTED = False


class Graph:

    @staticmethod
    def plot_graph(graph_name: str, to_file=False):
        if TK_IMPLEMENTED and not to_file:
            plt.show()
        else:
            filename = "/app/data/out/graphs/%s.png" % graph_name
            filename = File.get_safe_file_path(filename, ".png")
            plt.savefig(filename)
            Log.info("plot saved as: %s" % filename)
