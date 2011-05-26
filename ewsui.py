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
from wave import open as waveOpen
from ossaudiodev import open as ossOpen

gtk.gdk.threads_init()

class EwsWindow:
    def __init__(self, ewsmodel, ewsview):
        #setup main window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_title("Peringatan Dini Gempa")
        window.set_size_request(800, 500)
        window.set_icon_from_file('/usr/share/pixmaps/ews.png')
        window.connect("delete_event", self.delete_event)
        
        #setup model
        model = ewsmodel.get_model()
        #construct view
        view = ewsview.make_view(model)
        
        # Pack Box
        vbox       = gtk.VBox()
        box_body   = gtk.HBox()
        box_footer = gtk.HBox()
        box_footer_left = gtk.HBox()
        box_footer_right = gtk.HBox()
        
        box_body.pack_start(view)
        box_footer.pack_start(box_footer_left, False, True, 10)
        box_footer.pack_end(box_footer_right, False, True, 10)
        
        # Button
        close_button = gtk.Button("Tutup")
        close_button.connect("clicked", lambda w: gtk.main_quit())
        about_button = gtk.Button("Tentang")
        about_button.connect("clicked", self.show_about)
        
        # Label
        self.status_label = gtk.Label('Status : Tidak tersambung')
        
        # Pack Button
        box_footer_right.pack_end(close_button, False, True, 10)
        box_footer_right.pack_end(about_button, False, True, 10)
        box_footer_left.pack_end(self.status_label, False, True, 10)
        
        vbox.pack_start(box_body)
        vbox.pack_start(box_footer, False, False, 5)
        
        # Attatch to window
        window.add(vbox)
        window.show_all()
        return

    def show_about(self, widget):
        about = gtk.AboutDialog()
        about.set_program_name("Early Warning System")
        about.set_version("0.1")
        about.set_copyright("(c) Akhmat Safrudin 2011")
        about.set_website("http://www.airputih.or.id")
        about.run()
        about.destroy()
    
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
        self.coordinat = gtk.TreeViewColumn("Koordinat", self.renderer, text=2)
        self.magnitude = gtk.TreeViewColumn("Magnitude", self.renderer, text=3)
        self.depth     = gtk.TreeViewColumn("Kedalaman", self.renderer, text=4)
        self.region    = gtk.TreeViewColumn("Lokasi", self.renderer, text=5)
        self.potential = gtk.TreeViewColumn("Potensi", self.renderer, text=6)
        
        self.treeview.append_column(self.date)
        self.treeview.append_column(self.time)
        self.treeview.append_column(self.coordinat)
        self.treeview.append_column(self.magnitude)
        self.treeview.append_column(self.depth)
        self.treeview.append_column(self.region)
        self.treeview.append_column(self.potential)
        
        return self.treeview

class DesktopListner(IRCListner):
    def __init__(self, model=None, status=None):
        self.model = model
        self.status = status
        
    def on_connect(self):
        self.status.set_text('Status: Menyambungkan...')
        
    def on_welcome(self):
        self.status.set_text('Status: Tersambung')
        
    def on_join(self):
        self.status.set_text('Status: Aktif')
        
    def on_data(self, data, source):
        if source == 'airputih':
            store = self.model.get_model()
            self.model.prepend_model(store, data.strip().split('#'))
            self.alarm_gempa()
    
    def on_disconnected(self):
        self.status.set_text('Status: Tidak tersambung')
    
    def alarm_gempa(self):
        s = waveOpen('/usr/share/sounds/pyews/gempa.wav','rb')
        (nc,sw,fr,nf,comptype, compname) = s.getparams()
        dsp = ossOpen('/dev/dsp','w')
        
        try:
          from ossaudiodev import AFMT_S16_NE
        except ImportError:
          if byteorder == "little":
            AFMT_S16_NE = ossaudiodev.AFMT_S16_LE
          else:
            AFMT_S16_NE = ossaudiodev.AFMT_S16_BE
        
        dsp.setparameters(AFMT_S16_NE, nc, fr)
        data = s.readframes(nf)
        s.close()
        
        for i in range(1,5):
            dsp.write(data)

        dsp.close()
        
if __name__ == "__main__":
    Model   = EwsModel()
    View    = EwsView()
    EwsUI   = EwsWindow(Model, View)
    
    EwsUI.run()
