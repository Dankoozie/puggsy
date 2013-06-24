from socket import *
import threading
import contacts, struct, time
import binascii
import messages,tp

from myself import Myself

first_broadcast = True
transport_trusted = True

#Set up socket stuff
sock = socket(AF_INET6, SOCK_DGRAM)
bcast_addr = "ff02::1"
bcast_port = 49091
listen_port = 49091
bcast_time = 15
bcast_remove_factor = 3.1
bcast_running = True
listen_running = True
sock.bind(('',listen_port))

lan_uid = Myself.l_uid
Myself.Transports['lan'] = 1


class Lan_Contact():
    def __init__(self,ip,port,interval):
        self.ip = ip
        self.port = port
        self.lastseen = time.time()
        self.bcast_interval = interval

def lci(mc):
    return contacts.Contactlist[mc].Transport['lan']

#Process LAN presence broadcast packet ('B<lan_uid><nickname>')    
def process_broadcast(addr,packet):
    uid = packet[3:27]
    interval = packet[1]
    #Flags (lsb=presence,1=bcast_request)
    flags = int(packet[2])
    status = flags & 1
    bcast_request = flags & 2
    nick = str(packet[27:],'UTF-8')

    LTO = Lan_Contact(addr[0],addr[1],interval)
    
    #Ignore packets from self 
    if(uid == lan_uid): return
    #print("Incoming broadcast\n Nick:" + str(nick,'UTF-8') + "\nUID: " + str(binascii.hexlify(uid),'utf-8'))
    getmain = contacts.contact_by_li(uid)

    if (getmain == -1):
       #Create a brand new contact from scratch
       Contactobject = contacts.Contact(nick,status)
       Contactobject.li = uid
    else:
       Contactobject = contacts.Contactlist[getmain]

    #Add LAN transport to this object
    Contactobject.Transports['lan'] = LTO
    Contactobject.nick = nick
    Contactobject.presence = status
    Contactobject.ui_update()
    if(bcast_request): bcast_send() # Notify new peer that you are around

#Process Unsecured LAN message('M<sender lan_uid><message>')        
def process_unsecuredmsg(addr,packet):
    peer = peer_by_lan_ipport(addr[0],addr[1])
    print("Unsec msg incoming")
    if(peer != -1):
        #Attributes of received message
        Msg = contacts.Message_in(peer,packet[3:],"lan")
        Msg.time_received = time.time()
        Msg.timeout = 255
        Msg.security = 0
        Msg.seqid = struct.unpack("H",packet[1:3])[0]
        print(Msg.seqid)
        messages.process_message(Msg)
    else: print("[BOGUS]: Message received from unknown peer")

#Process 'sign off' packet
def process_signoff(addr,packet):
    getmain = contacts.contact_by_li(packet[1:25])
    if(getmain != -1):
        contacts.Contactlist[getmain].del_transport("lan")
        print("Peer signing off")


def process_transport_list(addr,packet):
    pass
    #peer = contacts.contact_by_li
    #if(peer in lan_contacts):
    #    print(packet[25:])
    #    depickle = packet[25:]
        

def process_info(addr,packet):
    return True

def process_securedmsg(addr,packet):
    return True
    
#Handles incoming UDP packet
def process_received(addr, packet):
    pack_switch = {65:process_ack,
                   66:process_broadcast,
                   73:process_info,
                   83:process_securedmsg,
                   84:process_transport_list,
                   85:process_unsecuredmsg,
                   89:process_signoff}

    try:
        pack_switch[int(packet[0])](addr,packet)
    except KeyError:
        print("[BOGUS]: Invalid start byte " + str(int(packet[0])))
    
#Process incoming delivery receipt        
def process_ack(addr,packet):
    seqid = struct.unpack("H",packet[1:3])[0]
    peer = peer_by_lan_ipport(addr[0],addr[1])
    if(peer != -1):
        messages.process_ack(peer,"lan",seqid)
    else: print("[BOGUS]: Delivery report (peer does not exist)")
    
#Send single presence broadcast (for use when one is received)
def bcast_send():
        global first_broadcast
        flags = ( (int(first_broadcast) << 1) + int(Myself.presence) ) 
        hdr = struct.pack("BBB",66,bcast_time,flags)
        sock.sendto(hdr + lan_uid + bytes(Myself.nick,'UTF-8'),(bcast_addr,bcast_port))    
        first_broadcast = False

def bcast():
    if(bcast_running):
        checktimeouts()
        bcast_send()
        threading.Timer(bcast_time,bcast).start()

def send_msg(mc,seq,msg):
    lc = mc.Transports['lan']
    hdr = struct.pack("B",85) + struct.pack("H",seq) + msg
    print("Sending unsec msg \n Addr:" + lc.ip +"\n Port:" + str(lc.port))
    sock.sendto(hdr,(lc.ip,lc.port))

def send_ack(mc,seq):
    lc = contacts.Contactlist[mc].Transports['lan']
    hdr = struct.pack("B",65) + struct.pack("H",seq)
    sock.sendto(hdr,(lc.ip,lc.port))

def checktimeouts():
    tdel = []
    c_w_lan = contacts.all_with_transport('lan')
    if(c_w_lan == []): return True
    for lc in c_w_lan:
        cur_contact = contacts.Contactlist[lc].Transports['lan']
        if((time.time() - cur_contact.lastseen) > (bcast_time * bcast_remove_factor)):
            tdel.append(lc)
            print(tdel)
    for lc in tdel: contacts.Contactlist[lc].del_transport('lan')

def peer_by_lan_ipport(ip,port):
    c_w_lan = contacts.all_with_transport('lan')
    if(c_w_lan == []): return True
    for lc in c_w_lan:
        if(contacts.Contactlist[lc].Transports['lan'].ip == ip and contacts.Contactlist[lc].Transports['lan'].port == port): return lc
    return -1


def Shutdown():
    global bcast_running,listen_running
    bcast_running = False
    listen_running = False
    #Tell other clients you are going offline
    sock.sendto(struct.pack("B",89) + lan_uid,(bcast_addr,bcast_port))

    
class listen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.recvd = 0
    def run(self):
        while listen_running:
            data, addr = sock.recvfrom(1024)
            process_received(addr, data)
bcast()
listener = listen()
listener.start()
