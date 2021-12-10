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


class PlotElement(tk.Frame):
    def __init__(self, mainwnd, r_var, val):
        super().__init__(mainwnd, highlightthickness=1, highlightbackground="blue")

        self.rad = tk.Radiobutton(self, variable=r_var, value=val)
        self.rad.grid(column=0, row=0)

        self.lbl = tk.Label(self, text="Plot 1")
        self.lbl.grid(column=1, row=0, padx=4)

        self.btnOpen = tk.Button(self, text="X", command=self.expand)
        self.btnOpen.grid(column=2, row=0, padx=4)

    def expand(self):
        None


class PlotListWnd(tk.Frame):
    def __init__(self, mainwnd):
        super().__init__(mainwnd, highlightthickness=1, highlightbackground="blue")
        self.list = []

        self.r_var = tk.IntVar()

        p1 = PlotElement(self, self.r_var, 0)
        p1.grid(column=0, row=0)
        self.list.append(p1)
        p2 = PlotElement(self, self.r_var, 1)
        p2.grid(column=0, row=1)
        self.list.append(p2)
        p3 = PlotElement(self, self.r_var, 2)
        p3.grid(column=0, row=2)
        self.list.append(p3)

        self.r_var.set(1)

