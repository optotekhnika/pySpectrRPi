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
from tkinter.ttk import Combobox
from tkinter import scrolledtext, END


class ToolFrame(tk.Frame):
    def __init__(self, mainwnd):
        super().__init__(mainwnd, highlightthickness=1, highlightbackground="blue")

        self.lbl = tk.Label(self, text="Choose com port")
        self.lbl.grid(column=0, row=0, padx=4, pady=2)

        self.combo = Combobox(self)
        self.combo.grid(column=1, row=0, padx=4)

        self.combo['values'] = mainwnd.list_ports()
        self.combo.current(0)

        self.btnOpen = tk.Button(self, text="Open com", command=mainwnd.clicked_open)
        self.btnOpen.grid(column=2, row=0, padx=4, pady=2)

        self.btnClose = tk.Button(self, text="Close", command=mainwnd.clicked_close)
        self.btnClose.grid(column=3, row=0, padx=4, pady=2)

        self.btnStart = tk.Button(self, text="Start", command=mainwnd.clicked_start)
        self.btnStart.grid(column=4, row=0, padx=4, pady=2)

        self.btnStop = tk.Button(self, text="Stop", command=mainwnd.clicked_stop)
        self.btnStop.grid(column=5, row=0, padx=4, pady=2)

        self.btnTime = tk.Button(self, text="Time", command=mainwnd.clicked_time)
        self.btnTime.grid(column=6, row=0, padx=4, pady=2)

        self.entTime = tk.Entry(self)
        self.entTime.grid(column=7, row=0, padx=4, pady=2)

    def get_port(self):
        self.lbl.configure(text="Opening {}".format(self.combo.get()))
        return self.combo.get()

    def get_time(self):
        return self.entTime.get()


class InfoFrame(tk.Frame):
    def __init__(self, mainwnd):
        super().__init__(mainwnd, highlightthickness=1, highlightbackground="blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.info = scrolledtext.ScrolledText(self, width=30)
        self.info.grid(row=0, column=0, sticky="nsew")
        self.info.insert(END, "Hello!\n")

    def append_info(self, txt):
        self.info.insert(END, txt)

    def clear(self):
        self.info.delete("1.0", END)
