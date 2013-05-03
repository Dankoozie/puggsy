from gi.repository import Gtk
import contacts
import transport_lan

tb = None


buffy = Gtk.TextBuffer()

#def blah():
#    enditer = buffy.get_end_iter()
 #   buffy.insert(enditer,"Gbshite")

def process_message(maincontact,transport,sec,body):
    print("Unsecured msg received")
    enditer = buffy.get_end_iter()
    tx = "Message from: " + contacts.Contactlist[maincontact].nick + " Transport: " + transport + "\n" + str(body,'UTF-8') + "\n\n"
    print(tx)
    buffy.insert(enditer,tx)
    tb.scroll_to_mark(buffy.get_insert(),0,False,0.5,0.5)
    
def send_message(maincontact,transport,sec,body):
    if not (maincontact in contacts.Contactlist): return False
    transport_lan.sendmsg(contacts.Contactlist[maincontact],body)
