#!/usr/bin/python

#!/usr/bin/python


import os
import shutil
import sys

from distutils.core import setup
from distutils.cmd import Command
import py2exe #pylint: disable=F0401
import py2exe.build_exe #pylint: disable=F0401
import win32com

# Hack the python path so that py2exe can find win32com.shell
import py2exe.mf as modulefinder #pylint: disable=F0401
for p in win32com.__path__[1:]:
    modulefinder.AddPackagePath('win32com', p)
    for extra in ['win32com.shell']:
        __import__(extra)
        m = sys.modules[extra]
        for p in m.__path__[1:]:
            modulefinder.AddPackagePath(extra, p)

if __name__ == '__main__':
    # Clear the dist folder
    if os.path.isdir('dist'):
        shutil.rmtree('dist', 0)

    python_dir = os.path.dirname(sys.executable)
    pyqt_plugins = os.path.join(python_dir, 'lib', 'site-packages', 'PyQt4', 'plugins')
    ico_file = os.path.join(pyqt_plugins, 'imageformats', 'qico4.dll')
    gif_file = os.path.join(pyqt_plugins, 'imageformats', 'qgif4.dll')
    phonon_file = os.path.join(pyqt_plugins, 'phonon_backend', 'phonon_ds94.dll')
    # NOTE: company_name is required for Windows 8 default program registration.
    setup(name = 'FullscreenBrowser',
          description = 'FullscreenBrowser',
          author = 'Josh Nisly',
          options = {'py2exe':
                     {'excludes': ['pywin', 'pywin.debugger', 'pywin.debugger.dbgcon',
                                  'pywin.dialogs', 'pywin.dialogs.list',
                                  'Tkconstants','Tkinter','tcl',],
                      'packages': ['encodings'],
                      'includes': ['sip'],
                      'dll_excludes': [
                        'w9xpopen.exe',
                        'mswsock.dll',
                        'powrprof.dll',
                        'API-MS-Win-Core-ErrorHandling-L1-1-0.dll',
                        'API-MS-Win-Core-File-L1-1-0.dll',
                        'API-MS-Win-Core-Handle-L1-1-0.dll',
                        'API-MS-Win-Core-Interlocked-L1-1-0.dll',
                        'API-MS-Win-Core-IO-L1-1-0.dll',
                        'API-MS-Win-Core-LocalRegistry-L1-1-0.dll',
                        'API-MS-Win-Core-Misc-L1-1-0.dll',
                        'API-MS-Win-Core-ProcessThreads-L1-1-0.dll',
                        'API-MS-Win-Core-Profile-L1-1-0.dll',
                        'API-MS-Win-Core-String-L1-1-0.dll',
                        'API-MS-Win-Core-SysInfo-L1-1-0.dll',
                        'API-MS-Win-Security-Base-L1-1-0.dll',
                        'WTSAPI32.dll',
                        ],
                      'bundle_files': 3}},
          data_files = [('phonon_backend', [phonon_file]),
                        ('imageformats', [ico_file, gif_file])],
          windows = [{'script':'main.py',
                      'dest_base':'FullscreenBrowser',
                      #'icon_resources':[(1,'InvLinkWeb.ico')],
                      'company_name': 'Josh Nisly',
                     }],
          )

