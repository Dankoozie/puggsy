from gi.repository import Gtk
import contacts
import transport_lan

tb = None

Inbox = {}
Pending = {}
Sentbox = {}
Archived = {}

buffy = Gtk.TextBuffer()

def process_ack(maincontact,transport,seqid):
    pass

def process_message(Msg_obj):
    print("Unsecured msg received")
    enditer = buffy.get_end_iter()
    tx = "Message from: " + contacts.Contactlist[Msg_obj.mc].nick + " Transport: " + Msg_obj.transport + "\n" + str(Msg_obj.contents,'UTF-8') + "\n\n"
    print(tx)
    buffy.insert(enditer,tx)
    tb.scroll_to_mark(buffy.get_insert(),0,False,0.5,0.5)
    
def send_message(maincontact,transport,sec,body):
    if not (maincontact in contacts.Contactlist): return False
    transport_lan.sendmsg(contacts.Contactlist[maincontact],body)
