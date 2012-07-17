# MSWinCanvas.py
# Copyright (c) 2004-2012 Chris Gonnerman
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.  Redistributions in binary
# form must reproduce the above copyright notice, this list of conditions and
# the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
    MSWinCanvas -- Reportlab Canvas emulation on Windows

    MSWinCanvas defines a class for use by programs needing to print complex
    output on Windows 2K/XP/2003 hosts.

    Canvas is a class for creating and running print jobs.  At present, it
    provides the subset of methods used by PollyReports, and some functions
    are incomplete or "stubbed."

    listprinters() returns a list of printer names.  The default printer is the 
    first element of the list, and all other printers follow in alphabetical order.

    desc(printer) returns a dictionary containing the descriptive fields
    for the named printer.  
"""

# "constants" for use with printer setup calls

HORZRES = 8
VERTRES = 10
LOGPIXELSX = 88
LOGPIXELSY = 90
PHYSICALWIDTH = 110
PHYSICALHEIGHT = 111

import win32gui, win32ui, win32print, win32con

try:
    from PIL import ImageWin
except:
    ImageWin = None

scale_factor = 20

prdict = None

paper_sizes = {
    "letter":       (1, (72*8.5, 72*11)),
    "lettersmall":  (2, (72*8.5, 72*11)),
    "tabloid":      (3, (72*11, 72*17)),
    "ledger":       (4, (72*17, 72*11)),
    "legal":        (5, (72*8.5, 72*14)),
#    "statement":    (6, (
    "executive":    (7, (72*7.25, 72*10.5)),
#    "a3":           (8, (
#    "a4":           (9, (
#    "envelope9":    (19, (
#    "envelope10":   (20, (
#    "envelope11":   (21, (
#    "envelope12":   (22, (
#    "envelope14":   (23, (
#    "fanfold":      (39, (
}

orientations = {
    "portrait":     1,
    "landscape":    2,
}

duplexes = {
    "normal":       1,
    "none":         1,
    "long":         2,
    "short":        3,
}

class Canvas:

    def __init__(self, printer = None, papersize = None, orientation = None, 
            duplex = None, desc = "MSWinCanvas.py print job"):

        self.dc = None
        self.font = None
        self.printer = printer
        self.papersize = papersize
        self.orientation = orientation
        self.page = 0
        self.duplex = duplex

        # open the printer
        if self.printer is None:
            self.printer = win32print.GetDefaultPrinter()
        self.hprinter = win32print.OpenPrinter(self.printer)

        # load default settings
        devmode = win32print.GetPrinter(self.hprinter, 8)["pDevMode"]

        # change paper size and orientation

        if self.papersize is None:
            self.papersize = "letter"

        devmode.PaperSize = paper_sizes[self.papersize][0]
        self._pagesize = paper_sizes[self.papersize][1]

        if self.orientation is None:
            self.orientation = "portrait"

        devmode.Orientation = orientations[self.orientation]
        if self.orientation == "landscape":
            self._pagesize = (self._pagesize[1], self._pagesize[0])

        if self.duplex is not None:
            devmode.Duplex = duplexes[self.duplex]

        # create dc using new settings
        self.hdc = win32gui.CreateDC("WINSPOOL", self.printer, devmode)
        self.dc = win32ui.CreateDCFromHandle(self.hdc)

        # self.dc = win32ui.CreateDC()
        # if self.printer is not None:
        #     self.dc.CreatePrinterDC(self.printer)
        # else:
        #     self.dc.CreatePrinterDC()

        self.dc.SetMapMode(win32con.MM_TWIPS) # 1440 per inch
        self.dc.StartDoc(desc)
        self.pen = win32ui.CreatePen(0, int(scale_factor), 0L)
        self.dc.SelectObject(self.pen)
        self.page = 1

    def drawAlignedString(self):
        pass

    def drawCentredString(self):
        pass

    def drawRightString(self):
        pass

    def drawString(self, x, y, text):
        self.dc.TextOut(scale_factor * x,
            -1 * scale_factor * y, text)

    def line(self, from_x, from_y, to_x, to_y):
        self.dc.MoveTo(self.scalepos((from_x, from_y)))
        self.dc.LineTo(self.scalepos((to_x, to_y)))

    def restoreState(self):
        pass

    def saveState(self):
        pass

    def setFont(self, name, size):
        wt = 400
        if name.endswith("-Bold"):
            wt = 700
            name = name[:-5]
        self.font = win32ui.CreateFont({
            "name": name,
            "height": scale_factor * size,
            "weight": wt,
        })
        self.dc.SelectObject(self.font)

    def setLineWidth(self, height):
        self.pen = win32ui.CreatePen(0, int(scale_factor*height), 0L)
        self.dc.SelectObject(self.pen)

    def setStrokeGray(self, gray):
        pass

    def showPage(self):
        if self.page == 0:
            return # nothing on the page
        self.dc.EndPage()
        self.page += 1

    def translate(self, *args):
        pass

    def scalepos(self, pos):
        rc = []
        for i in range(len(pos)):
            p = pos[i]
            rc.append(int(p * scale_factor))
        return tuple(rc)

    def close(self):
        if self.page == 0:
            return # document was never started
        self.dc.EndDoc()
        del self.dc


def build_dict():
    global prdict
    lst = win32print.EnumPrinters(
        win32print.PRINTER_ENUM_CONNECTIONS
        + win32print.PRINTER_ENUM_LOCAL)
    prdict = {}
    for flags, description, name, comment in lst:
        prdict[name] = {}
        prdict[name]["flags"] = flags
        prdict[name]["description"] = description
        prdict[name]["comment"] = comment

def listprinters():
    dft = win32print.GetDefaultPrinter()
    if prdict is None:
        build_dict()
    keys = prdict.keys()
    keys.sort()
    rc = [ dft ]
    for k in keys:
        if k != dft:
            rc.append(k)
    return rc

def desc(name):
    if prdict == None:
        listprinters()
    return prdict[name]


# end of file.
