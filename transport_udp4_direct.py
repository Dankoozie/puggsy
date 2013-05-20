from socket import *
import threading
import contacts, struct, time, random
import messages

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('192.168.1.1',49092))

listen_running = True

def process_received(addr,data):
    print("Incoming!")

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
