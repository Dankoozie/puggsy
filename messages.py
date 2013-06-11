from gi.repository import Gtk
import contacts
import transport_lan
import notification

from random import randint

tb = None
Mainwindow = None

Inbox = {}
Pending = [] #Contacts with pending messages
Sentbox = {}
Archived = {}

buffy = Gtk.TextBuffer()

def gen_seqid(mc):
    sp = contacts.Contactlist[mc].Messages_pending
    for i in range(0,65535):
        if(not (i in sp)): return i

def send_ack(Msg_obj):
    transport_lan.send_ack(Msg_obj.mc,Msg_obj.seqid)

def process_ack(maincontact,transport,seqid):
    mc = contacts.Contactlist[maincontact]
    if(seqid in mc.Messages_pending):
        del(mc.Messages_pending[seqid])
        print("Message sequence " + str(seqid) + " delivered")
    else: print("[BOGUS]: Message identifier invalid")

def process_message(Msg_obj):
    print("Unsecured msg received")
    enditer = buffy.get_end_iter()
    tx = "Message from: " + contacts.Contactlist[Msg_obj.mc].nick + " Transport: " + Msg_obj.transport + "\n" + str(Msg_obj.contents,'UTF-8') + "\n\n"
    print(tx)
    buffy.insert(enditer,tx)
    tb.scroll_to_mark(buffy.get_insert(),0,False,0.5,0.5)

    #Send receipt
    send_ack(Msg_obj)

    #Notify
    notification.sys_beep()
    #Mainwindow.set_urgency_hint(True)
    
def send_message(maincontact,transport,sec,body):
    if not (maincontact in contacts.Contactlist): return False
    seqid = gen_seqid(maincontact)
    contacts.Contactlist[maincontact].Messages_pending[seqid] = body
    transport_lan.sendmsg(contacts.Contactlist[maincontact],body,seqid)
    
