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
from pycom import PiCom
import frames as fr
import plotwnd as pw
import plotlistwnd as pl
import queue


class SpectrWnd(tk.Tk):
    def __init__(self):
        super().__init__()

        self.picom = None

        self.info_queue = queue.Queue()
        self.data_queue = queue.Queue()

        self.bind('<<MessageInfo>>', lambda e: self.do_append_info(e))

        self.title("pyColorApp")
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_control = fr.ToolFrame(self)
        self.frame_control.grid(row=0, column=0, sticky="ew")

        self.frame_base = tk.Frame(master=self, highlightthickness=1, highlightbackground="blue")
        self.frame_base.grid(row=1, column=0, sticky="nsew")
        self.frame_base.grid_rowconfigure(0, weight=1)
        self.frame_base.grid_columnconfigure(0, weight=0)
        self.frame_base.grid_columnconfigure(1, weight=1)
        self.frame_base.grid_columnconfigure(2, weight=0)

        self.frame_info = fr.InfoFrame(self.frame_base)
        self.frame_info.grid(row=0, column=0, sticky="nsew")

        self.frame_plot = pw.PlotFrame(self.frame_base)
        self.frame_plot.grid(row=0, column=1, sticky="nsew")

        self.frame_pl = pl.PlotListWnd(self.frame_base, self.frame_plot)
        self.frame_pl.grid(row=0, column=2, sticky="nsew")
        self.frame_pl.restore()

    def list_ports(self):
        return PiCom.list_ports()

    def clicked_open(self):
        self.picom = PiCom(self.frame_control.get_port(), self)

    def clicked_close(self):
        if self.picom:
            self.picom.close()
            self.picom = None
            self.frame_info.clear()

    def clicked_start(self):
        if self.picom:
            self.picom.start()
            line, color = self.frame_plot.start_plot()
            self.frame_pl.add_plot(line, color)

    def clicked_stop(self):
        if self.picom:
            self.picom.stop()

    def clicked_time(self):
        if self.picom:
            self.picom.set_time(self.frame_control.get_time())

    def loop(self):
        self.mainloop()

    def closed(self):
        self.frame_pl.save()
        if self.picom:
            self.picom.close()

    def do_append_info(self, e):
        txt = self.info_queue.get()
        self.frame_info.append_info(txt + '\n')

    def append_info(self, txt):
        self.info_queue.put(txt)
        self.event_generate('<<MessageInfo>>', when="tail")

    def update_plot(self, data):
        self.frame_info.append_info("Data " + str(len(data)) + '\n')
        self.frame_plot.update_plot(data)
