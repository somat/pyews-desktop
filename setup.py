#!/usr/bin/env python

from setuptools import setup

setup(name='pyews',
      version='1.0',
      py_modules=["ewsui", "ircclient"],
      data_files=[('/usr/bin', ['ews']),
                  ('/usr/share/bitmaps', ['data/ews.png']),
                  ('/etc', ['data/ews.conf']),
                  ('/usr/share/applications', ['data/ews.desktop']),
                  ('/usr/share/pyews', ['data/gempa.wav']),
                  ('/usr/share/pyews', ['data/tsunami.wav'])],
      install_requires=["pygtk >=2.0", "irclib >=0.4.8"],
      
      author = "Akhmat Safrudin",
      author_email = "somat@airputih.or.id",
      description = "Early Warning Disaster Information System",
      license = "GPL V3",
      keywords = "ews, python, pygtk",
      url = "http://www.airputih.or.id",
      )
