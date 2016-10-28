from socket import *
import threading
import contacts, struct, time
import binascii
import messages,tp

from myself import Myself

first_broadcast = True
transport_trusted = True

#Log level
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

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
    if(uid == lan_uid):
        logging.debug("LAN: Own broadcast received")
        return
    
    #print("Incoming broadcast\n Nick:" + str(nick,'UTF-8') + "\nUID: " + str(binascii.hexlify(uid),'utf-8'))
    getmain = contacts.contact_by_li(uid)

    if (getmain == -1):
        logging.debug("LAN: New broadcast contact detected")
       #Create a brand new contact from scratch
        Contactobject = contacts.Contact(nick,status)
        Contactobject.li = uid
    else:
        Contactobject = contacts.Contactlist[getmain]
        logging.debug("LAN: Existing contact detected")

    #Add LAN transport to this object
    Contactobject.Transports['lan'] = LTO
    Contactobject.nick = nick
    Contactobject.presence = status
    Contactobject.ui_update()

    
    if(bcast_request): bcast_send() # Notify new peer that you are around


#Process LAN broadcast packet ('C<ch>,<nick>,msg')
def process_broadcast_message(addr,packet):
    m = packet[1:]
    m = str(m,'UTF-8').split(",",2)
    messages.process_broadcast_message("lan",m[0],m[1],m[2])


#Process Unsecured LAN message('M<sender lan_uid><message>')        
def process_unsecuredmsg(addr,packet):
    peer = peer_by_lan_ipport(addr[0],addr[1])
    if(peer == -1):
        logging.warning("Message received for peer not on contact list")
        return 0

    logging.info("LAN: Unencrypted message from " + str(addr[0]) +  ":"+ str(addr[1]))
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
    logging.info("LAN: Peer " + addr[0] + " has signed off")

    if(len(packet)>24):
        if(packet[1:25]) == lan_uid:
            logging.debug("LAN: Own signoff packet received")
            return False
    
    getmain = contacts.contact_by_li(packet[1:25])
    if(getmain != -1):
        contacts.Contactlist[getmain].del_transport("lan")
        logging.debug("LAN: Removing LAN transport from this peer")
    else:
        logging.debug("LAN: Peer not found on contact list")


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
                   67:process_broadcast_message,
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
    logging.info("LAN: Sending unencrypted message to "  + lc.ip +"\n Port:" + str(lc.port))
    sock.sendto(hdr,(lc.ip,lc.port))

def send_ack(mc,seq):
    lc = contacts.Contactlist[mc].Transports['lan']
    hdr = struct.pack("B",65) + struct.pack("H",seq)
    logging.info("LAN: Sending acknowledgement to "  + lc.ip +"\n Port:" + str(lc.port))
    sock.sendto(hdr,(lc.ip,lc.port))

def send_bcast_message(ch,msg):
    logging.info("LAN: Sent broadcast message")
    sock.sendto(bytes("C" + ch + "," + Myself.nick + "," + msg,'UTF-8'),(bcast_addr,bcast_port))

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
            logging.debug("LAN: Received packet of length " + str(len(data)) + " from: " + addr[0] + ":" + str(addr[1]))
            process_received(addr, data)
                          
bcast()
listener = listen()
listener.start()
