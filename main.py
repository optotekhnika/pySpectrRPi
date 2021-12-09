#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from json import JSONDecodeError
from threading import Thread
from tkinter.ttk import Combobox
from tkinter import scrolledtext, END
from serial import Serial
import serial.tools.list_ports
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np


class PiCom:
    def __init__(self, port_name, post_info, post_plot):
        self.serialport = Serial(port_name, 115200, parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        bytesize=serial.EIGHTBITS, timeout=5)
        self.post_info = post_info
        self.post_plot = post_plot
        self.update = False
        self.line = None
        self.on = True
        self.thread_loop = Thread(target=self.__listen_loop)
        self.thread_loop.start()

    @staticmethod
    def list_ports():
        ports = serial.tools.list_ports.comports()
        comboports = []
        for port, desc, hwid in sorted(ports):
            comboports.append(port)
        return comboports

    def close(self):
        self.on = False
        if self.serialport:
            self.serialport.close()
            self.thread_loop.join()
            self.serialport = None

    def __listen_loop(self):
        self.post_info("Start loop!")
        while self.on:
            try:
                bts = self.serialport.readline().decode('utf-8')
                if len(bts) == 0:
                    continue
                print(bts)
                j = json.loads(bts)
                if 'info' in j:
                    self.post_info(j["info"])
                if 'cmd' in j:
                    print("Command = " + j['cmd'])
                    if j["cmd"] == "getline" and 'value' in j:
                        print(j['value'])
                        self.post_plot(j["value"])
                        if self.update:
                            self.ask_data()

            except TypeError:
                print("Type error on port")
            except JSONDecodeError:
                print("Json error: " + bts)

    def ask_data(self):
        self.serialport.write("{\"cmd\":\"getline\"}\r\n".encode())

    def start(self):
        self.ask_data()
        self.update = True

    def stop(self):
        self.update = False

    def set_time(self, time):
        self.serialport.write("{\"cmd\":\"settime\", \"time\":".encode())
        self.serialport.write(str(time).encode())
        self.serialport.write("}\r\n".encode())


class SpectrWnd:

    def __init__(self):
        self.line = None
        self.picom = None
        self.autoscale = False

        self.window = tk.Tk()
        self.window.title("pyColorApp")
        self.window.grid_rowconfigure(0, weight=0)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.frame_control = tk.Frame(master=self.window, highlightthickness=1, highlightbackground="blue")
        self.frame_control.grid(row=0, column=0, sticky="ew")

        self.lbl = tk.Label(self.frame_control, text="Choose com port")
        self.lbl.grid(column=0, row=0, padx=4, pady=2)

        self.combo = Combobox(self.frame_control)
        self.combo.grid(column=1, row=0, padx=4)

        self.combo['values'] = PiCom.list_ports()
        self.combo.current(0)

        self.btnOpen = tk.Button(self.frame_control, text="Open com", command=self.clicked_open)
        self.btnOpen.grid(column=2, row=0, padx=4, pady=2)

        self.btnClose = tk.Button(self.frame_control, text="Close", command=self.clicked_close)
        self.btnClose.grid(column=3, row=0, padx=4, pady=2)

        self.btnStart = tk.Button(self.frame_control, text="Start", command=self.clicked_start)
        self.btnStart.grid(column=4, row=0, padx=4, pady=2)

        self.btnStop = tk.Button(self.frame_control, text="Stop", command=self.clicked_stop)
        self.btnStop.grid(column=5, row=0, padx=4, pady=2)

        self.btnTime = tk.Button(self.frame_control, text="Time", command=self.clicked_time)
        self.btnTime.grid(column=6, row=0, padx=4, pady=2)

        self.entTime = tk.Entry(self.frame_control)
        self.entTime.grid(column=7, row=0, padx=4, pady=2)

        self.frame_info = tk.Frame(master=self.window, highlightthickness=1, highlightbackground="blue")
        self.frame_info.grid(row=1, column=0, sticky="nsew")
        self.frame_info.grid_rowconfigure(0, weight=1)
        self.frame_info.grid_columnconfigure(0, weight=0)
        self.frame_info.grid_columnconfigure(1, weight=1)

        self.info = scrolledtext.ScrolledText(self.frame_info, width=30)
        self.info.grid(row=0, column=0, sticky="nsew")
        self.info.insert(END, "Hello!\n")

        self.frame_plot = tk.Frame(master=self.frame_info, highlightthickness=1, highlightbackground="blue")
        self.frame_plot.grid(row=0, column=1, sticky="nsew")

        self.fig = plt.Figure()

        self.aplot = self.fig.add_subplot(111)
        self.aplot.set_xlim([0, 258])
        self.aplot.set_ylim([0, 64000])
        self.aplot.autoscale(enable=False, axis='y', tight=True)
        self.aplot.grid()
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame_plot)
        toolbar = NavigationToolbar2Tk(self.canvas, self.frame_plot)
        button_expand = tk.Button(master=toolbar, text="E", command=self.clicked_expand)
        button_expand.pack(side="left")
        button_shrink = tk.Button(master=toolbar, text="S", command=self.clicked_shrink)
        button_shrink.pack(side="left")
        button_ascale = tk.Button(master=toolbar, text="A", command=self.clicked_ascale)
        button_ascale.pack(side="left")
        toolbar.update()

        self.fig.tight_layout(pad=1.0)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    def clicked_open(self):
        self.lbl.configure(text="Opening {}".format(self.combo.get()))
        self.picom = PiCom(self.combo.get(), self.append_info, self.update_plot)

    def clicked_close(self):
        if self.picom:
            self.picom.close()
            self.picom = None
            self.info.delete("1.0", END)

    def clicked_start(self):
        if self.picom:
            self.picom.start()
            t = np.arange(1, 256, 1)
            self.line = self.aplot.plot(t, 40000 * np.sin(2 * np.pi * t))[-1]

    def clicked_stop(self):
        if self.picom:
            self.picom.stop()

    def clicked_time(self):
        if self.picom:
            self.picom.set_time(self.entTime.get())

    def loop(self):
        self.window.mainloop()

    def closed(self):
        if self.picom:
            self.picom.close()

    def append_info(self, txt):
        self.info.insert(END, txt + '\n')

    def update_plot(self, data):
        self.info.insert(END, "Data " + str(len(data)) + '\n')
        if self.line:
            self.line.set_data(range(0, len(data)), data)
            if self.autoscale:
                l = min(data)
                h = max(data)
                d = (h - l) / 8
                l = l - d
                h = h + d
                self.aplot.set_ylim([l, h])
                self.autoscale = False
        self.canvas.draw()

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
        l = l + d
        h = h - d
        self.aplot.set_ylim([l, h])
        self.canvas.draw()

    def clicked_ascale(self):
        self.autoscale = True


if __name__ == '__main__':
    spw = SpectrWnd()
    spw.loop()
    spw.closed()

