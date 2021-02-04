try:
    import _tkinter
    TK_IMPLEMENTED = True
except ImportError:
    TK_IMPLEMENTED = False

import matplotlib.pyplot as plt


class Graph:

    @staticmethod
    def plot_graph():
        if TK_IMPLEMENTED:
            plt.show()
        else:
            filename = "../data/out/img.png"
            plt.savefig(filename)
            print("plot saved as: %s" % filename)
