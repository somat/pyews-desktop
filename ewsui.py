#!/usr/bin/env python
#
# Main User Interface
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

import pygtk
pygtk.require('2.0')
import gtk, gobject
from ircclient import IRCListner

gtk.gdk.threads_init()

class EwsWindow:
    def __init__(self, ewsmodel, ewsview):
        #setup main window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Peringatan Dini Gempa")
        self.window.set_size_request(650, 500)
        self.window.connect("delete_event", self.delete_event)
        
        #setup model
        self.model = ewsmodel.get_model()
        #construct view
        self.view = ewsview.make_view(self.model)
        #attatch to window
        self.window.add(self.view)
        self.window.show_all()
        return
    
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False
    
    def run(self):
        gtk.main()
        return

class EwsModel:
    def __init__(self):
        self.treestore = gtk.TreeStore( gobject.TYPE_STRING, gobject.TYPE_STRING,
                                        gobject.TYPE_STRING, gobject.TYPE_STRING,
                                        gobject.TYPE_STRING)
        return
    
    def get_model(self):
        if self.treestore:
            return self.treestore
        else:
            return None
            
    def prepend_model(self, model, data):
        model.prepend(None, data)
        return

class EwsView:
    def make_view(self, model):
        self.treeview = gtk.TreeView(model)

        self.renderer   = gtk.CellRendererText()

        self.date      = gtk.TreeViewColumn("Tanggal", self.renderer, text=0)
        self.time      = gtk.TreeViewColumn("Jam", self.renderer, text=1)
        self.magnitude = gtk.TreeViewColumn("Magnitude", self.renderer, text=2)
        self.location  = gtk.TreeViewColumn("Lokasi", self.renderer, text=3)
        self.depth     = gtk.TreeViewColumn("Kedalaman", self.renderer, text=4)
        
        self.treeview.append_column(self.date)
        self.treeview.append_column(self.time)
        self.treeview.append_column(self.magnitude)
        self.treeview.append_column(self.location)
        self.treeview.append_column(self.depth)
        
        return self.treeview

class DesktopListner(IRCListner):

    def __init__(self, model=None):
        self.model = model
        return
        
    def on_data(self, data, source):
        if source == 'airputih':
            store = self.model.get_model()
            self.model.prepend_model(store, data.strip().split('#'))
        return
    
    def on_connected(self):
        print "Connected"
        return
    
    def on_disconnected(self):
        print "Disconnected"
        return

