from socket import *
import threading
import contacts, struct, time, random
import messages

from myself import Myself

transport_trusted = False

Myself.transports['udp4':('86.43.88.90',15892)]

udp4_contacts = {}

def nfid_udp4():
    if len(udp4_contacts) == 0: return 0
    for i in range(max(udp4_contacts) + 2):
        if(i in udp4_contacts):
                continue
        else:
                return i


class udp4_contact():
    def __init__(self,addr,port):
        self.nfid = None
        self.addr = addr
        self.port = port
        self.maincontact = -1

    

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('',15892))

listen_running = True

def process_received(addr,data):
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
