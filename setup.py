#!/usr/bin/env python
# Setup for MSWinCanvas

from distutils.core import setup

longdesc  =  """
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

Development versions of this module may be found on **Github** at:

https://github.com/Solomoriah/MSWinCanvas
"""

setup(
    name = "MSWinCanvas",
    version = "0.5",
    description = "MSWinCanvas",
    long_description = longdesc,
    author = "Chris Gonnerman",
    author_email = "chris@gonnerman.org",
    url = "http://newcenturycomputers.net/projects/mswinprint.html",
    py_modules = [ "MSWinCanvas" ],
    keywords = "windows printing",

    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows Server 2003",
        "Operating System :: Microsoft :: Windows :: Windows Server 2008",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows Vista",
        "Operating System :: Microsoft :: Windows :: Windows XP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Printing",
    ],
)

# end of file.
