#!/usr/bin/python3

from gi.repository import Gtk,Pango
from gi.repository import GObject
GObject.threads_init()

import contacts
import messages

import fivebit

import transport_lan
#import transport_serial
#import transport_bluetooth
import transport_udp4_direct
#import transport_tcp_direct
#import transport_udp_storeforward
#import transport_http_storeforward
##import transport_nfc
##import transport_ar
##import transport_sms
##import transport_sbd
##import transport_torchat

#GUI handlers

def Kwitt(blah,larg):
    print("Kwitting!")
    transport_lan.Shutdown()
    Gtk.main_quit()
 
def nick_changed(entry):
    contacts.Myself.nick = Yourname_box.get_text()
    
def tvs_changed(blah):
    (m,p) = blah.get_selected_rows()
    #Multi select possible
    for path in p:
        tree_iter = m.get_iter(path)
        value = m.get_value(tree_iter,1)
        contacts.Selected = value
        sendinfo.set_text("Destination: " + contacts.Contactlist[value].nick)

def sendmsg(blah):
    messages.send_message(contacts.Selected,"lan",None,sb.get_text())

def msgbox_keypress(widge,event):
    if(event.keyval == 65293):
       messages.send_message(contacts.Selected,"lan",None,sb.get_text()) 
       sb.set_text("")
    #else:
       # print(len(fivebit.encode3(sb.get_text())),len(zlib.compress(bytes(sb.get_text(),'UTF-8'),9)),len(sb.get_text())) 

#End GUI handlers
    
builder = Gtk.Builder()
builder.add_from_file("bakelite.glade")
window = builder.get_object("window1")
entry = builder.get_object("entry1")
tv = builder.get_object("contacts_tree")
sb = builder.get_object("sendbox")
sendinfo = builder.get_object("sendinfo")
collem = Gtk.TreeViewColumn('Contacts')
Yourname_box = builder.get_object("yourname")

sel = tv.get_selection()

mview = builder.get_object("msgview")
mview.set_buffer(messages.buffy)

messages.tb = mview


#GUI items for module 'contacts'
contacts.Builder = builder
contacts.Sel_lbl = sendinfo
contacts.Selbox = tv

#GUI items for module 'messages'
messages.Mainwindow = window

#Settings objects

Yourname_box.set_text(contacts.Myself.nick)

tv.append_column(collem)
cell = Gtk.CellRendererText()

collem.pack_start(cell,True)
collem.add_attribute(cell,'text',0)

tv.set_model(contacts.gui_contactlist)

window.show_all()

handlers = {
    "onDeleteWindow": Kwitt,
    "nick_change": nick_changed,
    "on_treeview-selection_changed": tvs_changed,
    "kpress": msgbox_keypress,
    "contact_showdetails": contacts.gui_showdetails,
    "wcd_close": contacts.wcd_close
}
builder.connect_signals(handlers)

Gtk.main()

