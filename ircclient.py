#!/usr/bin/env python
#
# IRC Client
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

from random import choice
import string
from irclib import SimpleIRCClient, ServerConnectionError, nm_to_n, is_channel

class IRCListner(object):
    def on_data(self, data, source):
        """Called when new data arrives"""
        return
    
    def on_connected(self):
        """Called when connected"""
        return
    
    def on_disconnected(self):
        """Called when disconnected"""
        return

class IRCClient(SimpleIRCClient):
    def __init__(self, config, listner):
        SimpleIRCClient.__init__(self)
        self.server = config['irc']['server']
        self.port = 6667
        self.nickname = self._generate_nick()
        self.channel = config['irc']['channel']
        self.listner = listner
    
    def on_welcome(self, connection, event):
        self.listner.on_connected()
        if is_channel(self.channel):
            connection.join(self.channel)
        else:
            sys.exit(1)

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")
    
    def on_disconnect(self, connection, event):
        self.listner.on_disconnected()
        self.connection.execute_delayed(0, self._reconnect)
    
    def on_pubmsg(self, connection, event):
        self.listner.on_data(event.arguments()[0], nm_to_n(event.source()))
    
    def _generate_nick(self):
        nick = ''.join([choice(string.letters + string.digits) for i in range(10)])
        return nick
    
    def _connect(self):
        try:
            self.connect(self.server, self.port, self.nickname)
        except ServerConnectionError, x:
            print x
            sys.exit(1)
    
    def _reconnect(self):
        if not self.connection.is_connected():
            self.connect(server, port, nickname)
    
    def start(self):
        self.ircobj.process_once()

