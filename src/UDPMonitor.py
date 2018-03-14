
import time, socket, sys, struct


class UDPMonitor:
    def __init__(self, table, m_time, ip, port):
        self.multicast_Time = m_time
        self.stateTable = table
        self.multicast_group = (ip, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def multicast(self):
        """
        Multicast function, will keep running as long as UDPMonitor is up
        """

        self.socket.settimeout(1)
        message = "OlHa, SoY Tu PaDrE"

        while True:
            time.sleep(self.multicast_Time)
            # depende das infos da tabela, ir buscar o maior (?)
            ttl = struct.pack('b',1)
            self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

            try:
                print ('sending %s') %message
                sent = self.socket.sendto(message, self.multicast_group)

                while True:
                    print ('Waiting to receive')

                    try:
                        data, server = self.socket.recvfrom(16) #(?)
                    except socket.timeout:
                        print >>sys.stderr, 'Timed out, no response'
                        break
                    else:
                        print('Received message %s from %s') % (data, server)

            finally:
                print("Closing socket") #(?)

        self.socket.close()

    def sendUDP(self, entry):
        """
        Send UDP request to single server
        :return:
        """


def main():
    #create info table to store server's info
    table = InfoTable()

    #create monitor instance
    monitor = UDPMonitor(table, 30, "239.8.8.8", 8888)

    #start monitor
    monitor.multicast()


if __name__ == "__main__":
    main()
