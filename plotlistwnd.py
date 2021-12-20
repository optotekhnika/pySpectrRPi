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
import h5py


class PlotElement(tk.Frame):
    def __init__(self, masterFrame, spwnd, r_var, val, comment, color, plot):
        super().__init__(masterFrame, highlightthickness=1, highlightbackground="blue")

        self.color = color
        self.is_hidden = False
        self.spwnd = spwnd
        self.plot = plot

        self.btnHide = tk.Button(self, text=" ", command=self.hide, bg=color, activebackground=color)
        self.btnHide.grid(column=0, row=0, padx=4, pady=4)

        self.rad = tk.Radiobutton(self, variable=r_var, value=val)
        self.rad.grid(column=1, row=0)

        self.lbl = tk.Label(self, text=comment)
        self.lbl.grid(column=2, row=0, padx=4)

        self.btnExpand = tk.Button(self, text="X", command=self.expand)
        self.btnExpand.grid(column=3, row=0, padx=4, pady=4)

    def expand(self):
        if not self.is_hidden:
            self.spwnd.expand_plot(self.plot)

    def hide(self):
        if self.is_hidden:
            self.btnHide.config(bg=self.color, activebackground=self.color)
        else:
            self.btnHide.config(bg='white', activebackground='white')
        self.is_hidden = not self.is_hidden
        self.spwnd.hide_plot(self.plot, self.is_hidden)


class PlotListWnd(tk.Frame):
    def __init__(self, mainframe, spwnd):
        super().__init__(mainframe, highlightthickness=1, highlightbackground="blue")
        self.spwnd = spwnd
        self.list = []

        self.r_var = tk.IntVar()

    def add_plot(self, plot, color):
        r = len(self.list)
        p = PlotElement(self, self.spwnd, self.r_var, r, comment="Plot", color=color, plot=plot)
        p.grid(column=0, row=r)
        self.r_var.set(r)
        self.list.append(p)

    def save(self):
        n = len(self.list)
        with h5py.File("spw.hdf5", "w") as f:
            gs = f.create_group("single")
            ds = gs.create_dataset("ds", (n, 2, 256))
            for i in range(n):
                x, y = self.spwnd.xy_plot(self.list[i].plot)
                ds[i, 0, ] = x
                ds[i, 1, ] = y

    def restore(self):
        with h5py.File("spw.hdf5", "r") as f:
            ds = f["single/ds"]
            for pl in ds:
                p, c = self.spwnd.add_plot(pl[0], pl[1])
                self.add_plot(p, c)
