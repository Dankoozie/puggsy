from socket import *
import threading
import contacts, struct, time, random
import messages



from myself import Myself

transport_trusted = False

Myself.Transports['udp4'] = ('86.43.88.90',10892)

class udp4_contact():
    def __init__(self,addr,port):
        self.addr = addr
        self.port = port    

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('',10892))

listen_running = True

def peer_by_ipport(addr,port):
    return False

#Process unsec message ('U<reachable time><status><nick>,msg')
def process_unsecuredmsg(addr,packet):
    m = packet[6:]
    m = str(m,'UTF-8').split(",",1)
    nick = m[0]
    msg = m[1]

    #Unpack reachable time / status
    
    if(peer_by_ipport(addr[0],addr[1])):
       pass #Known peer
    else:
       LTO = udp4_contact(addr[0],addr[1])
       Contactobject = contacts.Contact(m[0],0)
       

def process_received(addr,data):
    pack_switch = {85:process_unsecuredmsg}

    try:
        pack_switch[int(packet[0])](addr,packet)
    except KeyError:
        print("[BOGUS]: Invalid start byte " + str(int(packet[0])))

    print("Incoming! ", addr, data)

class listen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.recvd = 0
    def run(self):
        while listen_running:
            data, addr = sock.recvfrom(1024)
            process_received(addr, data)

listener = listen()
listener.start()
