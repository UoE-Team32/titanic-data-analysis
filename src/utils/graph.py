import os

import matplotlib.pyplot as plt

from utils.file import File
from utils.log import Log
from utils._graph import check_backend


if os.environ.get('DISPLAY'):
    try:
        import _tkinter
        TK_IMPLEMENTED = check_backend()
    except ImportError:
        TK_IMPLEMENTED = False
else:
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
        plt.clf()
