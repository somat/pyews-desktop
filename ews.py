#!/usr/bin/env python
#
# Main Program
#
# Akhmat Safrudin <somat@airputih.or.id>

"""
    Early Warning Disaster Information System
    Copyright (C) <2011>  Akhmat Safrudin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from ewsui import EwsModel, EwsView, EwsWindow, DesktopListner
from ircclient import IRCClient
from configobj import ConfigObj

import threading
import time
import gobject

gobject.threads_init()

class EwsThread(threading.Thread):
    def __init__(self, conn):
        super(EwsThread, self).__init__()
        self.conn = conn
        self.quit = False
        
    def conn_start(self):
        self.conn.start()
        return False
        
    def run(self):
        self.conn._connect()
        while not self.quit:
            gobject.idle_add(self.conn_start)
            time.sleep(0.1)

if __name__ == "__main__":
    config = ConfigObj('/etc/ews.conf')
    
    Model   = EwsModel()
    View    = EwsView()
    EwsUI   = EwsWindow(Model, View)
    Listner = DesktopListner(Model)
    
    
    conn = IRCClient(config, Listner)
    ews = EwsThread(conn)
    ews.start()
    EwsUI.run()
    ews.quit = True
    
