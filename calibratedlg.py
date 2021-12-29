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
from tkinter import simpledialog


class CalibrateDlg(simpledialog.Dialog):

    def body(self, main):
        self.main = main

        tk.Label(main, text="Current:").grid(row=0, column=1)
        tk.Label(main, text="New:").grid(row=0, column=2)
        tk.Label(main, text="Marker 1:").grid(row=1, column=0)
        tk.Label(main, text="Marker 2:").grid(row=2, column=0)

        self.entCM1 = tk.Entry(main)
        self.entCM2 = tk.Entry(main)
        self.entNM1 = tk.Entry(main)
        self.entNM2 = tk.Entry(main)

        a, b = main.master.parent.get_markers()

        self.entCM1.grid(row=1, column=1, padx=3, pady=2)
        self.entCM2.grid(row=2, column=1)
        self.entNM1.grid(row=1, column=2, padx=3, pady=2)
        self.entNM2.grid(row=2, column=2)

        self.entCM1.insert(0, str(a))
        self.entCM2.insert(0, str(b))
        self.entNM1.insert(0, str(a))
        self.entNM2.insert(0, str(b))

        self.entCM1.configure(state='readonly')
        self.entCM2.configure(state='readonly')

        self.varMarkers = tk.BooleanVar()
        self.varMarkers.set(True)
        self.check = tk.Checkbutton(main, text="From markers", variable=self.varMarkers, command=self.update_markers)
        self.check.grid(row=3, column=1)

    def apply(self):
        cm1 = float(self.entCM1.get())
        cm2 = float(self.entCM2.get())
        nm1 = float(self.entNM1.get())
        nm2 = float(self.entNM2.get())
        self.result = cm1, cm2, nm1, nm2

    def update_markers(self):
        if self.varMarkers.get():
            a, b = self.main.master.parent.get_markers()
            self.entCM1.insert(0, str(a))
            self.entCM2.insert(0, str(b))
            self.entCM1.configure(state='readonly')
            self.entCM2.configure(state='readonly')
        else:
            self.entCM1.configure(state='normal')
            self.entCM2.configure(state='normal')
