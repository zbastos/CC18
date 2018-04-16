#!/usr/bin/python3

import socket
import struct
import sys
import psutil
import json

class UDPAgent:


    def __init__(self, multicast_group, server_ipport):
        self.multicast_group = multicast_group
        self.server_port = ("",server_ipport)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



    def getInfo(self):
        cpu_freq = psutil.cpu_freq()

        min = cpu_freq[1]
        max = cpu_freq[2]

        virtual = psutil.virtual_memory()

        memtotal = virtual[0]

        return (min,max,memtotal)


    def receive(self):
        # Bind to the server address
        self.socket.bind(self.server_port)

        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = socket.inet_aton(self.multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Receive/respond loop
        while True:
            print('\nWaiting to receive message')
            dataB, addressTup = self.socket.recvfrom(1024)
            dataStr = str(dataB,"utf-8")

            address = addressTup[0]

            print('Received', dataStr, 'from', address )

            print('Sending information to', address)
            info = self.getInfo()
            print ('Information: ', info)
            self.socket.sendto(bytes(json.dumps(info),"utf-8"), addressTup)

def main():
    ip = "239.8.8.8"
    port = 8888

    #create monitor instance
    agente = UDPAgent(ip,port)
    #start monitor
    agente.receive()


if __name__ == "__main__":
    main()
