import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk,  # type: ignore
)

from gex.extra.NetworkList import network_index

from rich import print

from pandapower.auxiliary import pandapowerNet as ppNet

from gex.paint import plot_pp_network


class gexGui:
    def __init__(self, root: tk.Tk, net: ppNet):
        self.root = root
        self.root.title("Grid Explorer")

        self.net = net

        self.create_widgets()

    def create_widgets(self):
        # Canvas
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        # create the toolbar
        NavigationToolbar2Tk(self.canvas, self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.ax = self.figure.add_subplot(111)
        self.plot_net()

        # Console
        self.console = tk.Entry(self.root)
        self.console.pack(fill=tk.X)
        self.console.bind("<Return>", self.handle_input)
        self.console.focus_set()

    def handle_input(self, event):
        input_str = self.console.get()
        self.console.delete(0, tk.END)

        exec(input_str)

        self.plot_net()

    def plot_net(self):
        self.ax.clear()
        plot_pp_network(self.net, self.ax)

        self.ax.legend()
        self.canvas.draw()


def run_gui(net):
    root = tk.Tk()
    app = gexGui(root, net)
    root.mainloop()


if __name__ == "__main__":
    net = network_index["case118"]()
    print(net)
    run_gui(net)
