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
from matplotlib.backend_bases import MouseButton
import matplotlib.colors as mc
import numpy as np
from matplotlib.lines import Line2D


def scale(data):
    l = min(data)
    h = max(data)
    d = (h - l) / 8
    l = l - d
    h = h + d
    return l, h


class MouseDrag:
    def __init__(self):
        self.vertical = False
        self.stretch = False
        self.on = False
        self.x0 = 0
        self.y0 = 0


class PickCursor:
    def __init__(self):
        self.line = None
        self.ind = None
        self.lineShift = None
        self.indShift = None

    def set_cursor(self, line, ind):
        if self.lineShift == self.line and self.line:
            self.lineShift.set_markevery([self.indShift])
        elif self.line:
            self.line.set_markevery([])
        if self.lineShift == line:
            line.set_markevery([ind, self.indShift])
        else:
            line.set_markevery([ind])
        self.line = line
        self.ind = ind

    def set_cursor_shift(self, line, ind):
        if self.lineShift == self.line and self.line:
            self.line.set_markevery([self.ind])
        elif self.lineShift:
            self.lineShift.set_markevery([])
        if self.line == line:
            line.set_markevery([ind, self.ind])
        else:
            line.set_markevery([ind])
        self.lineShift = line
        self.indShift = ind

    def delete(self, line):
        if line == self.lineShift:
            self.lineShift = None
        if line == self.line:
            self.line = None

    def get_indx(self):
        if self.line:
            x, y = self.line.get_data()
            a = x[self.ind]
        else:
            a = 0
        if self.lineShift:
            x, y = self.lineShift.get_data()
            b = x[self.indShift]
        else:
            b = 0
        if a < b:
            return a, b
        return b, a


class PlotFrame(tk.Frame):
    def __init__(self, mainwnd):
        super().__init__(mainwnd, highlightthickness=1, highlightbackground="blue")

        self.line = None
        self.autoscale = False
        self.cursors = PickCursor()

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

        binding_id = self.fig.canvas.mpl_connect('motion_notify_event', self.mouse_move)
        self.fig.canvas.mpl_connect('button_press_event', self.mouse_press)
        self.fig.canvas.mpl_connect('button_release_event', self.mouse_release)
        self.fig.canvas.mpl_connect('pick_event', self.pick)

        self.fig.tight_layout(pad=1.0)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        self.mdrag = MouseDrag()

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
        t = np.arange(0, 256, 1)
        return self.add_plot(t, 40000 * np.sin(2 * np.pi * t))

    def add_plot(self, x, y):
        self.line = self.aplot.plot(x, y, picker=True, marker='d', markevery=[])[-1]
        self.line.set_markerfacecolor('black')
        self.line.set_markersize(9)
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

    def hide_plot(self, line, hide):
        if hide:
            line.set_linestyle("None")
        else:
            line.set_linestyle("solid")
        self.canvas.draw()

    def del_plot(self, line):
        self.cursors.delete(line)
        self.aplot.lines.remove(line)
        self.canvas.draw()

    def xy_plot(self, plot):
        return plot.get_data()

    def x_marked(self):
        if self.cursors.line:
            x, y = self.cursors.line.get_data()
            return x
        return None

    def get_markers(self):
        return self.cursors.get_indx()

    def mouse_press(self, event):
        if event.inaxes:
            return
        if event.button == MouseButton.LEFT:
            self.mdrag.stretch = False
        elif event.button == MouseButton.RIGHT:
            self.mdrag.stretch = True
        else:
            return
        xf, yf = self.fig.transFigure.inverted().transform((event.x, event.y))
        apos = self.aplot.get_position()
        if xf < apos.x0:
            self.mdrag.vertical = True
        elif yf < apos.y0:
            self.mdrag.vertical = False
        self.mdrag.on = True
        xd, yd = self.aplot.transData.inverted().transform((event.x, event.y))
        self.mdrag.x0 = xd
        self.mdrag.y0 = yd
        print(xd, yd)

    def mouse_release(self, event):
        self.mdrag.on = False

    def mouse_move(self, event):
        if not self.mdrag.on:
            return
        if event.inaxes:
            return
        x, y = event.x, event.y
        xd, yd = self.aplot.transData.inverted().transform((x, y))
        if event.button == MouseButton.LEFT:
            if self.mdrag.vertical:
                l, h = self.aplot.get_ylim()
                d = self.mdrag.y0 - yd
                self.aplot.set_ylim([l + d, h + d])
                self.canvas.draw()
            else:
                l, h = self.aplot.get_xlim()
                d = self.mdrag.x0 - xd
                self.aplot.set_xlim([l + d, h + d])
                self.canvas.draw()
        elif event.button == MouseButton.RIGHT:
            xa, ya = self.aplot.transAxes.inverted().transform((x, y))
            if self.mdrag.vertical:
                l, h = self.aplot.get_ylim()
                h = l + (self.mdrag.y0 - l) / ya
                self.aplot.set_ylim([l, h])
                self.canvas.draw()
            else:
                l, h = self.aplot.get_xlim()
                h = l + (self.mdrag.x0 - l) / xa
                self.aplot.set_xlim([l, h])
                self.canvas.draw()

    def pick(self, event):
        if isinstance(event.artist, Line2D):
            thisline = event.artist
            ind = event.ind
            n = len(ind)
            if n > 0:
                if event.mouseevent.key == 'shift':
                    self.cursors.set_cursor_shift(thisline, ind[int(n/2)])
                else:
                    self.cursors.set_cursor(thisline, ind[int(n / 2)])
                self.canvas.draw()
