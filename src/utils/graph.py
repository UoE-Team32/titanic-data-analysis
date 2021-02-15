from utils.file import File

try:
    import _tkinter
    TK_IMPLEMENTED = True
except ImportError:
    TK_IMPLEMENTED = False

import matplotlib.pyplot as plt


class Graph:

    @staticmethod
    def plot_graph(graph_name: str, to_file=False):
        if TK_IMPLEMENTED and not to_file:
            plt.show()
        else:
            filename = "/app/data/out/graphs/%s.png" % graph_name
            filename = File.get_safe_file_path(filename, ".png")
            plt.savefig(filename)
            print("plot saved as: %s" % filename)
