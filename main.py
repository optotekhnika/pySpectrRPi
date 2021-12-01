import tkinter as tk
from threading import Thread
from tkinter.ttk import Combobox
from tkinter import scrolledtext, END
from serial import Serial
import serial.tools.list_ports
import json


def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class PiCom:
    def __init__(self, port_name, post_info):
        self.serialport = Serial(port_name, 115200, parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        bytesize=serial.EIGHTBITS, timeout=5)

        self.on = True
        self.thread_loop = Thread(target=self.__listen_loop)
        self.thread_loop.start()
        self.post_info = post_info

    @staticmethod
    def list_ports():
        ports = serial.tools.list_ports.comports()
        comboports = []
        for port, desc, hwid in sorted(ports):
            comboports.append(port)
        return comboports

    def close(self):
        self.serialport.close()

    def __listen_loop(self):
        print("Start loop!")
        while self.on:
            try:
     #           bts = self.serialport.readline()
     #           if len(bts) == 0:
     #               continue
     #           print(bts.decode('utf-8'))
                j = json.load(self.serialport)
                if j["info"]:
                    self.post_info(j["info"])
            except TypeError:
                print("Type error on port")

    def start(self):
        self.serialport.write("{\"cmd\":\"getline\"}\r\n".encode())

    def stop(self):
        self.serialport.write("stop".encode)


class SpectrWnd:

    def __init__(self):
        self.picom = None

        self.window = tk.Tk()
        self.window.title("pyColorApp")
        self.window.grid_rowconfigure(0, weight=0)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.frame_control = tk.Frame(master=self.window, highlightthickness=1, highlightbackground="blue")
        self.frame_control.grid(row=0, column=0, sticky="ew")

        self.lbl = tk.Label(self.frame_control, text="Choose com port")
        self.lbl.grid(column=0, row=0)

        self.combo = Combobox(self.frame_control)
        self.combo.grid(column=1, row=0)

        self.combo['values'] = PiCom.list_ports()
        self.combo.current(0)

        self.btnOpen = tk.Button(self.frame_control, text="Open com", command=self.clicked_open)
        self.btnOpen.grid(column=2, row=0)

        self.btnClose = tk.Button(self.frame_control, text="Close", command=self.clicked_close)
        self.btnClose.grid(column=3, row=0)

        self.btnStart = tk.Button(self.frame_control, text="Start", command=self.clicked_start)
        self.btnStart.grid(column=4, row=0)

        self.btnStop = tk.Button(self.frame_control, text="Stop", command=self.clicked_stop)
        self.btnStop.grid(column=5, row=0)

        self.frame_info = tk.Frame(master=self.window, highlightthickness=1, highlightbackground="blue")
        self.frame_info.grid(row=1, column=0, sticky="nsew")

        self.info = scrolledtext.ScrolledText(self.frame_info)
        self.info.pack(expand=True, fill='both')
        self.info.insert(END, "Hello!\n")

    def clicked_open(self):
        self.lbl.configure(text="Opening {}".format(self.combo.get()))
        self.picom = PiCom(self.combo.get(), self.append_info)

    def clicked_close(self):
        self.picom.close()
        self.picom = None

    def clicked_start(self):
        if self.picom:
            self.picom.start()

    def clicked_stop(self):
        if self.picom:
            self.picom.stop()

    def loop(self):
        self.window.mainloop()

    def closed(self):
        if self.picom:
            self.picom.close()

    def append_info(self, txt):
        self.info.insert(END, txt + '\n')


if __name__ == '__main__':
    print_hi('PyCharm')

    spw = SpectrWnd()
    spw.loop()
    spw.closed()

