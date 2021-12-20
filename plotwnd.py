"""
Copyright (c) 2021 Optotekhnika

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.colors as mc
import numpy as np


def scale(data):
    l = min(data)
    h = max(data)
    d = (h - l) / 8
    l = l - d
    h = h + d
    return l, h


class PlotFrame(tk.Frame):
    def __init__(self, mainwnd):
        super().__init__(mainwnd, highlightthickness=1, highlightbackground="blue")

        self.line = None
        self.autoscale = False

        self.fig = plt.Figure()

        self.aplot = self.fig.add_subplot(111)
        self.aplot.set_xlim([0, 258])
        self.aplot.set_ylim([0, 64000])
        self.aplot.autoscale(enable=False, axis='y', tight=True)
        self.aplot.grid()
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        button_expand = tk.Button(master=toolbar, text="E", command=self.clicked_expand)
        button_expand.pack(side="left")
        button_shrink = tk.Button(master=toolbar, text="S", command=self.clicked_shrink)
        button_shrink.pack(side="left")
        button_ascale = tk.Button(master=toolbar, text="A", command=self.clicked_ascale)
        button_ascale.pack(side="left")
        toolbar.update()

        self.fig.tight_layout(pad=1.0)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    def clicked_expand(self):
        l, h = self.aplot.get_ylim()
        d = (h - l) / 8
        l = l - d
        h = h + d
        self.aplot.set_ylim([l, h])
        self.canvas.draw()

    def clicked_shrink(self):
        l, h = self.aplot.get_ylim()
        d = (h - l) / 8
        self.aplot.set_ylim([l + d, h - d])
        self.canvas.draw()

    def clicked_ascale(self):
        self.autoscale = True

    def start_plot(self):
        t = np.arange(1, 256, 1)
        self.line = self.aplot.plot(t, 40000 * np.sin(2 * np.pi * t))[-1]
        return self.line, mc.to_hex(self.line.get_color())

    def add_plot(self, x, y):
        self.line = self.aplot.plot(x, y)[-1]
        return self.line, mc.to_hex(self.line.get_color())

    def update_plot(self, data):
        if self.line:
            self.line.set_data(range(0, len(data)), data)
            if self.autoscale:
                l, h = scale(data)
                self.aplot.set_ylim([l, h])
                self.autoscale = False
        self.canvas.draw()

    def expand_plot(self, line):
        x, y = line.get_data()
        l, h = scale(y)
        self.aplot.set_ylim([l, h])
        l, h = scale(x)
        self.aplot.set_xlim([l, h])
        self.canvas.draw()

    def hide_plot(self, plot, hide):
        if hide:
            plot.set_linestyle("None")
        else:
            plot.set_linestyle("solid")
        self.canvas.draw()

    def xy_plot(self, plot):
        return plot.get_data()
