"""Lever frame for controlling JMRI-based yard."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import tkinter as tk

HOST = ''
PORT = 1


class LeverFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.one = Lever(self, "1", 'red', 1)
        self.two = Lever(self, "2", 'grey', 2, {'one': 'bw', 'three': 'off'})
        self.three = Lever(self, "3", 'grey', 3, {'one': 'bw', 'two': 'off'})
        self.four = Lever(self, "4", 'white', 4, {'one': 'bw', 'five': 'off'})
        self.five = Lever(self, "5", 'white', 5, {'one': 'bw', 'four': 'off'})

        self.grid()


class Lever(object):
    def __init__(self, master, text, colour, column, locking={}):
        self.master = master
        self.locking = locking

        self.state = tk.BooleanVar()
        self.state.set(True)
        lever = tk.Checkbutton(master, text=text, bg=colour, height=15, width=2,
                               selectcolor=colour, indicatoron=False,
                               variable=self.state,
                               activebackground=colour, command=self.throw)
        lever.grid(row=0, column=column)

    def throw(self, button=True):
        """Change position of lever if not locked."""
        # Check if this has been called by a button GUI press.
        if button:
            # Reset state after a GUI button press so we can enforce locking.
            self.state.set(not self.state.get())

        for name, position in self.locking.iteritems():
            item = getattr(self.master, name)
            if position == "bw" and not item.state.get():
                print("Locked by %s being reverse" % name)
                return
            elif position == "off" and not item.state.get() and self.state.get():
                print("Locked normal by %s being reverse" % name)
                return

        self.state.set(not self.state.get())


if __name__ == '__main__':
    app = LeverFrame()
    app.mainloop()
