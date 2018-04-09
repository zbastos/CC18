
import time
import socket
import sys
import struct
import json
from InfoTable import InfoTable


class UDPMonitor:

    def __init__(self, table, ip, port, m_time, timeout=1):
        self.multicast_Time = m_time
        self.stateTable = table
        self.multicast_group = (ip, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timeout = timeout

    """
            Multicast function, will keep running as long as UDPMonitor is up
    """
    def multicast(self):

        self.socket.settimeout(self.timeout)
        message = "OlHa, SoY Tu PaDrE"
        try:
            while True:
                time.sleep(self.multicast_Time)

                # depende das infos da tabela, ir buscar o maior (?)
                ttl = struct.pack('b',1)

                self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

                try:
                    print ("sending "+message)
                    sent = self.socket.sendto(bytes(message,"utf-8"), self.multicast_group)

                    while True:
                        if self.receive_msg() != 0:
                            break
                finally:
                    print("Closing socket") #(?)
        finally:
            self.socket.close()

    """
    Receive msg from random multicast server
    """
    def receive_msg(self):
        print('Waiting to receive')

        try:
            datastr, server = self.socket.recvfrom(1024)  # (?)
            # convert json object to python object
            data = json.loads(datastr)
            # update infos from client serer
            self.stateTable.updateInfo(server, data)
        except socket.timeout:
            print("Timed out, no response",end="",file=sys.stderr) 
            return -1
        else:
            print('Received message %s from %s') % (data, server)
            return 0


def main():
    #create info table to store server's info
    ip = "239.8.8.8"

    port = 8888

    time = 10

    table = InfoTable()

    #create monitor instance
    monitor = UDPMonitor(table,ip,port,time)

    #start monitor
    monitor.multicast()


if __name__ == "__main__":
    main()
