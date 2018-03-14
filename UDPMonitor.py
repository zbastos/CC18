
import time


class UDPMonitor:
    def __init__(self, table, m_time, ip, port):
        self.multicast_Time = m_time
        self.stateTable = table
        self.multicast_IP = ip
        self.multicast_PORT = port

    def multicast(self):
        """
        Multicast function, will keep running as long as UDPMonitor is up
        """
        while True:
            time.sleep(self.multicast_Time)
            #get table
            for entry in self.stateTable.getInfo():
                self.sendUDP(entry)

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
