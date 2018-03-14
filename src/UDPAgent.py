import socket
import struct
import sys

class UDPAgent:


    def __init__(self, multicast_group, server_ipport):
        self.multicast_group = multicast_group
        self.server_port = server_ipport
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
            self.socket.sendto('ack', address)

            #buscar o resto das merdas e meter na mensagem PELO MEIO SENOA O 17 ENERVA-SE E ENERVA-ME A MIM