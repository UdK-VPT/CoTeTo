#!/usr/bin/env python

from distutils.core import setup

setup(name='CoTeTo',
      version='0.99',
      description='Code Templating Tool - code generation framework based on templates',
      author='Joerg Raedler (UdK Berlin)',
      author_email='jraedler@udk-berlin.de',
      url='https://github.com/UdK-VPT/CoTeTo',
      # contents
      packages=['CoTeTo', 'CoTeTo.Loaders'],
      package_data={'CoTeTo': ['res/*']},
      scripts=['scripts/CoTeTo-cli.py', 'scripts/CoTeTo-gui.py'],
      # dependencies
      install_requires=['mako', 'jinja2', 'PyQt5'],
      # classifiers
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Environment :: Win32 (MS Windows)",
          "Environment :: X11 Applications :: Qt",
          "Environment :: MacOS X",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: POSIX :: Linux",
          "Operating System :: MacOS :: MacOS X",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Intended Audience :: Science/Research",
          "Topic :: Software Development :: Code Generators",
          "Topic :: Scientific/Engineering",
          "Topic :: Utilities"
      ],
      )
