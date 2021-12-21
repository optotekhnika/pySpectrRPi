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
import tables as pt


class PlotElement(tk.Frame):
    def __init__(self, masterFrame, spwnd, r_var, val, comment, color, plot):
        super().__init__(masterFrame.frame, highlightthickness=1, highlightbackground="blue")

        self.color = color
        self.is_hidden = False
        self.spwnd = spwnd
        self.plot = plot
        self.masterFrame = masterFrame
        self.comment = comment

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)

        self.btnHide = tk.Button(self, text=" ", command=self.hide, bg=color, activebackground=color)
        self.btnHide.grid(column=0, row=0, padx=4, pady=0, sticky="ew")

        self.rad = tk.Radiobutton(self, variable=r_var, value=val)
        self.rad.grid(column=1, row=0, sticky="ew")

        self.lbl = tk.Label(self, text=comment)
        self.lbl.grid(column=2, row=0, padx=4, sticky="ew")
        self.lbl.bind("<Button-3>", self.popup_menu)

        self.btnExpand = tk.Button(self, text="X", command=self.expand)
        self.btnExpand.grid(column=3, row=0, padx=4, pady=0, sticky="ew")

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Expand", command=self.expand)
        self.menu.add_command(label="Hide", command=self.hide)
        self.menu.add_command(label="Comment", command=self.menu_comment)
        self.menu.add_command(label="Delete", command=self.menu_delete)
        self.menu.add_command(label="Export", command=self.menu_export)

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

    def menu_comment(self):
        comment = simpledialog.askstring("Comment", "Commentary", parent=self.masterFrame, initialvalue=self.comment)
        if comment:
            self.comment = comment
            self.lbl['text'] = comment

    def menu_delete(self):
        self.grid_forget()
        self.masterFrame.delete(self)

    def menu_export(self):
        print("export")

    def popup_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root, 0)


class TableRow(pt.IsDescription):
    comment = pt.StringCol(128)
    x = pt.Int32Col(256)
    y = pt.Int32Col(256)


class PlotListWnd(tk.Frame):
    def __init__(self, mainframe, spwnd):
        super().__init__(mainframe, highlightthickness=1, highlightbackground="blue")

        self.spwnd = spwnd
        self.list = []
        self.r_var = tk.IntVar()

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=self.frame.winfo_width())

    def add_plot(self, plot, color, comment="Plot",):
        r = len(self.list)
        p = PlotElement(self, self.spwnd, self.r_var, r, comment=comment, color=color, plot=plot)
        p.grid(column=0, row=r, sticky="ew")
        self.r_var.set(r)
        self.list.append(p)

    def delete(self, pl):
        self.list.remove(pl)
        self.spwnd.del_plot(pl.plot)

    def save(self):
        n = len(self.list)
        h5file = pt.open_file("spw.h5", mode="w", title="spectrum")
        group = h5file.create_group("/", "simple", "Single spectrum")
        table = h5file.create_table(group, "sp", TableRow, "spectrum")
        sprow = table.row
        for i in range(n):
            x, y = self.spwnd.xy_plot(self.list[i].plot)
            sprow['x'] = x
            sprow['y'] = y
            sprow['comment'] = self.list[i].comment
            sprow.append()
        table.flush()
        h5file.close()

    def restore(self):
        h5file = pt.open_file("spw.h5", mode="r", title="spectrum")
        table = h5file.root.simple.sp
        for pl in table.iterrows():
            p, c = self.spwnd.add_plot(pl['x'], pl['y'])
            self.add_plot(p, c, pl['comment'])
        h5file.close()

