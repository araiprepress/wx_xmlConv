from distutils.core import setup
import py2exe
 
includes = ['lxml.etree', 'lxml._elementpath', 'gzip']
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']
packages = []
#dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll','tk84.dll']
dll_excludes = ['MSVCP90.dll', 'HID.DLL', 'tcl84.dll','w9xpopen.exe']

setup(
    options = {"py2exe": {"compressed": 2, 
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 3,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },
    windows=[{'script':'wxConv.py', 
              'icon_resources':[(1, 'icoXmlXslt4.ico')]}]
#    windows=[{'script':'wxConv_min.py', 
#              'icon_resources':[(1, 'icoXmlXsltMin4.ico')]}]
)