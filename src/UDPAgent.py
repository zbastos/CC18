import socket
import struct
import sys
import psutil
import json

class UDPAgent:


    def __init__(self, multicast_group, server_ipport):
        self.multicast_group = multicast_group
        self.server_port = server_ipport
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



    def getInfo(self):
        (_ ,min,max) = psutil.cpu_freq()
        (memtotal,_,_,_,_,_,_,_) = psutil.virtual_memory()

        return (min,max,memtotal)


    def receive(self):
        # Bind to the server address
        self.socket.bind(self.server_ipport)

        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = socket.inet_aton(self.multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Receive/respond loop
        while True:
            print >> sys.stderr, '\nwaiting to receive message'
            data, address = self.socket.recvfrom(1024)

            print >> sys.stderr, 'received %s bytes from %s' % (len(data), address)
            print >> sys.stderr, data

            print >> sys.stderr, 'sending acknowledgement to', address
            info = self.getInfo()
            self.socket.sendto(json.dumps(info), address)
