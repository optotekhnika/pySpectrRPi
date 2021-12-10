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

from json import JSONDecodeError
from threading import Thread
from serial import Serial
import serial.tools.list_ports
import json


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
