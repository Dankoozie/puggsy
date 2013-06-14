#!/usr/bin/python3

from gi.repository import Gtk,Pango
from gi.repository import GObject
from gi.repository import GdkPixbuf
GObject.threads_init()

import contacts
import messages

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


def set_transports_combo():
    transport_list.clear()

    if len(contacts.Contactlist) == 0:
        return False
    
    for a in contacts.Contactlist[contacts.Selected].Transports:
        transport_list.append([a,pixbuf_lan])
        print(a)
    transport_list.append(["Bluetooth",pixbuf_bt])
def tvs_changed(blah):
    (m,p) = blah.get_selected_rows()
    #Multi select possible
    for path in p:
        tree_iter = m.get_iter(path)
        value = m.get_value(tree_iter,0)
        contacts.Selected = value
        sendinfo.set_text("Destination: " + contacts.Contactlist[value].nick)

    set_transports_combo()
    
def sendmsg(blah):
    messages.send_message(contacts.Selected,"lan",None,sb.get_text())

def msgbox_keypress(widge,event):
    if(event.keyval == 65293):
       messages.send_message(contacts.Selected,"lan",None,sb.get_text()) 
       sb.set_text("")

#End GUI handlers
    
builder = Gtk.Builder()
builder.add_from_file("bakelite.glade")
window = builder.get_object("window1")
entry = builder.get_object("entry1")
tv = builder.get_object("contacts_tree")
sb = builder.get_object("sendbox")
sendinfo = builder.get_object("sendinfo")
Yourname_box = builder.get_object("yourname")

sel = tv.get_selection()

mview = builder.get_object("msgview")
mview.set_buffer(messages.buffy)

messages.tb = mview

#Pixbuf
pixbuf_lan = GdkPixbuf.Pixbuf.new_from_file_at_size("./graphics/lan.png",16,16)
pixbuf_bt = GdkPixbuf.Pixbuf.new_from_file_at_size("./graphics/bt.png",16,16)

#Transport select box
transport_select = builder.get_object("sel_transport")
transport_list = Gtk.ListStore(str,GdkPixbuf.Pixbuf)
transport_select.set_model(transport_list)

tpl_cell = Gtk.CellRendererText()
tpl_pcell = Gtk.CellRendererPixbuf()

transport_select.pack_start(tpl_cell,True)
transport_select.pack_start(tpl_pcell,False)
transport_select.add_attribute(tpl_cell,'text',0)
transport_select.add_attribute(tpl_pcell,'pixbuf',1)

#GUI items for module 'contacts'
contacts.Builder = builder
contacts.Sel_lbl = sendinfo
contacts.Selbox = tv

#GUI items for module 'messages'
messages.Mainwindow = window

#GUI items for contact details
tp_c = Gtk.TreeViewColumn("Transports")
transport_treeview = builder.get_object("wcd_transports_tv")
transport_treeview.append_column(tp_c)
transport_treeview.set_model(contacts.tp_l)
cell = Gtk.CellRendererText()
tp_c.pack_start(cell,True)
tp_c.add_attribute(cell,'text',0)


#Settings objects

Yourname_box.set_text(contacts.Myself.nick)

#Contacts list set-up
collem = Gtk.TreeViewColumn('Contacts')
tv.append_column(collem)

cell = Gtk.CellRendererText()
presence_cell = Gtk.CellRendererPixbuf()

collem.pack_start(presence_cell,False)
collem.pack_start(cell,True)
collem.add_attribute(cell,'text',1)
collem.add_attribute(presence_cell,'pixbuf',2)

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

